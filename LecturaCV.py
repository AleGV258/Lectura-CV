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

        tablas=[]
        nombre = ''
        contenido=[]
        counter = 0
        for table in doc.Tables: # Por c/tabla en el doc
            for row in table.Rows: # Por c/fila en la tabla
                row_content = [cell.Range.Text[0:-1].strip() for cell in row.Cells] # Texto de c/u de las celdas de la fila
                if len(row_content) == 1 and row_content[0] != '': 
                    if len(contenido) > 0:
                        counter = counter + 1
                        # print(counter)
                        # print({'nombre': nombre, 'contenido': contenido})
                        # print('')
                        # print('')
                        # print('')
                        tablas.append({'nombre': nombre, 'contenido': contenido})
                        contenido = []
                                                
                    nombre = row_content[0]                    
                    # print(row_content)
                    
                elif len(row_content)  > 1:
                    contenido.append(row_content)
                    # print(f"\t {row_content}")
                    
        doc.Close() # Cerrar el doc
        word.Quit() # Eliminar la instancia del word
        
        print('tabla final')
        # BUCAR TODO EN Variable tablas
        
        # Separar datos del profesor    
        # Formato al objeto
        # Enviarlo
        
        

    except Exception as error:
        print("An exception occurred:", error)
    # except:
    #     print()
    #     print(f"\nEl archivo que intentas leer no tiene el formato adecuado para extraer la información y se ha omitido: {file}")

print("\n------------------------------------- Terminando Lectura -------------------------------------\n")
fin = time.time() # Fin de la ejecución
print(str(fin - inicio) + " Segundos") # Calcular tiempo de ejecución