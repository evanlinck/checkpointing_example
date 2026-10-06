# Make `import htcondor_ckpt...` work when running pytest from the repository root.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
