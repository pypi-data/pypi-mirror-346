import os
import pathlib
import pickle
import re
from typing import Literal, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio as rio
import xarray as xr


def create_array(
    path: Union[str, pathlib.Path],
    *,
    save_pickle: bool = False,
) -> xr.DataArray:
    """
    Build a Sentinel-2 data cube from a folder of masked GeoTIFFs.

    Parameters
    ----------
    path : str | pathlib.Path
        Folder with the GeoTIFF files (one image per date).
    save_pickle : bool, default False
        If True, saves the DataArray to “s2_data.pkl”.

    Returns
    -------
    xr.DataArray
        Cube with dims (time, band, y, x) and values in 0-1 reflectance.
    """
    path = pathlib.Path(path)
    tif_files = list(path.rglob("*.tif"))

    re_date = re.compile(r"(\d{4}-\d{2}-\d{2})")
    re_cdf  = re.compile(r"_(\d+)\.tif$", re.IGNORECASE)

    meta: Optional[dict] = None
    crs_ref = None
    data, dates, cdfs = [], [], []

    for tif in tif_files:
        m_date, m_cdf = re_date.search(tif.name), re_cdf.search(tif.name)
        if not (m_date and m_cdf):
            raise ValueError(f"Unexpected name: {tif.name}")

        with rio.open(tif) as src:
            img = src.read()
            if np.all((img == 0) | (img == 65535)):   # discard empty scene
                continue
            if meta is None:
                meta, crs_ref = src.profile, src.crs
 
            data.append(img)

        dates.append(m_date.group(1))
        cdfs.append(int(m_cdf.group(1)) / 100)

    if not data:
        raise RuntimeError("No valid scenes found.")

    cube = np.stack(data, axis=0)

    y0, x0 = meta["transform"][5], meta["transform"][2]
    yres, xres = meta["transform"][4], meta["transform"][0]

    da = xr.DataArray(
        cube,
        dims=("time", "band", "y", "x"),
        coords={
            "time":   dates,
            "cs_cdf": ("time", cdfs),
            "band":   np.arange(1, cube.shape[1] + 1),
            "y":      y0 + np.arange(cube.shape[2]) * yres,
            "x":      x0 + np.arange(cube.shape[3]) * xres,
        },
        attrs={
            **{k: v for k, v in meta.items() if k not in ("transform", "dtype", "crs")},
            "crs_wkt": crs_ref.to_wkt(),
        },
    )

    if save_pickle:
        with open(path / "s2_data.pkl", "wb") as fp:
            pickle.dump(da, fp, protocol=pickle.HIGHEST_PROTOCOL)

    return da


def load_array(outdata: Union[str, pathlib.Path]) -> xr.DataArray:
    """Load a xarray DataArray from a pickle file.

    Args:
        outdata (Union[str, pathlib.Path]): The path to the pickle file.

    Returns:
        xr.DataArray: A xarray DataArray containing the S2 images.
    """

    with open(outdata, "rb") as f:
        s2_data = pickle.load(f)

    return s2_data


# Plot the scatter plot ------------------------------------------------------
def warp2df(
    warps: list,
    dates: np.ndarray,
    date_cutoff: Optional[str] = "2022-01-31"
) -> pd.DataFrame:
    """Create a dataframe with the warps and dates

    Args:
        warps (list): The warps found by the alignment model.
        dates (np.ndarray): The dates of the warps.
        date_cutoff (Optional[str], optional): The date cutoff.
            Defaults to "2022-01-31".

    Returns:
        pd.DataFrame: A dataframe with the warps and dates.
    """

    # create a dataframe with the warps and dates
    warp_translation = [warp[:2, 2] for warp in warps]
    df = pd.DataFrame(warp_translation, columns=["x", "y"])
    df["date"] = pd.to_datetime(dates)
    df["after"] = df["date"] > pd.to_datetime(date_cutoff)
    return df


