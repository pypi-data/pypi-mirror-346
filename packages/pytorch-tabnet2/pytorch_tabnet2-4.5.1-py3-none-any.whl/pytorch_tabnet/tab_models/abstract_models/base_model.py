"""Abstract base model definition for TabNet."""

import copy
import io
import json
import shutil
import warnings
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import numpy as np
import torch
from sklearn.base import BaseEstimator

from ...callbacks import (
    CallbackContainer,
)
from ...error_handlers.embedding_errors import check_embedding_parameters
from ...utils import (
    ComplexEncoder,
    define_device,
)
from ...utils.explain import explain_v1


@dataclass
class _TabModel(BaseEstimator):
    compile_backends = ["inductor", "cudagraphs", "ipex", "onnxrt"]

    n_d: int = 8
    n_a: int = 8
    n_steps: int = 3
    gamma: float = 1.3
    cat_idxs: List[int] = field(default_factory=list)
    cat_dims: List[int] = field(default_factory=list)
    cat_emb_dim: Union[int, List[int]] = 1
    n_independent: int = 2
    n_shared: int = 2
    epsilon: float = 1e-15
    momentum: float = 0.02
    lambda_sparse: float = 1e-3
    seed: int = 0
    clip_value: int = 1
    verbose: int = 1
    optimizer_fn: Any = torch.optim.Adam
    optimizer_params: Dict = field(default_factory=lambda: dict(lr=2e-2))
    scheduler_fn: Any = None
    scheduler_params: Dict = field(default_factory=dict)
    mask_type: str = "sparsemax"
    input_dim: int = None
    output_dim: Union[List[int], int] = None
    device_name: str = "auto"
    n_shared_decoder: int = 1
    n_indep_decoder: int = 1
    grouped_features: List[List[int]] = field(default_factory=list)
    _callback_container: CallbackContainer = field(default=None, repr=False, init=False, compare=False)
    compile_backend: str = ""

    def __post_init__(self) -> None:
        """Initialize default values and device for TabModel."""
        self.batch_size: int = 1024
        self.virtual_batch_size: int = 128

        torch.manual_seed(self.seed)
        self.device = torch.device(define_device(self.device_name))
        if self.verbose != 0:
            warnings.warn(f"Device used : {self.device}", stacklevel=2)

        self.optimizer_fn = copy.deepcopy(self.optimizer_fn)
        self.scheduler_fn = copy.deepcopy(self.scheduler_fn)

        updated_params = check_embedding_parameters(self.cat_dims, self.cat_idxs, self.cat_emb_dim)
        self.cat_dims, self.cat_idxs, self.cat_emb_dim = updated_params

    def __update__(self, **kwargs: Any) -> None:
        """Update model parameters with provided keyword arguments.

        If a parameter does not already exist, it is created. Otherwise, it is overwritten with a warning.
        """
        update_list = [
            "cat_dims",
            "cat_emb_dim",
            "cat_idxs",
            "input_dim",
            "mask_type",
            "n_a",
            "n_d",
            "n_independent",
            "n_shared",
            "n_steps",
            "grouped_features",
        ]
        for var_name, value in kwargs.items():
            if var_name in update_list:
                setattr(self, var_name, value)

    def explain(self, X: np.ndarray, normalize: bool = False) -> Tuple[np.ndarray, Dict]:
        """Return local explanation.

        Parameters
        ----------
        X : tensor: `torch.Tensor` or matrix: `scipy.sparse.csr_matrix`
            Input data.
        normalize : bool (default False)
            Whether to normalize so that sum of features are equal to 1.

        Returns
        -------
        np.ndarray
            Importance per sample, per columns.
        dict
            Sparse matrix showing attention masks used by network.

        """
        self.network.eval()
        device = self.device
        network = self.network
        reducing_matrix = self.reducing_matrix
        batch_size = self.batch_size

        res_explain, res_masks = explain_v1(X, batch_size, device, network, normalize, reducing_matrix)

        return res_explain, res_masks

    def load_weights_from_unsupervised(self, unsupervised_model: "_TabModel") -> None:
        """Load weights from a previously trained unsupervised TabNet model.

        Parameters
        ----------
        unsupervised_model : pytorch_tabnet.tab_models.abstract_models.TabModel
            Previously trained unsupervised TabNet model.

        """
        update_state_dict = copy.deepcopy(self.network.state_dict())
        for param, weights in unsupervised_model.network.state_dict().items():
            if param.startswith("encoder"):
                new_param = "tabnet." + param
            else:
                new_param = param
            if self.network.state_dict().get(new_param) is not None:
                update_state_dict[new_param] = weights

        self.network.load_state_dict(update_state_dict)

    def load_class_attrs(self, class_attrs: Dict) -> None:
        """Load class attributes from a dictionary.

        Parameters
        ----------
        class_attrs : dict
            Dictionary of class attributes to set.

        """
        for attr_name, attr_value in class_attrs.items():
            setattr(self, attr_name, attr_value)

    def save_model(self, path: str) -> str:
        """Save TabNet model in two distinct files.

        Parameters
        ----------
        path : str
            Path of the model.

        Returns
        -------
        str
            Input filepath with ".zip" appended.

        """
        saved_params = {}
        init_params = {}
        for key, val in self.get_params().items():
            if isinstance(val, type):
                continue
            else:
                init_params[key] = val
        saved_params["init_params"] = init_params

        class_attrs = {"preds_mapper": self.preds_mapper}
        saved_params["class_attrs"] = class_attrs

        Path(path).mkdir(parents=True, exist_ok=True)

        with open(Path(path).joinpath("model_params.json"), "w", encoding="utf8") as f:
            json.dump(saved_params, f, cls=ComplexEncoder)

        torch.save(self.network.state_dict(), Path(path).joinpath("network.pt"))
        shutil.make_archive(path, "zip", path)
        shutil.rmtree(path)
        print(f"Successfully saved model at {path}.zip")
        return f"{path}.zip"

    def load_model(self, filepath: str) -> None:
        """Load TabNet model.

        Parameters
        ----------
        filepath : str
            Path of the model.

        Raises
        ------
        KeyError
            If the zip file is missing required components.

        """
        try:
            with zipfile.ZipFile(filepath) as z:
                with z.open("model_params.json") as f:
                    loaded_params = json.load(f)
                    loaded_params["init_params"]["device_name"] = self.device_name
                with z.open("network.pt") as f:
                    try:
                        saved_state_dict = torch.load(f, map_location=self.device)
                    except io.UnsupportedOperation:
                        saved_state_dict = torch.load(
                            io.BytesIO(f.read()),
                            map_location=self.device,
                        )
        except KeyError:
            raise KeyError("Your zip file is missing at least one component")

        self.__init__(**loaded_params["init_params"])  # type: ignore

        self._set_network()
        self.network.load_state_dict(saved_state_dict)
        self.network.eval()
        self.load_class_attrs(loaded_params["class_attrs"])

        return
