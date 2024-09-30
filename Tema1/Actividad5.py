import json

class JSONFileHandler:
    def write_json(self, file_path):
        try:
            d={"DNI": 24525402, "Fecha de nacimiento": "16/03/2003"};
            with open(file_path, 'w') as f:
                json.dump(d, f)
        except Exception as e:
            print("Error escribiendo JSON: {e}");

    def read_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print("Error escribiendo JSON: {e}");


json_handler=JSONFileHandler()
json_handler.write_json('data.json')
data=json_handler.read_json('data.json')
print(data)