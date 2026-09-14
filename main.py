import os
import shutil
from configparser import ConfigParser
import history
#C:\Users\Adam\OneDrive\Documents\Programs\Test Folder
class File:
    def __init__(self, file_name, location):
        self.file_name = file_name
        self.location = location
        self.full_path = os.path.join(self.location, self.file_name)
        self.file_extension = self.__get_file_extension()
        self.file_type = self.__get_file_type()
        self.size = self.get_file_size()
        self.is_ignored = self.file_extension in ignore_lookup
        self.destination = self.get_destination()
        if not self.is_ignored:
            self.full_destination = os.path.join(self.location, self.destination)
    
    def format_size(self):
        units = ["B","KB","MB","GB"]
        unit_index = 0

        size = self.size
        while size >= 1024 and unit_index < len(units) -1:
            size /= 1024
            unit_index +=1
        return f"{size:.2f} {units[unit_index]}"

    def __get_file_extension(self):
        return "." + self.file_name.split(".")[-1]

    def __get_file_type(self):
        if self.file_extension in ignore_lookup:
            return self.file_extension
        elif self.file_extension in extension_lookup:
            return extension_lookup[self.file_extension]
        else:
            return "Other"
        
    def get_file_size(self):
        stats = os.stat(self.full_path)
        size = stats.st_size
        return size

    def get_destination(self):
        if self.file_extension in ignore_lookup:
            return "N/A"
        elif self.file_extension in extension_lookup:
            return extension_lookup[self.file_extension]
        else:
            return "Other"


def draw_progress_bar(val1, val2):

    progress = int(((val1 / val2)*100) // 2)
    progress_bar = "[" + "\u001b[47m.\u001b[0m"*progress + "."*(50-progress) + "]" + f" {val1}/{val2}"
    #return progress_bar
    if val1 != val2:
        print(progress_bar, end="\r")
    else:
        print(progress_bar)

#Gets the directory from the user and extracts all files and folders from it
def get_directories():
    while True:
        dir = input("Input the path for the file to sort: ")
        if not os.path.isdir(dir):
            print("This folder path does not exist")
        else:
            if not os.listdir(dir):
                print("This folder is empty")
            else:
                break


    dir_files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    dir_folders = [f for f in os.listdir(dir) if not os.path.isfile(os.path.join(dir, f))]
    return dir, dir_files, dir_folders


#parses the config file to get the types of files and their matching file extensions. Returns a dictionary with this info.
def load_configs():
    config = ConfigParser()
    config.read("config.ini")
    filetypes = {}
    for filetype, extensions in config["FILETYPES"].items():
        filetypes[filetype.capitalize()] = [extension.strip() for extension in extensions.split(",")]
    return filetypes


def generate_lookup(folders_config):
    extension_lookup = {}
    ignore_lookup = []
    for file_type, extensions in folders_config.items():
        for extension in extensions:
            if file_type != "Ignore":
                extension_lookup[extension] = file_type
            else:
                ignore_lookup.append(extension)
    return extension_lookup, ignore_lookup

#Scans through all directories in the given location to get all the files within. Returns a list of all existing files
#and of which folders will be needed.
def scan_dir(dir, dir_files, dir_folders):

    needed_folders = []
    files = []
    total_files = len(dir_files)
    current_file_num = 0
    print("Scanning directory...")
    for file_name in dir_files:
        file = File(file_name, dir)

        file_destination = file.get_destination()

        if not file.is_ignored and file_destination not in needed_folders and file_destination not in dir_folders:
            needed_folders.append(file_destination)

        if not file.is_ignored:
            files.append(file)
        current_file_num += 1
        draw_progress_bar(current_file_num,total_files)
    print("Scan complete")
    return files, needed_folders

def dry_run(files, needed_folders):
    print("Files to move:\n")
    for file in files:
        print(file.file_name)
        print(f"    {file.full_path}")
        print(f"    └ {file.destination}")

    print("Folders to be created:")
    print(" "+"\n ".join(needed_folders))
    print(f"\n{len(files)} files would be moved.")


def create_folders(needed_folders, dir):
    for folder in needed_folders:
        os.mkdir(os.path.join(dir, folder))

def move_file(file):
    shutil.move(file.full_path, file)

def main():
    dir, dir_files, dir_folders = get_directories()
    test = ["Images", "Videos"]

    files, needed_folders = scan_dir(dir, dir_files, dir_folders)
    dry_run(files,needed_folders)
    

folders_config = load_configs()
extension_lookup, ignore_lookup = generate_lookup(folders_config)
main()
