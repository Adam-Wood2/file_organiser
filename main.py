import os
import shutil
from configparser import ConfigParser
import history
import logging
from configwriter import generateDefaultConfig
class File:
    def __init__(self, file_name, location):
        self.file_name = file_name
        self.location = location
        self.full_path = os.path.join(self.location, self.file_name)
        self.file_extension = self.__get_file_extension()
        self.file_type = self.__get_file_type()
        self.size = self.get_file_size()
        self.is_ignored = self.file_extension in ignore_lookup
        if not self.is_ignored:
            self.full_destination = os.path.join(self.location, self.__get_file_type())

    #Returns a string with the size of the file in the largest units whilst keeping the digits above 1
    def format_size(self):
        units = ["B","KB","MB","GB"]
        unit_index = 0

        size = self.size
        while size >= 1024 and unit_index < len(units) -1:
            size /= 1024
            unit_index +=1
        return f"{size:.2f} {units[unit_index]}"

    #Rebuilds the file extension after it has been split
    def __get_file_extension(self):
        return "." + self.file_name.split(".")[-1]

    #Checks if the file type is to be ignored. If not, looks up the extension in the lookup dictionary to find the related file type.
    #If the extension is not found in the lookup dictionary, it is set to "Other"
    def __get_file_type(self):
        if self.file_extension in ignore_lookup:
            return None
        elif self.file_extension in extension_lookup:
            return extension_lookup[self.file_extension]
        else:
            return "Other"

    #Returns the file size in bytes    
    def get_file_size(self):
        stats = os.stat(self.full_path)
        size_in_bytes = stats.st_size
        return size_in_bytes


#Draws the progress bar at a specific percentage
def draw_progress_bar(val1, val2):

    progress = int(((val1 / val2)*100) // 2)
    progress_bar = "[" + "\u001b[47m.\u001b[0m"*progress + "."*(50-progress) + "]" + f" {val1}/{val2}"
    #return progress_bar
    if val1 != val2:
        print(progress_bar, end="\r")
    else:
        print(progress_bar)

#Gets the directory from the user and extracts all files and folders from it
def get_directories(dir):
    if not os.path.isdir(dir):
        print("This folder path does not exist")
        raise AttributeError("Non-existent file path")
    else:
        if not os.listdir(dir):
            print("This folder is empty")
            raise ValueError("Empty directory")



    dir_files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    dir_folders = [f for f in os.listdir(dir) if not os.path.isfile(os.path.join(dir, f))]
    return dir_files, dir_folders


#parses the config file to get the types of files and their matching file extensions. Returns a dictionary with this info.
def load_configs():
    logger.info("Loading configurations")
    config = ConfigParser()

    if os.path.exists(os.path.join(os.getcwd(), config_file)):
        logger.info("configuration file found")
        config.read(config_file)
    else:
        logger.info("Configuration file not found")
        raise Exception("No configuration file exists")
    
    filetypes = {}
    for filetype, extensions in config["FILETYPES"].items():
        filetypes[filetype.capitalize()] = [extension.strip() for extension in extensions.split(",")]
    return filetypes

#Generates a lookup dictionary with the format of {extension} : {file type}. This makes future searches much quicker/
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

    logger.info("Beginning directory scan")
    print("Scanning directory...")
    for file_name in dir_files:
        file = File(file_name, dir)
        logger.info(f"File {file_name} found")

        file_destination = file.file_type

        #checks if the filetype will be sorted, whether the folder has already been identified, and whether or not it already exists
        if not file.is_ignored and file_destination not in needed_folders and file_destination not in dir_folders:
            needed_folders.append(file_destination)
            logger.info(f"Identified folder {file_destination} to be created")

        if not file.is_ignored:
            files.append(file)
        current_file_num += 1
        draw_progress_bar(current_file_num,total_files)
    print("Scan complete")
    return files, needed_folders

#Prints to the command line where each file is going to be moved and from where, and what folders need to be created
def dry_run(files, needed_folders):
    print("Files to move:\n")
    for file in files:
        print(file.file_name)
        print(f"    {file.full_path}")
        print(f"    └ {file.destination}")

    print("Folders to be created:")
    print(" "+"\n ".join(needed_folders))
    print(f"\n{len(files)} files would be moved.")

#Checks if any folders need to be created, and if so creates them
def create_folders(needed_folders, dir):
    if len(needed_folders) == 0:
        raise Exception("No folders created")
    for folder in needed_folders:
        logger.info(f"Creating folder {folder}")
        os.mkdir(os.path.join(dir, folder))
        logger.info(f"Created folder {folder}")

#Moves an individual file to its destination, and then generates an operation history.
def move_file(file):
    logger.info(f"Moving file {file.file_name}")
    shutil.move(file.full_path, file.full_destination)
    logger.info(f"Completed move {file.full_path} to {file.full_destination}")
    operation = history.generate_operation(file.full_path, file.full_destination)
    return operation

#Creates all the missing folders, then moves all files into their configured folder. It then calls the save_operations function to save it to a json file.
def organise(files, needed_folders, dir):
    logger.info("beginning organisation")

    logger.info("Creating missing folders")
    try:
        create_folders(needed_folders,dir)
    except Exception as e:
        logger.warning(f"Issue creating missing folders. Issue: {e}")
    else:
        logger.info("Missing folders created")

    operations = []

    for file in files:
        try:
            operation = move_file(file)
        except Exception as e:
            logger.warning(f"File {file.full_path} not moved. Error: {e}")
        else:
            operations.append(operation)
            logger.info("finished organisng")

    logger.info("saving operation to json file")

    try:
        history.save_operations(operations)
    except Exception as e:
        logger.info(f"error encountered saving operations to json file. Error: {e}")
    else:
        logger.info("operation saved to json file")


def main():
    
    logger.info("Test")
    
    dir, dir_files, dir_folders = get_directories()
    test = ["Images", "Videos"]
    
    files, needed_folders = scan_dir(dir, dir_files, dir_folders)
    dry_run(files,needed_folders)
    #input("")
    #organise(files,needed_folders,dir)
    
if __name__ == "__main__":
    main()


#Creates logger and configures it, example of logger format: "[INFO] 2026-06-20 12:30:35"
logger = logging.getLogger("FILE_ORGANISER")
logging.basicConfig(filename="file_organsier.log", 
                        level=logging.INFO, 
                        format="[%(levelname)s] %(asctime)s %(message)s", 
                        datefmt="%Y-%m-%d %H:%M:%S")
#Attempts to load the configuration file. If it doesnt exist, a default configuration file is created.
config_file = "config.ini"
try:
    folders_config = load_configs()
except Exception as e:
    if "No configuration file exists" in str(e):
        logger.warning("No configuration file found. Generating new configuration file")
        generateDefaultConfig()
        logger.info("Default configuration file generated.")
        folders_config = load_configs()

extension_lookup, ignore_lookup = generate_lookup(folders_config)


#C:\Users\Adam\OneDrive\Documents\Programs\Test Folder