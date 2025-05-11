import importlib.resources
import json

def load_report_type_map():
    # Access the resource from the metadata folder
    try:
        resource_package = __name__  # This refers to the current package/module
        resource_path = importlib.resources.files(resource_package).joinpath('metadata/reportTypeMap.json')

        # Read the JSON file
        with open(resource_path, 'r') as file:
            data = json.load(file)  # Parse JSON content
        return data

    except Exception as e:
        print(f"Error loading reportTypeMap.json: {e}")
        return None

