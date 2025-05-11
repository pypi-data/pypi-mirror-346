# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

import importlib.util
try:
    from importlib import metadata as importlib_metadata
except ImportError:
    import importlib_metadata

def get_package_availability(pkg_name: str) -> bool:
    try:
        top_level = pkg_name.split('.')[0]
        return importlib.util.find_spec(top_level) is not None
    except Exception:
        return False

def get_package_version(pkg_name: str) -> str | None:
    try:
        return importlib_metadata.version(pkg_name)
    except importlib_metadata.PackageNotFoundError:
        return None
