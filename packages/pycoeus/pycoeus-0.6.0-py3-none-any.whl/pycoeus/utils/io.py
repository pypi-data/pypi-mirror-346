import logging
from pathlib import Path
from typing import Any, Union

from rioxarray import rioxarray

from pycoeus.logging_config import log_array

logger = logging.getLogger(__name__)


def read_geotiff(raster_path: Path, **dask_kwargs) -> rioxarray.raster_array:
    raster = rioxarray.open_rasterio(raster_path, **dask_kwargs)
    log_array(raster.data, logger, array_name=str(raster_path))
    return raster


def save_tiff(prediction_raster: rioxarray.raster_array, output_path: Union[Path, str]) -> None:
    prediction_raster.rio.to_raster(output_path)
