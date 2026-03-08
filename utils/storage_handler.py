import json
import os



def load_from_json(filename):

    file_path = os.path.join("data", f"{filename}.json")
    
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            flattened = []
            for item in data:
                if isinstance(item, list):
                    flattened.extend(item)
                else:
                    flattened.append(item)
            return flattened
        except json.JSONDecodeError:
            return []


def save_to_json(data, filename):
    folder = "data"
    file_path = os.path.join(folder, f"{filename}.json")

    if not os.path.exists(folder):
        os.makedirs(folder)

    existing_data = load_from_json(filename)

    if isinstance(data, list):
        existing_data.extend(data)
    else:
        existing_data.append(data)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

def overwrite_patients_file(updated_list, category):  

    file_path = os.path.join("data", f"{category}.json")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(updated_list, f, indent=4)
    except Exception as e:
        print(f"Error while overwriting {category}: {e}")