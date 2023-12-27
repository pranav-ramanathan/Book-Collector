import subprocess
import os
import os
import subprocess
from icecream import ic

def convert_to_epub(file_path, directory):
    # Check if the file is a .mobi file
    if file_path.endswith('.mobi'):

        # Get the file name without extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Construct the command to convert .mobi to .epub
        command = f'ebook-convert "{file_path}" "{os.path.join(directory, file_name)}.epub"'

        # Execute the command using subprocess
        subprocess.run(command, shell=True)
        ic(f'Converted {file_path} to {file_name}.epub')
        os.remove(file_path)
        return True

    elif file_path.endswith('.azw3'):
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Construct the command to convert .mobi to .epub
        command = f'ebook-convert "{file_path}" "{os.path.join(directory, file_name)}.epub"'

        # Execute the command using subprocess
        subprocess.run(command, shell=True)
        ic(f'Converted {file_path} to {file_name}.epub')
        os.remove(file_path)
        return True
    
    else:
        ic(f'Could not convert {file_path} to .epub')
        return False

def rename_file(file_path, new_name):
    # Get the directory and extension of the file
    directory = os.path.dirname(file_path)
    extension = os.path.splitext(file_path)[1]

    # Construct the new file path with the new name and the original extension
    new_file_path = os.path.join(directory, new_name + extension)

    # Rename the file
    os.rename(file_path, new_file_path)
    ic(f'Renamed {file_path} to {new_file_path}')
    return new_file_path

def move_file(file_path, new_directory):
    # Get the file name
    file_name = os.path.basename(file_path)

    # Construct the new file path
    new_file_path = os.path.join(new_directory, file_name)

    # Move the file
    os.rename(file_path, new_file_path)
    ic(f'Moved {file_path} to {new_file_path}')