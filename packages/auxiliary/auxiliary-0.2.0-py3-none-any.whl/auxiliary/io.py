from pathlib import Path
from typing import Optional

import SimpleITK as sitk
from numpy.typing import NDArray


def write_image(
    input_array: NDArray,
    output_path: str,
    reference_path: Optional[str] = None,
    create_parent_directory: bool = False,
) -> None:
    """
    Write an image file from a NumPy array using SimpleITK.
    Supports e.g. NIfTI and other formats. More details: https://simpleitk.readthedocs.io/en/master/IO.html

    Args:
        input_array (np.ndarray): The NumPy array containing the data to be written.
        output_path (str): The path where the output file will be saved.
        reference_path (str, optional): Path to a reference file for spatial metadata.
        create_parent_directory (bool): If True, create parent directories if they don't exist.

    Returns:
        None
    """
    # Convert NumPy array to SimpleITK image (zyx expected)
    image = sitk.GetImageFromArray(input_array)

    if reference_path:
        reference = sitk.ReadImage(reference_path)
        image.CopyInformation(reference)

    if create_parent_directory:
        parent_dir = Path(output_path).parent
        parent_dir.mkdir(parents=True, exist_ok=True)

    sitk.WriteImage(image, output_path)


def read_image(
    input_path: str,
    maintain_dtype: bool = True,
) -> NDArray:
    """
    Read an image file using SimpleITK and return its data as a NumPy array.
    Supports e.g. NIfTI and other formats. More details: https://simpleitk.readthedocs.io/en/master/IO.html

    Args:
        input_path (str): Path to the input file.
        maintain_dtype (bool, optional): If True, maintain the data type of the image data.
                                         If False, allow data type conversion to float. Default is True.

    Returns:
        numpy.ndarray: Image data as a NumPy array.
    """

    image = sitk.ReadImage(input_path)
    if maintain_dtype:
        array = sitk.GetArrayFromImage(image)
    else:
        array = sitk.GetArrayFromImage(sitk.Cast(image, sitk.sitkFloat32))

    return array
