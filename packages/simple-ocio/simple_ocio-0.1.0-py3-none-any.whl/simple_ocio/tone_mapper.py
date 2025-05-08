"""
ToneMapper: zero-copy NumPy ⇄ OpenColorIO interface.

* Bundled Filmic config if no path is supplied.
* Uses OCIO 2.x `CPUProcessor.applyRGB(np.ndarray)` for in-place processing.
"""

from __future__ import annotations
from pathlib import Path
from importlib import resources as _rsc
import numpy as np
import PyOpenColorIO as OCIO


_OCIO_SUBDIR = "ocio_data"          # inside simple_ocio package


def _default_cfg_path() -> str:
    """ Locate bundled `config.ocio` relative to package. """
    return str(_rsc.files(__package__).joinpath(_OCIO_SUBDIR, "config.ocio"))


class ToneMapper:
    """
    Parameters
    ----------
    view : str
        OCIO *view* (e.g. "Filmic", "AgX"). Default = "Filmic".
    ocio_cfg : str | Path | None
        Path to an OCIO `config.ocio`. If *None*, use bundled Filmic.
    """

    def __init__(
        self,
        view: str = "Filmic",
        ocio_cfg: str | Path | None = None,
    ):
        ocio_cfg = ocio_cfg or _default_cfg_path()
        self.config = OCIO.Config.CreateFromFile(str(ocio_cfg))
        OCIO.SetCurrentConfig(self.config)

        self.display = self.config.getDefaultDisplay()
        self._view = view

        self.xform = OCIO.DisplayViewTransform(OCIO.ROLE_SCENE_LINEAR, self.display, self.view)
        self.cpu = self.config.getProcessor(self.xform).getDefaultCPUProcessor()

    @property
    def view(self) -> str:
        return self._view

    @view.setter
    def view(self, value: str):
        self._view = value
        self.xform.setView(value)
        del self.cpu
        self.cpu = self.config.getProcessor(self.xform).getDefaultCPUProcessor()

    @property
    def available_views(self) -> list[str]:
        return list(self.config.getViews(self.display))

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def hdr_to_ldr(self, hdr: np.ndarray, clip: bool = True) -> np.ndarray:
        """
        Tone-map HDR -> LDR (both float32, NumPy).

        Accepts RGB or RGBA arrays.  Values are expected in linear scene-referred
        [0,+infinity).  Output will be display-referred [0,1] (clipped if `clip`).

        Notes
        -----
        `CPUProcessor.applyRGB` works *in place* and requires:
        * contiguous buffer
        * dtype float32 (or matching OCIO bit-depth)
        """

        channels = hdr.shape[-1]
        if channels not in [3, 4]:
            raise ValueError("Input must be RGB or RGBA array")
        
        arr = np.array(hdr, dtype=np.float32, copy=True, order='C')

        if channels == 4:
            self.cpu.applyRGBA(arr)
        else:
            self.cpu.applyRGB(arr)

        if clip:
            np.clip(arr, 0.0, 1.0, out=arr)
        return arr
