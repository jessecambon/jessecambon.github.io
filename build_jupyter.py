#!/usr/bin/env python
"""
Author: Jesse Cambon
Description: 
    A script for converting a jupyter notebook (.ipynb) into a Markdown (.md) file that is
    ready for use on a Jekyll blog. nbconvert is used for the conversion, image files are moved,
    and image links within the markdown are adjusted accordingly.
Usage:
    python build_jupyter.py path/to/notebook.ipynb

---------------------


Manual Steps that this Script Replaces:

- Convert the jupyter notebook to markdown using nbconvert with this terminal command: 

`jupyter nbconvert --to markdown <filename.ipynb>`. 

This creates a markdown (.md) file and a folder next to it (<filenane_files>) that will contain all images from the notebook.
```

- Move the folder `<filename_files>` to [jupyter_files](jupyter_files) 
this is where the notebook images were saved by nbconvert).

- Open the Markdown (`.md`) file that was created by nbconvert 
(in the same directory as the jupyter notebook) and modify all image paths to refer to the correct folder (given where we moved the image folder to). The image references should begin with `![png]`. For example you would want to change this image path:

`![png](sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_15_1.png)`

To this:

`![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_15_1.png)`

"""

import sys, os, re, shutil, argparse

# Usage:
#   python build_jupyter.py path/to/notebook.ipynb

# Important: do not include any '/' in this variable
jupyter_files_directory = 'jupyter_files'

# https://stackoverflow.com/questions/11944978/call-functions-from-re-sub
# text = "![png](sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_15_1.png)"
# re.sub("!\[png\]\(([\w/\.]+)\)",'\\1', text)


def fix_image_paths(text, image_dir):
    """
    Adjusts the image paths in markdown content with the alternative text "png" to point to the correct
    image directory

    Args:
        text (str): text which may contain markdown image references (ie. ![png](path/to/image.png))
        image_dir (str): the path to where we put our image files 

    Example usage:
        fix_image_paths("![png](sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_15_1.png)", "jupyter_files")

    Output:
        '![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_15_1.png)'
    """
    
    # Edits markdown references for PNG images to point to the right file location
    fixed_text = re.sub("!\[png\]\(([\w/\.\-]+)\)", 
      lambda match: '![png]({0})'.format(os.path.join('/' + image_dir, match.group(1))), text)

    return(fixed_text)


def main(notebook_path, test):
    """
    if test == True then no files will be modified
    """
    if test:
        print("Testing mode! No files will be modified.")

    # get jupyter notebook file path from command line argument
    nbconvert_cmd = "jupyter nbconvert --to markdown " + notebook_path

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
    if len(notebook_path) == 0:
        raise Exception("Notebook path not specified")

    if not os.path.exists(notebook_path):
        raise Exception('"' + notebook_path + '" does not exist')

    # check that the file is a jupyter notebook
    if filename_components[1] != '.ipynb':
        raise Exception('"' + notebook_filename + '" is not a jupyter notebook')
    
    # nbconvert (converts noteook to markdown) -----------------------------------------------
    if test == False:
        os.system(nbconvert_cmd)
    else:
        print("\nNbconvert command to run:")
        print(nbconvert_cmd)
        print("\n")

    # Move image file directory if it exists ---------------------------------------------------
    orig_image_dir_path = os.path.abspath(os.path.join(notebook_directory, filename_components[0] + "_files"))

    # check if image folder exists (if you don't have any charts or graphs that created an image then it won't exist)
    if not os.path.exists(orig_image_dir_path):
        print('Image folder "' + notebook_path + '" does not exist')
        print("This is expected if your notebook does not contain graphs that would generate an image files.")
    else:
        # If the image folder does exist then we need to move it and fix the image references in the markdown file
        final_image_dir_path = os.path.abspath(os.path.join(jupyter_files_directory, filename_components[0] + "_files"))

        print('Moving folder: ' + orig_image_dir_path)
        print('To: ' + final_image_dir_path)

        # remove the destination image folder if it exists already
        if os.path.exists(final_image_dir_path):
            shutil.rmtree(final_image_dir_path) 

        if test == False:
            shutil.move(orig_image_dir_path, final_image_dir_path)

        # Fix image file paths  -------------------------------------------------------------------------------------
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
    parser = argparse.ArgumentParser()
    parser.add_argument('notebook_path', help="path to jupyter notebook")
    parser.add_argument('--test', action='store_true', 
    help="enables testing model (no files will be modified)")
    args = parser.parse_args()

    main(notebook_path = args.notebook_path, test = args.test)