def plot_s2_scatter(warp_df: pd.DataFrame) -> Tuple[plt.Figure, plt.Axes]:
    """Scatter plot of the S2 images with the warps affine matrices

    Args:
        warp_df (pd.DataFrame): The dataframe with the warps.

    Returns:
        Tuple[plt.Figure, plt.Axes]: The figure and axes of the plot.
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    # x1, y1 are the points after the fix in spatial alignment
    # x2, y2 are the points before the fix in spatial alignment
    x1, y1 = warp_df[warp_df["after"]]["x"], warp_df[warp_df["after"]]["y"]
    x2, y2 = warp_df[~warp_df["after"]]["x"], warp_df[~warp_df["after"]]["y"]
    
    # Build the scatter plot
    ax.scatter(x1, y1, label="After Cutoff date", color="blue", alpha=0.5)
    ax.scatter(x2, y2, label="Before  Cutoff date", color="red", alpha=0.5)
    ax.legend()

    return fig, ax

def plot_rgb(
    warped_cube: np.ndarray,
    raw_cube: np.ndarray,
    dates: np.ndarray,
    rgb_band: Optional[list] = [3, 2, 1],
    intensity_factor: Optional[int] = 3,
    index: Optional[int] = 0,
) -> Tuple[plt.Figure, plt.Axes]:
    """ Plot a RGB image from the raw and warped cube for
    a given index (date).

    Args:
        warped_cube (np.ndarray): Aligned cube
        raw_cube (np.ndarray): Original cube
        dates (np.ndarray): Dates of the cube
        rgb_band (Optional[list], optional): RGB bands to use. Defaults to [3, 2, 1].
        intensity_factor (Optional[int], optional): A factor to scale the pixel values. 
            Defaults to 3.
        index (Optional[int], optional): The index of the date. Defaults to 0.

    Returns:
        Tuple[plt.Figure, plt.Axes]: The figure and axes of the plot.
    """

    # create a image from the raw and warped cube
    warped_cube_img = warped_cube[index, rgb_band]
    warped_cube_img = np.transpose(warped_cube_img, (1, 2, 0))
    raw_cube_img = raw_cube[index, rgb_band]
    raw_cube_img = np.transpose(raw_cube_img, (1, 2, 0))

    to_display1 = (raw_cube_img * intensity_factor).clip(0, 1)
    to_display2 = (warped_cube_img * intensity_factor).clip(0, 1)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(to_display1)
    axs[0].set_title(f"Original Cube - {str(dates[index])}")
    axs[0].axis("off")
    axs[1].imshow(to_display2)
    axs[1].set_title(f"Aligned Cube - {str(dates[index])}")
    axs[1].axis("off")

    return fig, axs


def plot_animation1(
    warped_cube: np.ndarray,
    raw_cube: np.ndarray,
    dates: np.ndarray,
    png_output_folder: Union[str, pathlib.Path],
    gif_output_file: Union[str, pathlib.Path],
    rgb_band: Union[int, list, None] = [3, 2, 1],
    intensity_factor: int = 3,
    gif_delay: int = 20,
    gif_loop: int = 0,
) -> pathlib.Path:
    """Create a gif animation from the raw and warped cube

    Args:
        warped_cube (np.ndarray): The aligned cube
        raw_cube (np.ndarray): The original cube
        dates (np.ndarray): The dates of the cube
        png_output_folder (Union[str, pathlib.Path]): The folder to save the 
            png files.
        gif_output_file (Union[str, pathlib.Path]): The gif file to save.
        rgb_band (Union[int, list, None], optional): The RGB bands to use.
            Defaults to [3, 2, 1].
        intensity_factor (int, optional): The intensity factor, used to scale
            the pixel values. Defaults to 3.
        gif_delay (int, optional): The delay between the images. Defaults to 20.
        gif_loop (int, optional): The number of loops. Defaults to 0.

    Raises:
        ValueError: The two cubes must have the same shape
        ValueError: The error creating the gif

    Returns:
        pathlib.Path: The path to the gif file.
    """
    # check if the system has ImageMagick installed
    if os.system("convert -version") != 0:
        raise ValueError("You need to install ImageMagick to create the gif")

    # create folder is not exists
    png_output_folder = pathlib.Path(png_output_folder)
    png_output_folder.mkdir(parents=True, exist_ok=True)

    # both images must have the same shape
    if warped_cube.shape != raw_cube.shape:
        raise ValueError("The two cubes must have the same shape")

    for index in range(warped_cube.shape[0]):
        print(f"Creating image {index} of {warped_cube.shape[0]}")

        fig, axs = plot_rgb(
            warped_cube=warped_cube,
            raw_cube=raw_cube,
            dates=dates,
            rgb_band=rgb_band,
            intensity_factor=intensity_factor,
            index=index,
        )

        plt.savefig(png_output_folder / ("%04d.png" % index))
        plt.close()
        plt.clf()

    # Use convert to create a gif
    try:
        print("Creating the gif...")
        os.system(
            f"convert -delay {gif_delay} -loop {gif_loop} {png_output_folder}/*.png {gif_output_file}"
        )
    except Exception as e:
        print(e)
        raise ValueError("Error creating the gif")

    return gif_output_file


def plot_profile(
    warped_cube: np.ndarray,
    raw_cube: np.ndarray,
    x_axis: Union[int, slice, None] = None,
    y_axis: Union[int, slice, None] = None,
    rgb_band: Union[int, list, None] = [3, 2, 1],
    intensity_factor: int = 3,
    figsize: Tuple[float] = (10,5),
    **kwargs: dict,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Display the profile of the cube at a given point

    Args:
        warped_cube (np.ndarray): The aligned cube
        raw_cube (np.ndarray): The original cube
        x (Union[int, slice, None], optional): The x coordinate.
            Defaults to None. If None, the middle of the cube is used.
        y (Union[int, slice, None], optional): The y coordinate.
            Defaults to None. If None, the middle of the cube is used.
        rgb_band (Union[int, list, None], optional): The RGB bands to use.
            Defaults to [3, 2, 1].
        intensity_factor (int, optional): The intensity factor, used to scale
            the pixel values. Defaults to 3.
        figsize (tuple(float), optional): figsize parameter to plt.subplots
        **kwargs (dict, optional): Extra parameters to plt.subplots
    """
    t1, c1, h1, w1 = warped_cube.shape
    t2, c2, h2, w2 = raw_cube.shape

    if t1 != t2 or c1 != c2 or h1 != h2 or w1 != w2:
        raise ValueError("The two cubes must have the same shape")

    if x_axis is None:
        if y_axis is None:
            raise ValueError("Both x and y cannot be None")
        x_axis = slice(0, h1)
        axes = (2, 1, 0)

    if y_axis is None:
        if x_axis is None:
            raise ValueError("Both x and y cannot be None")
        y_axis = slice(0, w1)
        axes = (0, 2, 1)

    temporal_profile1 = raw_cube[:, rgb_band, x_axis, y_axis]
    temporal_profile1 = np.transpose(temporal_profile1, axes)
    temporal_profile2 = warped_cube[:, rgb_band, x_axis, y_axis]
    temporal_profile2 = np.transpose(temporal_profile2, axes)

    to_display1 = (temporal_profile1 * intensity_factor).clip(0, 1)
    to_display2 = (temporal_profile2 * intensity_factor).clip(0, 1)

    fig, axs = plt.subplots(1, 2, figsize=figsize, **kwargs)
    axs[0].imshow(to_display1)
    axs[0].set_title("Original Cube")
    axs[0].set_ylabel("Time")
    if isinstance(x_axis, slice):
        axs[0].set_xlabel(f"Y axis - {y_axis}")
    else:
        axs[0].set_xlabel(f"X axis - {x_axis}")
    axs[1].imshow(to_display2)
    axs[1].set_title("Aligned Cube")
    axs[1].set_ylabel("Time")
    if isinstance(x_axis, slice):
        axs[1].set_xlabel(f"Y axis - {y_axis}")
    else:
        axs[1].set_xlabel(f"X axis - {x_axis}")

    return fig, axs


