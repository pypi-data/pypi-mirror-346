"""TrainLoop Evaluations CLI package."""

import os

# Read version from VERSION file
with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION')) as f:
    __version__ = f.read().strip()
