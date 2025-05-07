from .model.ctabgan import CTAB_XTRA_DP


from .model import evaluation as _evaluation

evaluation = _evaluation

from .datasets.dataset_loader import load_demo , display_demo


__all__ = [
    "CTAB_XTRA_DP",
    "evaluation",
    "load_demo",
    "display_demo",
]


__version__ = "0.1.0"