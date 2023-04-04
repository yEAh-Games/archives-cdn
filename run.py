import os
import shutil

# Get the current directory and the path to index.py
current_dir = os.getcwd()
index_py_path = os.path.join(current_dir, 'index.py')

# Loop through all subdirectories in the current directory
for root, dirs, files in os.walk(current_dir, topdown=False):
    # Copy index.py to each subdirectory
    for subdir in dirs:
        subdir_path = os.path.join(root, subdir)
        index_copy_path = os.path.join(subdir_path, 'index.py')
        shutil.copy2(index_py_path, index_copy_path)

        # Run index.py in the subdirectory
        os.chdir(subdir_path)
        os.system(f'python index.py')
        os.chdir(current_dir)

        # Remove the copied index.py file
        os.remove(index_copy_path)
