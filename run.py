import main as m

VERSION = "0.1"


def get_location(command: str):

    start_index = command.index('"')
    end_index = start_index + 1
    for i in command[start_index + 1:]:
        if i == '"':
            break
        end_index += 1
    print(command[start_index + 1:end_index])
    return command[start_index + 1:end_index]


def target(location):
    dir_files, dir_folders = m.get_directories(location)

    files, needed_foleders = m.scan_dir(location, dir_files, dir_folders)
    return "target", files, needed_foleders

def parse_command(command: str):
    keyword = command.split(" ")[0].lower()
    match keyword:
        case "exit":
            print("Exiting File Organiser")
            exit()
        case "target":
            try:
                location = get_location(command)
            except ValueError as e:
                return "error", e, "directory path must be enclosed in quotation marks (\"C:\\path\")"
            output = target(location)
        case "dryrun":
            dryrun()
        case "organise":
            organise()
        case "help":
            show_help()
        case "config":
            set_config()
        case _:
            error()

    return output

def run():
    exit = False
    print(f"File Organiser - Version {VERSION}")
    while not exit:
        command = input(">>")
        output = parse_command(command)
        print(output)
        input("")



if __name__ == "__main__":
    run()

#C:\Users\Adam\OneDrive\Documents\Programs\Test Folder