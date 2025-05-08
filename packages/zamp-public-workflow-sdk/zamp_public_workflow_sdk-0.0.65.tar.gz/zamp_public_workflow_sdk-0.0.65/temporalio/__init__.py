"""
This package re-exports everything from zamp_temporalio as temporalio.
"""

import sys
from zamp_temporalio import *

# Make sure the package is properly recognized
__name__ = 'temporalio'
__all__ = sys.modules['zamp_temporalio'].__all__ 