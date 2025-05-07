import os
import datetime
import numbers
from itertools import zip_longest
from typing import Sequence, Optional, Dict, Union


def mca_data_to_spec_string(
    mca: Sequence[float],
    title: Optional[str] = None,
    filename: Optional[str] = None,
    date: Optional[Union[str, datetime.datetime, datetime.date]] = None,
    calibration: Optional[Sequence[float]] = None,
    detector_name: Optional[str] = None,
    metadata: Optional[Dict] = None,
) -> str:
    """Official file format specs: https://certif.com/downloads/css_docs/spec_man.pdf

    :param mca: MCA spectrum
    :param title: scan title
    :param filename: name by which the file will be created
    :param date: start date of the scan
    :param calibration: MCA calibration as the sequence [zero, gain, quad],
                        all of them optional so that
                        energy = zero + gain*channels + quad*channels^2
    :param detector_name: name of the MCA detector
    :param metadata: saved as comments
    :returns: SPEC serialized string
    """
    nchan_per_line = 16
    nchan_tot = len(mca)

    if title is None:
        title = "ct"
    if filename is None:
        filename = "unspecified"
    if detector_name is None:
        detector_name = "MCA0"
    if date is None:
        date = datetime.datetime.now()
    calib = [0, 1, 0]  # zero, gain, quad
    if calibration:
        if len(calibration) > 3:
            raise ValueError("MCA calibration requires 3 only coefficients")
        calib = [
            p if p is not None else pdefault
            for p, pdefault in zip_longest(calibration, calib)
        ]

    header = [f"#F {filename}", f"#D {date}", "", f"#S {title}", f"#D {date}"]
    if metadata:
        for k, v in metadata.items():
            header.append(f"#C {k} = {v}")
    header.append("#N 1")
    header.append(f"#@MCA {nchan_per_line}C")
    header.append(f"#@CHANN {nchan_tot} 0 {nchan_tot-1} 1")
    header.append(f"#@CALIB {' '.join(map(str, calib))}")
    header.append("#@MCA_NB 1")
    header.append(f"#L {detector_name}")

    mcastring = "\n".join(header)

    mcastring += "\n@A"
    if isinstance(mca[0], numbers.Integral):
        fmt = " %d"
    else:
        # fmt = " %.4f"
        fmt = " %.8g"
    for idx in range(0, nchan_tot, nchan_per_line):
        if idx + nchan_per_line - 1 < nchan_tot:
            for i in range(0, nchan_per_line):
                mcastring += fmt % mca[idx + i]
            if idx + nchan_per_line != nchan_tot:
                mcastring += "\\"
        else:
            for i in range(idx, nchan_tot):
                mcastring += fmt % mca[i]
        mcastring += "\n"
    return mcastring


def save_as_spec(filename, mca: Sequence[float], **kwargs) -> None:
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    content = mca_data_to_spec_string(mca, filename=filename, **kwargs)
    with open(filename, "w") as f:
        f.write(content)
