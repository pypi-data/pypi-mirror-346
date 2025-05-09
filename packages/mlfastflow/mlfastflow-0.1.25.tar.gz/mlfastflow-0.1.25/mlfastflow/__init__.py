"""MLFastFlow - packages for fast dataflow and workflow processing."""

__version__ = "0.1.25"

# Import core components
from mlfastflow.core import Flow

# Import sourcing functionality
import mlfastflow.sourcing as sourcing
from mlfastflow.sourcing import Sourcing

# Import BigQueryClient
import mlfastflow.bigqueryclient as bigqueryclient
from mlfastflow.bigqueryclient import BigQueryClient

# Import utils module (functions accessible via utils.function_name)
import mlfastflow.utils as utils


# uncomment the following line to import utils functions directly
# from mlfastflow.utils import concat_files, profile

# Make these classes and modules available at the package level
__all__ = [
    'Flow',
    'bigqueryclient' # module
    'BigQueryClient', # class

    'sourcing',     # module
    'Sourcing',     # class
    
    'utils',        # module
    # comment out if you don't want to import utils functions directly   
    # 'concat_files',   # function
    # 'profile',        # function
    
    
    
]
