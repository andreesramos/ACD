import csv
import json

class FileConverter:
    def json_to_csv(self, json_file, csv_file):
        try:
            with open(json_file, 'r') as f:
                data=json.load(f)

            headers = data[0].keys()
            
            with open(csv_file, 'w') as f:
                writer=csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()

                for row in data:
                    writer.writerow(row)
                
            print(f'Conversión de {csv_file} a {json_file} completada.')
        except Exception as e:
            print(f"Error de conversion: {e}");

converter=FileConverter()
converter.json_to_csv('data.json', 'data.csv')
