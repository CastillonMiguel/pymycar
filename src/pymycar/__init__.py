# pymycar/__init__.py

__version__ = "0.0.3"
__author__ = "Miguel Castillón"
__email__ = "miguel.research@pm.me"
__license__ = "MIT"
__description__ = "pyMyCar: An Open-Source Framework for Vehicle Dynamics simulations"
__url__ = "https://github.com/CastillonMiguel/pymycar"

# Import submodules to be included in the package namespace
from .Cad import *
from .Logger import *
from .MotorCycleKinematic import *
from .CarKinematic import *
from .Vehicle import *
from .VerticalModels import *
from .files import *

# Optionally, you can specify which symbols to export when using 'from
# pymycar import *'
__all__ = [
    'Cad',
    'Logger',
    'MotorCycleKinematic',
    'CarKinematic',
    'Vehicle',
    'VerticalModels',
    'files',
]
