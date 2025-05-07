from typing import List

import h5py
import pytest

from ..tasks.hdf5_to_ascii import Hdf5ToAscii


@pytest.mark.parametrize(
    "counters",
    [
        ["counter1", "counter2"],
        "all",
        ["counter2", "all"],
        ["counter2"],
    ],
)
def test_hdf5_to_spec(tmp_path, counters):
    filename = tmp_path / "RAW_DATA" / "bliss_dataset.h5"
    filename.parent.mkdir()
    filename = str(filename)
    output_filename = str(tmp_path / "PROCESSED_DATA" / "bliss_dataset.dat")

    nscans = 3
    nchannels = 10
    with h5py.File(filename, "w") as nxroot:
        for scan in range(1, nscans + 1):
            _save_scan_content(nxroot, scan, nchannels)

    inputs = {
        "filename": filename,
        "scan_numbers": list(range(1, nscans + 1)),
        "output_filename": output_filename,
        "counters": counters,
    }
    task = Hdf5ToAscii(inputs=inputs)
    task.run()

    output_filenames = [
        str(tmp_path / "PROCESSED_DATA" / f"scan{i:03d}_bliss_dataset.dat")
        for i in range(1, nscans + 1)
    ]
    output_values = task.get_output_values()
    assert output_values["output_filenames"] == output_filenames

    counters = output_values["counters"]
    _assert_ascii_content(output_filenames, counters, nchannels)


def test_hdf5_to_spec_failed(tmp_path):
    filename = tmp_path / "RAW_DATA" / "bliss_dataset.h5"
    filename.parent.mkdir()
    filename = str(filename)
    output_filename = str(tmp_path / "PROCESSED_DATA" / "bliss_dataset.dat")

    nscans = 1
    nchannels = 10
    with h5py.File(filename, "w") as nxroot:
        for scan in range(1, nscans + 1):
            _save_scan_content(nxroot, scan, nchannels)

    inputs = {
        "filename": filename,
        "scan_numbers": list(range(1, nscans + 3)),
        "output_filename": output_filename,
        "counters": ["counter1", "counter2"],
        "retry_timeout": 0.1,
    }
    task = Hdf5ToAscii(inputs=inputs)
    with pytest.raises(
        RuntimeError, match=r"^Failed scans \(see logs why\): \[2, 3\]$"
    ):
        task.run()

    output_filenames = [tmp_path / "PROCESSED_DATA" / "scan001_bliss_dataset.dat"]
    counters = inputs["counters"]
    _assert_ascii_content(output_filenames, counters, nchannels)


def _save_scan_content(nxroot: h5py.Group, scan: int, nchannels: int) -> None:
    nxroot[f"/{scan}.1/start_time"] = "start_time"
    nxroot[f"/{scan}.1/title"] = "timescan 0.1"
    for counter in ["counter1", "counter2"]:
        factor = 10 ** (int(counter[-1]) - 1)
        nxroot[f"/{scan}.1/measurement/{counter}"] = [
            scan + i / factor for i in range(nchannels)
        ]
    nxroot[f"/{scan}.1/end_time"] = "end_time"


def _assert_ascii_content(
    output_filenames: List[str],
    counters: List[str],
    nchannels: int,
):
    for scan, filename in enumerate(output_filenames, 1):
        with open(filename, "r") as f:
            header = "  ".join(counters)
            expected_lines = [header]
            for i in range(nchannels):
                values = []
                for counter in counters:
                    # Calculate factor based on the suffix of the counter name.
                    factor = 10 ** (int(counter[-1]) - 1)
                    value = scan + i / factor
                    values.append(str(value))
                expected_lines.extend([" ".join(values)])

            actual_lines = [s.rstrip() for s in f.readlines()]
            assert actual_lines == expected_lines
