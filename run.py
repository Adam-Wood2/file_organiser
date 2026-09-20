import main as m

VERSION = "0.1"



def parse_command(command: str):
    command_parts = command.split(" ")
    match command_parts[0].lower():
        case "exit":
            exit()
        case "target":
            target()
        case "dryrun":
            dryrun()
        case "organise":
            organise()
        case "help":
            show_help()
        case _:
            error()


def run():
    exit = False
    print(f"File Organiser - Version {VERSION}")
    while not exit:
        command = input(">>")
        parse_command(command)
        pass



if __name__ == "__main__":
    run()