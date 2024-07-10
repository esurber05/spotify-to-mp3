from zipfile import ZipFile
import os, re, time

def create_zip_file(input_path: str, output_path: str):
    """Creates a zip file of an entire directory
    
    Uses zipfile module combined with the os module to "walk" through the 
    provided directory and create a zip file. 

    Args:
        input_path (str): folder to be zipped
        output_path (str): output path of zipped file
    """
    
    with ZipFile(output_path, 'w') as zipObject:
        for folder_name, sub_folders, file_names in os.walk(input_path):
            for file_name in file_names:
                file_path = os.path.join(folder_name, file_name)
                zipObject.write(file_path, os.path.basename(file_path))

def strip_ansi_codes(text: str) -> str:
    """Strips ansi codes from provided text 
    
    Uses re module to strip the ansi codes out of character, 
    in this case used to strip codes from status data emitted from yt_dlp module

    Args:
        text (str): provided text to strip ansi codes

    Returns:
        str: text without ansi codes
    """
    
    ansi_escape = re.compile(r'\x1b\[([0-9;]*[A-Za-z])')
    return ansi_escape.sub('', text)

def delete_old_files(folder_path: str, age_threshold: int = 86400):
    """
    Delete files in the given folder that are older than the age threshold.

    :param folder_path: The path to the folder containing files to delete.
    :param age_threshold: Age threshold in seconds. Files older than this will be deleted.
                          Default is 86400 seconds (1 day).
    """
    
    current_time = time.time()
    
    #Loops through all files in provided path
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            #Deletes file older than one day
            fileAge = current_time - os.path.getmtime(file_path)
            if fileAge > age_threshold:
                print(f"Deleting old file: {file_path}")
                os.remove(file_path)
