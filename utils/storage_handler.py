import json
import os

def save_to_json(data, filename):  
    
    folder = "data"
    file_path = os.path.join(folder, f"{filename}.json")

    if not os.path.exists(folder):
        os.makedirs(folder)

    existing_data = load_from_json(filename)
    
    existing_data.append(data)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

def load_from_json(filename):

    file_path = os.path.join("data", f"{filename}.json")
    
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
        
def overwrite_patients_file(updated_list, category):  

    file_path = os.path.join("data", f"{category}.json")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(updated_list, f, indent=4)
    except Exception as e:
        print(f"Error while overwriting {category}: {e}")