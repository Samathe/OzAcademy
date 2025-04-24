import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the JSON file
json_path = os.path.join(script_dir, "data_json.json")
# Open the file using the full path
r = open(json_path, "r", encoding="utf-8")

print(r.read(20))