import os
import sys
app_root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(app_root_path)
print(f'Root path is set to {app_root_path}')
