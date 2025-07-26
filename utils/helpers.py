
# Take a json file, convert it to a python dictionary, add a new key-value pair, and convert it back to json format.
import json
import os


def create_metadata(file_id, value):
    """
    Update a JSON file by adding a new key-value pair.
    
    :param file_path: Path to the JSON file.
    :param file_name: File name to add or update in the JSON file.
    :param value: Value to set for the specified key.
    :return: Updated JSON data as a string.
    """
    file_path = 'storage/metadata.json'
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        data[str(file_id)] = value
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        return json.dumps(data, indent=4)
    
    except Exception as e:
        raise ValueError(f"Error updating the metadata file: {str(e)}")
    
def list_metadata():
    """
    List all key-value pairs in the metadata JSON file.
    
    :return: Dictionary containing all key-value pairs in the metadata file.
    """
    file_path = 'storage/metadata.json'
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Metadata file not found: {file_path}")
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        return data
    
    except Exception as e:
        raise ValueError(f"Error listing metadata: {str(e)}")

def get_metadata(file_name):
    """
    Get metadata for a specific file from the metadata JSON file.
    
    :param file_name: Name of the file to retrieve metadata for.
    :return: Metadata dictionary for the specified file.
    """
    metadata = list_metadata()
    return metadata.get(file_name, None)

def get_current_time():
    """
    Get the current time in a human-readable format.
    
    :return: Current time as a string.
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def delete_metadata(file_name):
    """
    Delete a key-value pair from the metadata JSON file.
    
    :param file_name: File name to delete from the metadata file.
    :return: Updated JSON data as a string.
    """
    file_path = 'storage/metadata.json'
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        if file_name in data:
            del data[file_name]
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        return json.dumps(data, indent=4)
    
    except Exception as e:
        raise ValueError(f"Error deleting metadata: {str(e)}")