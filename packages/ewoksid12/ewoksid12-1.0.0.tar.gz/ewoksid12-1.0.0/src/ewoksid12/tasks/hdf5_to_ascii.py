import logging
import os
from typing import Optional, Sequence

from blissdata.h5api import dynamic_hdf5
from ewokscore.task import Task

from .io import save_as_ascii

logger = logging.getLogger(__name__)


class Hdf5ToAscii(
    Task,
    input_names=["filename", "output_filename"],
    optional_input_names=["scan_numbers", "retry_timeout", "retry_period", "counters"],
    output_names=["counters", "output_filenames"],
):
    """Save 1D data from Bliss HDF5 scans in ID12 ASCII files."""

    def run(self):
        filename: str = self.inputs.filename
        scan_numbers: Optional[Sequence[int]] = self.get_input_value(
            "scan_numbers", None
        )
        retry_timeout: Optional[float] = self.get_input_value("retry_timeout", None)
        retry_period: Optional[float] = self.get_input_value("retry_period", 1)
        counters: Optional[Sequence[str]] = self.get_input_value("counters", "all")

        output_filename: str = self.inputs.output_filename
        dirname = os.path.dirname(output_filename)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        basename = os.path.basename(output_filename)

        output_filenames = list()
        failed_scans = list()

        with dynamic_hdf5.File(
            filename, retry_timeout=retry_timeout, retry_period=retry_period
        ) as nxroot:
            if scan_numbers:
                scan_names = [f"{scannr}.1" for scannr in scan_numbers]
            else:
                scan_names = nxroot

            for scan_name in scan_names:
                scan_number = int(float(scan_name))
                try:
                    _ = nxroot[f"/{scan_name}/end_time"]  # wait for scan to finish
                    measurement = nxroot[f"/{scan_name}/measurement"]
                    data = dict()

                    # Convert counters to a list if it is a string.
                    if isinstance(counters, str):
                        counters = [counters]
                    else:
                        counters = list(counters)

                    # Replace all occurrence of "all".
                    if "all" in counters:
                        while "all" in counters:
                            counters.remove("all")
                        counters.extend(measurement.keys())

                    # Remove duplicates while preserving order.
                    counters = list(dict.fromkeys(counters))

                    for counter in counters:
                        try:
                            dataset = measurement[counter]
                        except Exception as e:
                            logger.warning(
                                "Skipping counter '%s' in scan %s: %s (%s)",
                                counter,
                                scan_name,
                                str(e),
                                e.__class__.__name__,
                            )
                            continue
                        if dataset.ndim == 1:
                            data[counter] = dataset[()]
                except Exception as e:
                    failed_scans.append(scan_number)
                    logger.error(
                        "Processing scan %s::/%s failed (%s)", filename, scan_name, e
                    )
                    continue

                if not data:
                    # Scan has no data to save
                    continue

                scan_output_filename = os.path.join(
                    dirname, f"scan{scan_number:03d}_{basename}"
                )
                save_as_ascii(scan_output_filename, data)
                output_filenames.append(scan_output_filename)

        if failed_scans:
            raise RuntimeError(f"Failed scans (see logs why): {failed_scans}")

        self.outputs.counters = counters
        self.outputs.output_filenames = output_filenames
