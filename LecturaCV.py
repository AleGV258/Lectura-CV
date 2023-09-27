import win32com.client # Para leer .doc → ´pip install pywin32´
import os
import time
from bson import ObjectId
from functions.createDictionary import createDictionary, tablePromep
from functions.cleanData import cleanData
from functions.cleanNames import cleanNames
from functions.dataFunctions import connectionDB, retrieveAllRecords, retrieveRecords, retrieveRecordByID, insertRecord, updateRecords, updateRecordByID, deleteRecords, deleteRecordByID

def lecturaCV(ruta_actual, files, SelectedTables, Filters):
    # (folder_path, documentosArray, SelectedTables,Filters)
    inicio = time.time() # Inicio de la ejecución
    print("\n-------------------------------------- Iniciando Lectura --------------------------------------")
    # ruta_actual2 = os.path.dirname(os.path.abspath(__file__)) # Directorio actual
    # files = os.listdir(ruta_actual + "\\files") # Ruta de los archivos

    mc = connectionDB()
    bd = mc[0]
    word = win32com.client.Dispatch("Word.Application") # Generar instancia de word
    print(files)
    for index, file in enumerate(files, start = 1): # Por c/archivo en el directorio
        try:
            doc = word.Documents.Open(ruta_actual.replace("/", "\\") + "\\" + file) # Ruta del archivo
            doc = word.ActiveDocument # Selección del documento abierto
            doc.ActiveWindow.Visible = False # Ocultar doc para el usuario
            tablas = []
            contenido = []
            nombre = ''
            counter = 0
            for table in doc.Tables: # Por c/tabla en el doc
                for row in table.Rows: # Por c/fila en la tabla
                    row_content = [cleanData(cell.Range.Text[0:-1].strip(), False) for cell in row.Cells] # Texto de c/u de las celdas de la fila
                    if len(row_content) == 1 and row_content[0] != '': 
                        if len(contenido) > 0:
                            counter = counter + 1
                            tablas.append({'nombre': nombre, 'contenido': contenido})
                            contenido = []
                        nombre = row_content[0]
                    elif len(row_content) > 1:
                        contenido.append(row_content)
            doc.Close() # Cerrar el doc
          
            if SelectedTables['InfoProfesor'] == True:            
                # SEPARACIÓN DE DATOS DE LAS TABLAS                
                print('\n------------------Profesores--------------------')
                nombreProfesor = tablas[1]['contenido'][0][1].upper().replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
                profesorRecord = {
                    'Nombre': nombreProfesor,
                    'RFC': tablas[1]['contenido'][2][1],
                    'CURP':  tablas[1]['contenido'][3][1],
                    'FechaNacimiento':  tablas[1]['contenido'][5][1],
                    'IES':  tablas[1]['contenido'][6][1],
                    'EstudioRealizado':  tablas[2]['contenido'], # CORREGIR QUE NO SEA UN ARRAY SINO UN OBJETO
                    'DatosLaborales':  tablas[3]['contenido'], # CORREGIR QUE NO SEA UN ARRAY SINO UN OBJETO
                    'Area':  tablas[4]['contenido'][0][1],
                    'Disciplina':  tablas[4]['contenido'][1][1]
                }
                # Verificar si el profesor ya existe o es uno nuevo
                dataBusqueda = retrieveRecords(bd, "Profesores", {"Nombre":nombreProfesor})
                if(len(dataBusqueda) != 0):
                    profesorID = updateRecords(bd, "Profesores", {"Nombre":nombreProfesor}, profesorRecord)
                else:
                    profesorID = insertRecord(bd, "Profesores", profesorRecord)
                # data = retrieveAllRecords(bd, "Profesores")
                # profesores = set(nombre["Nombre"] for nombre in data)
                # nuevosProfesores = set()
            
            if SelectedTables['LogrosProfesor'] == True:  
                print('\n------------------Logros--------------------')
                print("\n Tabla original: ",tablas[5]['contenido'])
                Logros = createDictionary(tablas[5]['contenido'], ['Tipo', 'Año', 'Título', 'País'], 'Tipo')
                print("\nTabla Resultante: ")
                print("\nLogros: ", Logros)
                
                # # Separar a los Autores
                for logro in Logros:
                    cleanNames(logro['OtrosDatos'][0]['Autor'], logro, 'Logros', 'ProfesorLogros', 'IdLogro')
                    
                    
                #     ProfesorLogros = []
                #     if(len(logro['OtrosDatos'][0]['Autor'].split(';')) > 1):
                #         autores = logro['OtrosDatos'][0]['Autor'].replace('; ', ';').replace('.', '').replace(',', '').split(';')
                #     else:
                #         autores = logro['OtrosDatos'][0]['Autor'].replace(', ', ',').replace('.', '').split(',')
                #     # print('autores:', autores)
                #     for autor in autores:
                #         autor = autor.upper().replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
                #         contador = 0
                #         nombresAutorSplit = set(autor.split(' '))
                #         for profesor in profesores:
                #             nombresSplit = set(profesor.split(' '))
                #             interseccion = nombresAutorSplit.intersection(nombresSplit)
                #             # print(nombresAutorSplit, " - \t", nombresSplit, " - \t", len(interseccion), " - \t", interseccion)
                #             if(len(interseccion) >= 3):
                #                 contador = contador + 1
                #                 break
                #         for profesor in nuevosProfesores:
                #             nombresSplit = set(profesor.split(' '))
                #             interseccion = nombresAutorSplit.intersection(nombresSplit)
                #             if(len(interseccion) >= 3):
                #                 contador = contador + 1
                #                 break
                #         if(contador == 0):
                #             # print("\nSe agrego: ", autor)
                #             nuevosProfesores.add(autor)
                #         # print("\n", len(profesores), " - ", profesores)
                #         ProfesorLogrosRow ={
                #             'Autor': cleanData(autor, False),
                #         }
                #         # print(ProfesorLogrosRow)
                #         ProfesorLogros.append(ProfesorLogrosRow)
                #     logro['OtrosDatos'][0]['Autor'] = ProfesorLogros
                
                # # Insertar Nuevos Profesores Encontrados
                # for profesor in nuevosProfesores:
                #     if(nombreProfesor != cleanData(profesor, False)):
                #         record = {
                #             'Nombre': cleanData(profesor, False),
                #         }
                #         insertRecord(bd, "Profesores", record)
                        
                # data = retrieveAllRecords(bd, "Profesores")
                # profesores = {nombre["_id"]: nombre["Nombre"] for nombre in data}
                # # Insertar Logros hacía un Profesor
                # # print("\nLogros: ", Logros[0])
                # for logro in Logros:
                #     busqueda = retrieveRecords(bd, "Logros", logro)
                #     if(len(busqueda) == 0):
                #         logroID = insertRecord(bd, "Logros", logro)
                #         for autor in logro['OtrosDatos'][0]['Autor']:
                #             nombreProfesorSplit = set(autor['Autor'].split(' '))
                #             for profesorID, profesorNombre in profesores.items():
                #                 profesorNombreSplit = set(profesorNombre.split(' '))
                #                 interseccion = nombreProfesorSplit.intersection(profesorNombreSplit)
                #                 if(len(interseccion) >= 3):
                #                     ProfesorLogros = {
                #                         'Nombre': profesorNombre,
                #                         'IdProfesor': ObjectId(profesorID),
                #                         'IdLogro': ObjectId(logroID)
                #                     }
                #                     insertRecord(bd, "ProfesorLogros", ProfesorLogros)
                #                     break
                
            if SelectedTables['InvestigacionesProfesor'] == True:  
                print('\n------------------Investigaciones--------------------')
                Investigaciones = createDictionary(tablas[11]['contenido'],['Título del proyecto','Nombre del patrocinador','Fecha de inicio','Fecha de fin del proyecto','Tipo de patrocinador','TipoPatrocinador','Investigadores participantes','Alumnos participantes','Actividades realizadas','Para considerar en el currículum de cuerpo académico','Miembros','LGACs'], 'Título del proyecto')
                print("\nInvestigaciones: ", Investigaciones)     
                
                for investigacion in Investigaciones:
                    cleanNames(investigacion['InvestigadoresParticipantes'], investigacion, 'Investigaciones', 'ProfesorInvestigaciones', 'IdInvestigacion')
                
            if SelectedTables['GestionAcademica'] == True:  
                print('\n------------------Gestion Academica--------------------')
                GestionAcademica = createDictionary(tablas[9]['contenido'],['Tipo gestión','Cargo dentro de la comisión o cuerpo colegiado','Función encomendada','Órgano colegiado al que fué presentado','Aprobado','Resultados obtenidos','Estado'], 'Tipo gestión')
                print("\nGestion Academica: ", GestionAcademica)
            
            if SelectedTables['Docencias'] == True:  
                # # Docencia = {
                # #     'Curso': tablas[1]['contenido'][0][1],
                # #     'InstitucionEducacionSuperior': tablas[1]['contenido'][0][1],
                # #     'DependenciaEducacionSuperior': tablas[1]['contenido'][0][1],
                # #     'ProgramaEducativo': tablas[1]['contenido'][0][1],
                # #     'Nivel': tablas[1]['contenido'][0][1],
                # #     'FechaInicio': tablas[1]['contenido'][0][1],
                # #     'Alumnos': tablas[1]['contenido'][0][1],
                # #     'Semanas': tablas[1]['contenido'][0][1],
                # #     'HorasMes': tablas[1]['contenido'][0][1],
                # #     'HorasSemanalesDedicadas': tablas[1]['contenido'][0][1]
                # # }
                print('\n------------------Docencias--------------------')
                # Docencias = createDictionary()
                # print("\nDocencias: ", Docencias)  
            if SelectedTables['BeneficiosPROMEP'] == True:  
                print("\n-------------------Beneficios PROMEP----------------------")
                # Obtención de diccionarios de Beneficios PROMEP
                BeneficiosPROMEP= tablePromep(tablas[12]['contenido'],['IES', 'Solicitud', 'Vigencia', 'Estado'])
                print("\nBeneficios PROMEP: ", BeneficiosPROMEP)
            if SelectedTables['CuerpoAcademico'] == True:  
                print("\n-------------------Cuerpo Academico----------------------")
                CuerpoAcademico = tablePromep(tablas[13]['contenido'],['Nombre','Clave','Grado Consolidación','Línea Académica'])
                print("\nCuerpo Academico: ", CuerpoAcademico)
            if SelectedTables['ProgramasAcademicos'] == True:  
                print("\n-------------------Programas Academicos----------------------")
                # # ProgramaAcademico = {
                # #     'Programa': tablas[1]['contenido'][0][1],
                # #     'Fecha': tablas[1]['contenido'][0][1],
                # #     'TipoActualizacion': tablas[1]['contenido'][0][1]
                # # }
                # # print("\n Programa Academico: ", ProgramaAcademico)
            if SelectedTables['Tutorias'] == True:  
                print('\n------------------Tutorias--------------------')
                Tutorias = createDictionary(tablas[7]['contenido'],['Tutoría','Nivel', 'Programa educativo en el que participa', 'Fecha de inicio', 'Fecha de término', 'Tipo de tutelaje', 'Estado del tutelaje'], 'Tutoría')
                print("\nTutorias: ", Tutorias)
            if SelectedTables['DireccionIndividualizada'] == True:  
                print('\n------------------Dirección Individualizada--------------------')
                DireccionIndividualizada = createDictionary(tablas[8]['contenido'],['Título de la tesis o proyecto individual','Grado'], 'Título de la tesis o proyecto individual')
                print("\nDirección Individualizada: ", DireccionIndividualizada)        
            
        except Exception as error:
            print("An exception occurred:", error)
        # except:
        #     print()
        #     print(f"\nEl archivo que intentas leer no tiene el formato adecuado para extraer la información y se ha omitido: {file}")
    
    mc[1].close()
    print("\n------------------------------------- Terminando Lectura-------------------------------------\n")
    fin = time.time() # Fin de la ejecución
    print(str(fin - inicio) + " Segundos") # Calcular tiempo de ejecución





