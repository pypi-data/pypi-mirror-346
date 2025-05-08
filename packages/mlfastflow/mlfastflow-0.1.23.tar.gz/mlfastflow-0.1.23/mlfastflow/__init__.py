"""MLFastFlow - packages for fast dataflow and workflow processing."""

__version__ = "0.1.23"

# Import core components
from mlfastflow.core import Flow

# Import sourcing functionality
from mlfastflow.sourcing import Sourcing

# Import BigQueryClient
from mlfastflow.bigqueryclient import BigQueryClient

# Import utils
from mlfastflow.utils import concat_files

# Make these classes available at the package level
__all__ = ['Flow', 'Sourcing', 'BigQueryClient', 'concat_files']
