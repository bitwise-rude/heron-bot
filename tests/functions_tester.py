import sys
import os

c_dir = os.path.dirname(os.path.abspath(__file__))
p_dir = os.path.dirname(c_dir)

sys.path.append(p_dir)

from functions import *

print("The current Date+Time: ", get_now())
print(get_all_commands())
