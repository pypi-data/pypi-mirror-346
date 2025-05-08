from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from liquid_earth_sdk.api.le_api import (
    upload_mesh_to_existing_space,
    upload_mesh_to_new_space,
    get_available_projects,
    get_deep_link
)
# Version.

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # For Python <3.8, fallback
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("subsurface")  # Use package name
except ImportError:
    # If it was not installed, then we don't know the version. We could throw a
    # warning here, but this case *should* be rare. subsurface should be
    # installed properly!
    __version__ = 'unknown-'+datetime.today().strftime('%Y%m%d')
