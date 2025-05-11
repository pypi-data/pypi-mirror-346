import os

import h5py
import numpy


def offline_saxs_data(
    dataset_dirname: str,
    scan_number: int = 1,
    image_shape: tuple = (10, 11),
    npoints: int = 13,
    images_per_file: int = 5,
) -> dict:
    # Compute number of Lima files and distribute images
    nfiles = npoints // images_per_file
    remainder = npoints % images_per_file
    if remainder:
        images_per_file = [images_per_file] * nfiles + [remainder]
        nfiles += 1
    else:
        images_per_file = [images_per_file] * nfiles

    # Lima files
    pixel_value = 0
    lima_dir = os.path.join(dataset_dirname, f"scan{scan_number:04d}")
    os.makedirs(lima_dir, exist_ok=True)
    dtype = int
    for i, num_images in enumerate(images_per_file):
        file_path = os.path.join(lima_dir, f"lima_{i:04d}.h5")
        with h5py.File(file_path, "w") as f:
            lima_shape = (num_images, *image_shape)
            dset = f.create_dataset("/entry/data", shape=lima_shape, dtype=dtype)
            for i in numpy.arange(num_images):
                dset[i] = pixel_value + i
            dset.attrs["interpretation"] = "image"
        pixel_value += num_images

    # Bliss dataset file
    scan_file_path = os.path.join(dataset_dirname, "sample_0001.h5")
    with h5py.File(scan_file_path, "w") as f:
        nxdetector = f.create_group(f"/{scan_number}.1/instrument/lima")
        nxdetector["type"] = "lima"

        layout_shape = (npoints, *image_shape)
        layout = h5py.VirtualLayout(shape=layout_shape, dtype=dtype)
        offset = 0
        for i, num_images in enumerate(images_per_file):
            rel_file_path = os.path.join(f"scan{scan_number:04d}", f"lima_{i:04d}.h5")
            lima_shape = (num_images, *image_shape)
            vsource = h5py.VirtualSource(rel_file_path, "/entry/data", shape=lima_shape)
            layout[offset : offset + num_images] = vsource
            offset += num_images

        _ = nxdetector.create_virtual_dataset("image", layout)

        positioners_start = f.create_group(
            f"/{scan_number}.1/instrument/positioners_start"
        )
        positioners_start["energy"] = 12.4
        positioners_start["energy"].attrs["units"] = "keV"

    return {"scan_file_path": scan_file_path, "scan_number": scan_number}
