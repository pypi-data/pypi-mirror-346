import sys
import importlib
import logging

logger = logging.getLogger(__name__)

"""
Registers the bindiings that should be used by golem_py. Make sure this is called before any other golem_py import.
"""


def register_bindings(world_name: str) -> None:
    # componentize-py generates bindings under a world name. Import them here and make them available under a well known name.

    def try_load(module: str) -> None:
        try:
            sys.modules[f"golem_py_bindings.bindings.{module}"] = (
                importlib.import_module(f".{module}", world_name)
            )
        except ImportError:
            logger.warning(
                f"Binding module {module} is not available. Functionality relying on it will not work."
            )
            pass

    def try_load_all(modules: list[str]) -> None:
        for module in modules:
            try_load(module)

    try_load_all(
        [
            "exports",
            "imports",
            "imports.host",
            "imports.durability",
            "imports.oplog",
            "imports.golem_rpc_typestypes",
        ]
    )
