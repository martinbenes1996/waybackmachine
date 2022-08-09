
import sys
import unittest

sys.path.append(".")

# === unit tests ===
# from test_init import *
from test_browse import TestBrowse
# ==================


# logging
if __name__ == "__main__":
    import logging
    logging.basicConfig(level = logging.INFO)

# run unittests
if __name__ == "__main__":
    unittest.main()