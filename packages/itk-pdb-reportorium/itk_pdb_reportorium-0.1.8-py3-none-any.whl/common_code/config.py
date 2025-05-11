import importlib.resources
import json
import os

def load_report_type_map():
    try:
        resource_package = __name__  # This refers to the current package/module
        resource_path = importlib.resources.files(resource_package).joinpath('metadata/reportTypeMap.json')

        # Check if the file exists
        if not os.path.exists(resource_path):
            print(f"Error: The file {resource_path} does not exist.")
            return None

        # Read the JSON file
        with open(resource_path, 'r') as file:
            data = json.load(file)  # Parse JSON content
        return data

    except Exception as e:
        print(f"Error loading reportTypeMap.json: {e}")
        return None

# Attempt to load the reportTypeMap.json data
data = load_report_type_map()

if data is None:
    print("Failed to load reportTypeMap.json data.")
else:
    try:
        # Process the data as needed
        general_data = next((item for item in data if "general" in item), {})
        reportTypeMap = general_data.get("general", {}).get("reportTypeMap", {})
        general_subtypes = general_data.get("general", {}).get("subtypes", [])

        # Continue with further processing as required...
    except Exception as e:
        print(f"Error processing reportTypeMap.json: {e}")
