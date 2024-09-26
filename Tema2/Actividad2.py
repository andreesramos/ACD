from pathlib import Path

class FileManager:
    def write_file(self, file_path, content, mode='w'):
        try:
            with open(file_path, mode) as archivo:
                archivo.write(content)
        except Exception as e:
            print("Error escribiendo el achivo: {e}")

    def read_file(self, file_path, mode='r'):
        try:
            with open(file_path, mode) as archivo:
                content=archivo.read()
                print(content)
        except Exception as e:
            print("Error leyendo el archivo: {e}")

file_manager=FileManager()
file_manager.write_file("24525402.txt", "16/03/2003")
file_manager.read_file("24525402.txt")
