import win32com.client # Para leer .doc → ´pip install pywin32´
import os
import time

inicio = time.time() # Inicio de la ejecución
print("\n-------------------------------------- Iniciando Lectura --------------------------------------")

ruta_actual = os.path.dirname(os.path.abspath(__file__)) # Directorio actual
files = os.listdir(ruta_actual + "\\files") # Ruta de los archivos

for index, file in enumerate(files, start = 1): # Por c/archivo en el directorio
    try:
        word = win32com.client.Dispatch("Word.Application") # Generar instancia de word
        word.Visible = False # Ocultar doc para el usuario
        doc = word.Documents.Open(ruta_actual + '\\files\\' + file) # Ruta del archivo

        table_contents = [] # Todas las tablas
        for table in doc.Tables: # Por c/tabla en el doc
            table_content = [] # Cada tabla en específico
            for row in table.Rows: # Por c/fila en la tabla
                row_content = [cell.Range.Text[0:-1].strip() for cell in row.Cells] # Texto de c/u de las celdas de la fila
                table_content.append(row_content)
            table_contents.append(table_content)
        doc.Close() # Cerrar el doc
        word.Quit() # Eliminar la instancia del word

        # Dar formato a la info
        print(f"\nArchivo {index} - {file}:")
        for table_number, table_content in enumerate(table_contents, start = 1):
            print(f"Tabla {table_number}:")
            for row_number, row in enumerate(table_content, start = 1):
                print(f"  Fila {row_number}: {row}")
    except:
        print(f"\nEl archivo que intentas leer no tiene el formato adecuado para extraer la información y se ha omitido: {file}")

print("\n------------------------------------- Terminando Lectura -------------------------------------\n")
fin = time.time() # Fin de la ejecución
print(str(fin - inicio) + " Segundos") # Calcular tiempo de ejecución