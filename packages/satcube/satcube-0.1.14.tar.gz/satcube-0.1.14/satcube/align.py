from __future__ import annotations

import pathlib
from typing import List, Tuple
import pickle

import numpy as np
import rasterio
import xarray as xr
from affine import Affine

import satalign as sat


def align(
    input_dir: str | pathlib.Path,
    output_dir: str | pathlib.Path,
    *,
    channel: str = "mean",
    crop_center: int = 128,
    num_threads: int = 2,
    save_tiffs: bool = True,
) -> Tuple[xr.DataArray, List[np.ndarray]]:
    """Align all masked Sentinel‑2 tiles found in *input_dir*.

    Parameters
    ----------
    input_dir
        Directory containing masked Sentinel‑2 *TIFF* tiles produced by the
        previous preprocessing stage.
    output_dir
        Directory where the alignment artefacts (``datacube.pickle``) and, if
        requested, one aligned *GeoTIFF* per date will be written.
    channel
        Datacube band used by the *PCC* model for correlation.  ``"mean"`` is
        recommended because it carries fewer noise artefacts.
    crop_center
        Half‑size (in pixels) of the square window extracted around the scene
        centre that is fed to the correlation engine.
    num_threads
        Number of CPU threads for the multi‑core phase‑correlation run.
    save_tiffs
        If *True* (default) the aligned datacube is exported to tiled *COGs* via
        :func:`save_aligned_cube_to_tiffs`.
    pickle_datacube
        If *True* (default) the raw (unaligned) datacube is pickled to
        ``datacube.pickle`` inside *output_dir* for reproducibility/debugging.

    Returns
    -------
    aligned_cube, warp_matrices
        *aligned_cube* is the spatially aligned datacube as an
        :class:`xarray.DataArray`; *warp_matrices* is the list of 3 × 3 affine
        homography matrices (one per time step) returned by the
        :pyclass:`~satalign.PCC` engine.
    """
    input_path = pathlib.Path(input_dir).expanduser().resolve()
    output_path = pathlib.Path(output_dir).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    # ── 1. Build datacube ────────────────────────────────────────────
    da =  sat.utils.create_array(input_path)

    # ── 2. Select reference slice (highest cloud‑score CDF) ───────────
    da_sorted = da.sortby("cs_cdf", ascending=False)
    ref_slice = da_sorted.isel(time=0)
    reference = ref_slice.where((ref_slice != 0) & (ref_slice != 65535))

    # ── 3. Instantiate and run PCC model ─────────────────────────────
    pcc_model = sat.PCC(
        datacube=da,
        reference=reference,
        channel=channel,
        crop_center=crop_center,
        num_threads=num_threads,
    )
    aligned_cube, warp_matrices = pcc_model.run_multicore()

    # ── 4. Optionally export as Cloud‑Optimised GeoTIFFs ────────────
    if save_tiffs:
        save_aligned_cube_to_tiffs(aligned_cube, output_path)

    return aligned_cube, warp_matrices


def save_aligned_cube_to_tiffs(
    aligned_cube: xr.DataArray,
    out_dir: str | pathlib.Path,
    *,
    block_size: int = 128,
) -> None:
    """Write each time slice of *aligned_cube* to an individual tiled COG.

    The filenames follow the pattern ``YYYY‑MM‑DD.tif``.

    Parameters
    ----------
    aligned_cube
        Datacube returned by :func:`align_datacube`.
    out_dir
        Target directory; it will be created if it does not exist.
    block_size
        Internal tile size (*rasterio* ``blockxsize`` and ``blockysize``).
    """
    out_dir_path = pathlib.Path(out_dir).expanduser().resolve()
    out_dir_path.mkdir(parents=True, exist_ok=True)

    # ── 1. Build affine transform from x/y coordinate vectors ────────
    x_vals = aligned_cube.x.values
    y_vals = aligned_cube.y.values
    x_res = float(x_vals[1] - x_vals[0])  # positive (east)
    y_res = float(y_vals[1] - y_vals[0])  # negative (north‑up)
    transform = (
        Affine.translation(x_vals[0] - x_res / 2.0, y_vals[0] - y_res / 2.0)
        * Affine.scale(x_res, y_res)
    )

    # ── 2. Retrieve CRS from datacube attributes ────────────────────
    attrs = aligned_cube.attrs
    crs: str | None = attrs.get("crs_wkt")
    if crs is None and "crs_epsg" in attrs:
        crs = f"EPSG:{int(attrs['crs_epsg'])}"

    # ── 3. Loop over acquisition dates and write GeoTIFFs ────────────
    for t in aligned_cube.time.values:
        date_str = str(t)[:10]  # YYYY‑MM‑DD
        da_t = aligned_cube.sel(time=t)

        # Ensure (band, y, x) memory layout for rasterio
        data = da_t.transpose("band", "y", "x").values

        profile = {
            "driver": da_t.attrs.get("driver", "GTiff"),
            "height": da_t.sizes["y"],
            "width": da_t.sizes["x"],
            "count": da_t.sizes["band"],
            "dtype": str(da_t.dtype),
            "transform": transform,
            "crs": crs,
            "nodata": int(getattr(da_t, "nodata", 0)),
            "tiled": True,
            "blockxsize": block_size,
            "blockysize": block_size,
            "interleave": "band",
        }

        outfile = out_dir_path / f"{date_str}.tif"
        with rasterio.open(outfile, "w", **profile) as dst:
            dst.write(data)
