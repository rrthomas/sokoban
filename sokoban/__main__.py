"""Sokoban: Main module.

© Reuben Thomas <rrt@sc3d.org> 2024
Released under the GPL version 3, or (at your option) any later version.
"""

import re
import sys

from sokoban import main


sys.argv[0] = re.sub(r"__main__.py$", "sokoban", sys.argv[0])
main()
