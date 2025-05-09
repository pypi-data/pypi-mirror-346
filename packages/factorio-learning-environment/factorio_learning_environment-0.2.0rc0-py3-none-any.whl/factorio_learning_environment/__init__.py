# factorio_learning_environment package
import tomli
import sys
import importlib.util
import os

__version__ = "0.2.0rc"

# First, create empty module objects for all of our submodules
# This prevents import errors when modules try to import each other
for name in ['env', 'agents', 'server', 'eval', 'cluster']:
    module_name = f'factorio_learning_environment.{name}'
    if module_name not in sys.modules:
        # Create empty module to avoid circular imports
        spec = importlib.util.find_spec(module_name)
        if spec:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
    
    # Create alias in global namespace immediately
    sys.modules[name] = sys.modules[f'factorio_learning_environment.{name}']

# Re-export important classes and functions at the top level
try:
    from .env.src.instance import FactorioInstance
    from .env.src import entities, game_types, namespace

    sys.modules['factorio_learning_environment.entities'] = entities
    sys.modules['factorio_learning_environment.game_types'] = game_types
    sys.modules['factorio_learning_environment.namespace'] = namespace

    __all__ = [
        # Modules
        'env', 'agents', 'server', 'eval', 'cluster', 'entities', 'game_types', 'namespace',
        # Classes and functions
        'FactorioInstance',
    ]
except ImportError:
    # Allow the package to import even if some modules are missing (during build)
    pass
