import sys, os

# Usage:
#   python build_jupyter.py subfolder/filename.ipynb

jupyter_files_directory = 'jupyter_files'

if __name__ == "__main__":


    # get jupyter notebook file path from command line argument
    notebook_path = str(sys.argv[1])

    # strip folder from file path
    notebook_filename = os.path.basename(notebook_path)

    # path to notebook directory
    notebook_directory = os.path.dirname(notebook_path)

    # splits file extension from base of file name
    filename_components = os.path.splitext(notebook_filename)

    # print('filepath components:')
    # print(filename_components)

    # check if jupyter notebook exists
    if not os.path.exists(notebook_path):
        raise Exception('"' + notebook_path + '" does not exist')

    # check that the file is a jupyter notebook
    if filename_components[1] != '.ipynb':
        raise Exception('"' + notebook_filename + '" is not a jupyter notebook')
    
    # placeholder: nbconvert command (use os.system)
    # https://www.geeksforgeeks.org/python-os-system-method/

    nbconvert_cmd = "jupyter nbconvert --to markdown " + notebook_path

    print(nbconvert_cmd)

    # placeholder: move jupyter images files directory
    # use shutils: https://www.geeksforgeeks.org/python-shutil-move-method/
    print('Moving folder: ' + os.path.join(notebook_directory, filename_components[0]))
    print('To: ' + os.path.join(jupyter_files_directory, os.path.basename(notebook_directory), filename_components[0]))

    # placeholder: fix image filepaths in the .md file
    print('Fixing image filepaths in: ' + filename_components[0] + '.md')

    #print(notebook_path)