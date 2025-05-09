ultrasound-processing

ultrasound-processing is a Python package designed for processing, transforming, and analyzing ultrasound image data. It includes utilities for masking, interpolation, volumetric transformations, and geometric corrections to convert polar or curvilinear images to flat formats.

 Installation

Install the package directly from PyPI:

pip install ultrasound-processing

Or install the latest development version from GitHub:

pip install git+https://github.com/Mart-SciecPyt/ScPytone_ultrasound_processing.git

 What does it do?

This library includes the following core functionalities:

Noise masking of ultrasound image data (2D slices and volumes)

Interpolation of irregular image data onto uniform grids

Geometric transformations from curved (polar) formats to flat images

Volumetric stacking and reshaping of slice data

 Modules Overview

mask.py

Provides noise filtering and artifact masking.

from ultrasound_processing.mask import mask_volume

masked = mask_volume(volume, threshold=0.1)

interp.py

Performs interpolation on 2D and 3D ultrasound data.

from ultrasound_processing.interp import interpolate_2d

grid_data = interpolate_2d(raw_image, method="linear")

transform.py

Converts curvilinear ultrasound images into flat geometry.

from ultrasound_processing.transform import polar_to_cartesian

flat_image = polar_to_cartesian(polar_image, angle_array, radius_array)

VolumeTransformer

Class-based utility for advanced 3D ultrasound volume processing.

from ultrasound_processing.interp_img import VolumeTransformer

vt = VolumeTransformer(volume)
flattened_volume = vt.to_flat()

 Use in Google Colab

You can try out the package in this interactive Google Colab notebook, which demonstrates:

Loading and visualizing ultrasound data

Applying masking and noise filtering

Performing geometric flattening

Exporting final processed volumes

 Example Use Case

import numpy as np
from ultrasound_processing.mask import mask_volume
from ultrasound_processing.transform import polar_to_cartesian

# Simulate raw polar data
raw = np.random.rand(256, 256)
angles = np.linspace(0, np.pi, 256)
radii = np.linspace(0, 100, 256)

# Apply transformation
cartesian = polar_to_cartesian(raw, angles, radii)

# Apply masking
cleaned = mask_volume(cartesian, threshold=0.2)

 Documentation

Full documentation is available at:https://scpytone-ultrasound-processing.readthedocs.io

 Contributing

Contributions are welcome! Please fork the GitHub repository and submit a pull request:
https://github.com/Mart-SciecPyt/ScPytone_ultrasound_processing

For feature requests or bugs, open an issue on GitHub.

Uploading to PyPI

Ensure build and twine are installed:

pip install build twine

Build the package:

python -m build

Upload to PyPI:

twine upload dist/*

Log in using your PyPI credentials when prompted.

 Author

Developed by: Trancsik MartinProject: ScPytone Ultrasound Processing Suite

