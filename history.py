import os
import json
from datetime import datetime

def generate_operation(source, destination):
    operation = {
        "source": source,
        "destination": destination
    }
    return operation

def save_operations(operations: list):
    id = datetime.now().strftime("%Y%m%d%H%M%S")

    json_operation = {
        "id": id,
        "moves": operations
    }

    history_file = "operation_history.json"

    operation_history = []

    if os.path.isfile(history_file):
        with open(history_file, "r") as file:
            operation_history = json.load(file)

    operation_history.append(json_operation)

    with open(history_file, "w") as file:
        json.dump(operation_history,file,indent=4)

