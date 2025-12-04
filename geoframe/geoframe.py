from .geojson import GeoJSON
from .geoparquet import GeoParquet
from .geoarrow import GeoArrow
import polars as pl
import polars_extensions as plx


class GeoFrame:
    def __init__(self
                 ,df: pl.DataFrame
                 ,coordinates_column: str = 'geometry'
                 ,wkt_column: str = None
                 ,raw: GeoJSON|GeoParquet|GeoArrow= None
                   ,read_format: str = None
                 ,crs: str = None):
        # if geometry_column not in df.columns:
        #     raise ValueError(f"'{geometry_column}' not found in DataFrame columns")
        self.df = df
        self.coordinates_column = coordinates_column
        self.crs = crs  # e.g., "EPSG:4326"
        self.raw = raw  # Store the raw data if available
        self.read_format = read_format  # Store the format used for reading (e.g.,

    def __getattr__(self, item):
        # Delegate all unknown attribute access to the underlying Polars DataFrame
        return getattr(self.df, item)

    def __repr__(self):
        crs_str = f" (CRS: {self.crs})" if self.crs else ""
        return f"GeoFrame with geometry column '{self.coordinates_column}'{crs_str}:\n{self.df}"

    # Example method
    def to_wkt(self):
        return self.df.select(self.geometry_column).to_series().to_list()

    # Optional: set a new CRS
    def set_crs(self, new_crs: str):
        self.crs = new_crs
    

    def with_columns(self, *args, **kwargs):
        new_df = self.df.with_columns(*args, **kwargs)
        return GeoFrame(
            df=new_df,
            coordinates_column=self.coordinates_column,
            wkt_column=getattr(self, 'wkt_column', None),
            raw=self.raw,
            read_format=self.read_format,
            crs=self.crs
        )

    # Optionally, override other methods similarly:
    def select(self, *args, **kwargs):
        new_df = self.df.select(*args, **kwargs)
        return GeoFrame(
            df=new_df,
            coordinates_column=self.coordinates_column,
            wkt_column=getattr(self, 'wkt_column', None),
            raw=self.raw,
            read_format=self.read_format,
            crs=self.crs
        )
