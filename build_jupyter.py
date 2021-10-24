import sys, os, re, shutil

# Usage:
#   python build_jupyter.py subfolder/filename.ipynb

# Important: do not include any '/' in this variable
jupyter_files_directory = 'jupyter_files'

# https://stackoverflow.com/questions/11944978/call-functions-from-re-sub
# text = "![png](sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_15_1.png)"
# re.sub("!\[png\]\(([\w/\.]+)\)",'\\1', text)


def fix_image_paths(text, image_dir):
    """
    Fixes the image paths in text (string) by adding 
    in the path to the image_dir (string)

    Example usage:

        fix_image_paths("![png](sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_15_1.png)", "/jupyter_files")

    Output:
        '![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_15_1.png)'

    """
    
    # Edits markdown references for PNG images to point to the right file location
    fixed_text = re.sub("!\[png\]\(([\w/\.]+)\)", 
      lambda match: '![png]({0})'.format(os.path.join('/' + image_dir, match.group(1))), text)

    return(fixed_text)


def main(test = False):
    """
    if test == True then no files will be modified
    """
    # get jupyter notebook file path from command line argument
    notebook_path = str(sys.argv[1])

    # strip folder from file path
    notebook_filename = os.path.basename(notebook_path)

    # path to notebook directory
    notebook_directory = os.path.dirname(notebook_path)

    # splits file extension from base of file name
    filename_components = os.path.splitext(notebook_filename)

    md_file_path = os.path.join(notebook_directory, filename_components[0] + '.md')

    # print('filepath components:')
    # print(filename_components)

    # check if jupyter notebook exists
    if not os.path.exists(notebook_path):
        raise Exception('"' + notebook_path + '" does not exist')

    # check that the file is a jupyter notebook
    if filename_components[1] != '.ipynb':
        raise Exception('"' + notebook_filename + '" is not a jupyter notebook')
    
    # nbconvert -------------------------------------------------------------------

    nbconvert_cmd = "jupyter nbconvert --to markdown " + notebook_path

    if test == False:
        os.system(nbconvert_cmd)

    # Move image file directory ---------------------------------------------------
    orig_image_dir_path = os.path.join(notebook_directory, filename_components[0] + "_files")
    final_image_dir_path = os.path.join(jupyter_files_directory, os.path.basename(notebook_directory), filename_components[0] + "_files")

    print('Moving folder: ' + orig_image_dir_path)
    print('To: ' + final_image_dir_path)

    if test == False:
        shutil.move(orig_image_dir_path, final_image_dir_path) 

    # Fix image file paths --------------------------------------------------------
    print('Fixing image filepaths in: ' + md_file_path)

    if test == False:
        # Read content of MD file
        with open(md_file_path, 'r') as file:
            orig_md_content = file.read()

        # Fix all the image file paths
        fixed_md_content = fix_image_paths(orig_md_content, jupyter_files_directory)
        
        # Overwrite the file with the fixed content
        with open(md_file_path, 'w') as file:
            file.write(fixed_md_content)

if __name__ == "__main__":
    main(test = False)
