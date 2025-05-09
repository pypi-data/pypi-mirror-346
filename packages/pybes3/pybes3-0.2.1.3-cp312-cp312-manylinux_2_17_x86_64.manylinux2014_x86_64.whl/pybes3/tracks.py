from typing import Literal, Union

import awkward as ak
import numba as nb
import numpy as np

from .typing import FloatLike


@nb.vectorize([nb.float64(nb.float64, nb.float64)], cache=True)
def _helix01_to_x(helix0: FloatLike, helix1: FloatLike) -> FloatLike:
    """
    Convert helix parameters to x location.

    Parameters:
        helix0: helix[0] parameter, dr.
        helix1: helix[1] parameter, phi0.

    Returns:
        x location of the helix.
    """
    return helix0 * np.cos(helix1)


@nb.vectorize([nb.float64(nb.float64, nb.float64)], cache=True)
def _helix01_to_y(helix0: FloatLike, helix1: FloatLike) -> FloatLike:
    """
    Convert helix parameters to y location.

    Parameters:
        helix0: helix[0] parameter, dr.
        helix1: helix[1] parameter, phi0.

    Returns:
        y location of the helix.
    """
    return helix0 * np.sin(helix1)


@nb.vectorize([nb.float64(nb.float64)], cache=True)
def _helix2_to_pt(
    helix2: FloatLike,
) -> FloatLike:
    """
    Convert helix parameter to pt.

    Parameters:
        helix2: helix[2] parameter, kappa.

    Returns:
        pt of the helix.
    """
    return 1 / np.abs(helix2)


@nb.vectorize([nb.int8(nb.float64)], cache=True)
def _helix2_to_charge(
    helix2: FloatLike,
) -> FloatLike:
    """
    Convert helix parameter to charge.

    Parameters:
        helix2: helix[2] parameter, kappa.

    Returns:
        charge of the helix.
    """
    if -1e-10 < helix2 < 1e-10:
        return 0
    return 1 if helix2 > 0 else -1


@nb.vectorize([nb.float64(nb.float64, nb.float64)], cache=True)
def _pt_helix1_to_px(pt: FloatLike, helix1: FloatLike) -> FloatLike:
    """
    Convert pt and helix1 to px.

    Parameters:
        pt: pt of the helix.
        helix1: helix[1] parameter, phi0.

    Returns:
        px of the helix.
    """
    return -pt * np.sin(helix1)


@nb.vectorize([nb.float64(nb.float64, nb.float64)], cache=True)
def _pt_helix1_to_py(pt: FloatLike, helix1: FloatLike) -> FloatLike:
    """
    Convert pt and helix1 to py.

    Parameters:
        pt: pt of the helix.
        helix1: helix[1] parameter, phi0.

    Returns:
        py of the helix.
    """
    return pt * np.cos(helix1)


@nb.vectorize([nb.float64(nb.float64, nb.float64)], cache=True)
def _pt_helix4_to_p(pt: FloatLike, helix4: FloatLike) -> FloatLike:
    """
    Convert pt and helix4 to p.

    Parameters:
        pt: pt of the helix.
        helix4: helix[4] parameter, tanl.

    Returns:
        p of the helix.
    """
    return pt * np.sqrt(1 + helix4**2)


@nb.vectorize([nb.float64(nb.float64, nb.float64)], cache=True)
def _pz_p_to_theta(pz: FloatLike, p: FloatLike) -> FloatLike:
    """
    Convert pz and p to theta.

    Parameters:
        pz: pz of the helix.
        p: p of the helix.

    Returns:
        theta of the helix.
    """
    return np.arccos(pz / p)


def parse_helix(
    helix: Union[ak.Array, np.ndarray], library: Literal["ak", "auto"] = "auto"
) -> Union[ak.Array, dict[str, np.ndarray]]:
    """
    Parse helix parameters to physical parameters.

    Parameters:
        helix: helix parameters, the last dimension should be 5.
        library: the library to use, if "auto", return a dict when input is np.ndarray, \
            return an ak.Array when input is ak.Array. If "ak", return an ak.Array.

    Returns:
        parsed physical parameters. "x", "y", "z", "r" for position, \
            "pt", "px", "py", "pz", "p", "theta", "phi" for momentum, \
            "charge" for charge, "r_trk" for track radius.
    """
    helix0 = helix[..., 0]
    helix1 = helix[..., 1]
    helix2 = helix[..., 2]
    helix3 = helix[..., 3]
    helix4 = helix[..., 4]

    x = _helix01_to_x(helix0, helix1)
    y = _helix01_to_y(helix0, helix1)
    z = helix3
    r = np.abs(helix0)

    pt = _helix2_to_pt(helix2)
    px = _pt_helix1_to_px(pt, helix1)
    py = _pt_helix1_to_py(pt, helix1)
    pz = pt * helix4
    p = _pt_helix4_to_p(pt, helix4)
    theta = _pz_p_to_theta(pz, p)
    phi = np.arctan2(py, px)

    charge = _helix2_to_charge(helix2)

    r_trk = pt * (10 / 2.99792458)  # |pt| * [GeV/c] / 1[e] / 1[T] = |pt| * 10/3 [m]
    r_trk = r_trk * 100  # to [cm]

    res_dict = {
        "x": x,
        "y": y,
        "z": z,
        "r": r,
        "px": px,
        "py": py,
        "pz": pz,
        "pt": pt,
        "p": p,
        "theta": theta,
        "phi": phi,
        "charge": charge,
        "r_trk": r_trk,
    }

    if isinstance(helix, ak.Array) or library == "ak":
        return ak.zip(res_dict)
    else:
        return res_dict