def plot_animation2(
    warped_cube: np.ndarray,
    raw_cube: np.ndarray,
    png_output_folder: Union[str, pathlib.Path],
    gif_output_file: Union[str, pathlib.Path],
    dominant_axis: Literal["x", "y"] = "x",
    rgb_band: Union[int, list, None] = [3, 2, 1],
    intensity_factor: int = 3,
    gif_delay: int = 100,
    gif_loop: int = 0,
) -> pathlib.Path:
    """Create a gif animation from the raw and warped cube
    
    Args:
        warped_cube (np.ndarray): The aligned cube
        raw_cube (np.ndarray): The original cube
        png_output_folder (Union[str, pathlib.Path]): The folder to save the 
            png files.
        gif_output_file (Union[str, pathlib.Path]): The gif file to save.
        dominant_axis (Literal["x", "y"], optional): The dominant axis. Defaults to "x".
        rgb_band (Union[int, list, None], optional): The RGB bands to use.
            Defaults to [3, 2, 1].
        intensity_factor (int, optional): The intensity factor, used to scale
            the pixel values. Defaults to 3.
        gif_delay (int, optional): The delay between the images. Defaults to 20.
        gif_loop (int, optional): The number of loops. Defaults to 0.    
    """
    # check if the system has ImageMagick installed
    if os.system("convert -version") != 0:
        raise ValueError("You need to install ImageMagick to create the gif")

    # create folder is not exists
    png_output_folder = pathlib.Path(png_output_folder)
    png_output_folder.mkdir(parents=True, exist_ok=True)

    # both images must have the same shape
    if warped_cube.shape != raw_cube.shape:
        raise ValueError("The two cubes must have the same shape")

    # if the dominant axis is x
    if dominant_axis == "x":
        range_value = warped_cube.shape[1]
    else:
        range_value = warped_cube.shape[2]

    for index in range(range_value):
        print(f"Creating image {index} of {warped_cube.shape[0]}")
        if dominant_axis == "x":
            fig, axs = plot_profile(
                warped_cube=warped_cube,
                raw_cube=raw_cube,
                x_axis=None,
                y_axis=index,
                rgb_band=rgb_band,
                intensity_factor=intensity_factor,
            )
        else:
            fig, axs = plot_profile(
                warped_cube=warped_cube,
                raw_cube=raw_cube,
                x_axis=index,
                y_axis=None,
                rgb_band=rgb_band,
                intensity_factor=intensity_factor,
            )
        plt.savefig(png_output_folder / ("%04d.png" % index))
        plt.close()
        plt.clf()

    # Use convert to create a gif
    try:
        print("Creating the gif...")
        os.system(
            f"convert -delay {gif_delay} -loop {gif_loop} {png_output_folder}/*.png {gif_output_file}"
        )
    except Exception as e:
        print(e)
        raise ValueError("Error creating the gif")

    return gif_output_file
