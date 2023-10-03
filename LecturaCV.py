import win32com.client # Para leer .doc → ´pip install pywin32´
import os
import time
from bson import ObjectId
from functions.createDictionary import createDictionary, horizontalTable, dictionaryMixTable
from functions.cleanData import cleanData
from functions.cleanNames import cleanNames
from functions.generateData import generateData
from functions.dataFunctions import connectionDB, retrieveAllRecords, retrieveRecords, retrieveRecordByID, insertRecord, updateRecords, updateRecordByID, deleteRecords, deleteRecordByID

def lecturaCV(ruta_actual, files, SelectedTables, Filters):
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
          
            # if SelectedTables['InfoProfesor'] == True:            
            # SEPARACIÓN DE DATOS DE LAS TABLAS                
            print('\n------------------Profesores--------------------')
            
            estudiosRealizados = dictionaryMixTable(tablas[2]['contenido'],['Nivel de estudios','Estudios en','Área     > Disciplina','Institución otorgante','Institución otorgante no considerada en el catálogo'], 'Nivel de estudios','País')  
            
            datosLaborales = generateData(tablas[3]['contenido'], ['Nombramiento', 'Tipo de nombramiento','Dedicación','Institución de Educación Superior','Dependencia de Educación Superior','Unidad Académica','Inicio del contrato', 'Fin del contrato', 'Cronología'])
            
            nombreProfesor = tablas[1]['contenido'][0][1].upper().replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
            profesorRecord = {
                'Nombre': nombreProfesor,
                'RFC': tablas[1]['contenido'][2][1],
                'CURP':  tablas[1]['contenido'][3][1],
                'FechaNacimiento':  tablas[1]['contenido'][5][1],
                'IES':  tablas[1]['contenido'][6][1],
                'EstudioRealizado':  estudiosRealizados[0],
                'DatosLaborales':  datosLaborales,
                'Area':  tablas[4]['contenido'][0][1],
                'Disciplina':  tablas[4]['contenido'][1][1]
            }
            # Verificar si el profesor ya existe o es uno nuevo
            dataBusqueda = retrieveRecords(bd, "Profesores", {"Nombre":nombreProfesor})
            if(len(dataBusqueda) != 0):
                profesorID = updateRecords(bd, "Profesores", {"Nombre":nombreProfesor}, profesorRecord)
                if(profesorID == []):
                    profesorID = dataBusqueda[0]["_id"]
            else:
                profesorID = insertRecord(bd, "Profesores", profesorRecord)

            if SelectedTables['LogrosProfesor'] == True and tablas[5]['nombre'] == 'Producción':  
                print('\n------------------Logros--------------------')
             
                Logros = createDictionary(tablas[5]['contenido'], ['Tipo', 'Año', 'Título', 'País'], 'Tipo')
                # print("\nLogros: ", Logros)
                
                for logro in Logros:
                    cleanNames(logro['OtrosDatos']['Autor'], logro, 'Logros', 'ProfesorLogros', 'IdLogro')
                
            if SelectedTables['InvestigacionesProfesor'] == True and tablas[11]['nombre'] == 'Proyectos de investigación':  
                print('\n------------------Investigaciones--------------------')
                
                Investigaciones = createDictionary(tablas[11]['contenido'],['Título del proyecto','Nombre del patrocinador','Fecha de inicio','Fecha de fin del proyecto','Tipo de patrocinador','TipoPatrocinador','Investigadores participantes','Alumnos participantes','Actividades realizadas','Para considerar en el currículum de cuerpo académico','Miembros','LGACs'], 'Título del proyecto')
                # print("\nInvestigaciones: ", Investigaciones)     
            
                for investigacion in Investigaciones:
                    cleanNames(investigacion['InvestigadoresParticipantes'], investigacion, 'Investigaciones', 'ProfesorInvestigaciones', 'IdInvestigacion')
                
            if SelectedTables['GestionAcademica'] == True and tablas[9]['nombre'] == 'Gestión académica':  
                print('\n------------------Gestion Academica--------------------')
                GestionAcademica = dictionaryMixTable(tablas[9]['contenido'],['Tipo gestión','Cargo dentro de la comisión o cuerpo colegiado','Función encomendada','Órgano colegiado al que fué presentado','Aprobado','Resultados obtenidos','Estado'], 'Tipo gestión', 'Fecha de inicio')
                # print("\nGestion Academica: ", GestionAcademica)
                                
                for gestion in GestionAcademica:
                    gestion['IdProfesor'] = ObjectId(profesorID)
                    insertRecord(bd, 'GestionesAcademicas', gestion)                              
            
            if SelectedTables['Tutorias'] == True and tablas[7]['nombre'] == 'Tutoría':  
                print('\n------------------Tutorias--------------------')
                Tutorias = createDictionary(tablas[7]['contenido'],['Tutoría','Nivel', 'Programa educativo en el que participa', 'Fecha de inicio', 'Fecha de término', 'Tipo de tutelaje', 'Estado del tutelaje'], 'Tutoría')
                print("\nTutorias: ", Tutorias)
                
                for tutoria in Tutorias:
                    tutoria['IdProfesor'] = ObjectId(profesorID)
                    insertRecord(bd, 'Tutorias', tutoria)
                    
            if SelectedTables['DireccionIndividualizada'] == True and tablas[8]['nombre'] == 'Dirección individualizada':  
                print('\n------------------Dirección Individualizada--------------------')
                DireccionIndividualizada = dictionaryMixTable(tablas[8]['contenido'],['Título de la tesis o proyecto individual','Grado'], 'Título de la tesis o proyecto individual','Fecha de inicio')
                print("\nDirección Individualizada: ", DireccionIndividualizada)        
            
                for direccion in DireccionIndividualizada:
                    direccion['IdProfesor'] = ObjectId(profesorID)
                    insertRecord(bd, 'DireccionesIndividualizadas', direccion)
            
            if SelectedTables['Docencias'] == True and tablas[6]['nombre'] == 'Docencia':   
                print('\n------------------Docencias--------------------')
                print(tablas[6]['contenido'])
                # Docencias = createDictionary()
                # print("\nDocencias: ", Docencias)
                Docencias = dictionaryMixTable(tablas[6]['contenido'],['Nombre del curso','Institución de Educación Superior (IES)', 'Dependencia de Educación Superior (IES)', 'Programa educativo','Nivel'], 'Nombre del curso','Fecha de inicio')  
                print("\n Docencias: ", Docencias)
                
                for docencia in Docencias:
                    docencia['IdProfesor'] = ObjectId(profesorID)
                    insertRecord(bd, 'Docencias', docencia)
            
            if SelectedTables['BeneficiosPROMEP'] == True and tablas[12]['nombre'] == 'Beneficios externos a PROMEP':  
                print("\n-------------------Beneficios PROMEP----------------------")
                # Obtención de diccionarios de Beneficios PROMEP
                BeneficiosPROMEP= horizontalTable(tablas[12]['contenido'])
                print("\nBeneficios PROMEP: ", BeneficiosPROMEP)
                
                for beneficio in BeneficiosPROMEP:
                    beneficio['IdProfesor'] = ObjectId(profesorID)
                    insertRecord(bd, 'BeneficiosPROMEP', beneficio)
                    
            if SelectedTables['CuerpoAcademico'] == True and tablas[13]['nombre'] == 'Cuerpo Académico':  
                print("\n-------------------Cuerpo Academico----------------------")
                CuerpoAcademico = horizontalTable(tablas[13]['contenido'])
                print("\nCuerpo Academico: ", CuerpoAcademico)
                
                for cAcademico in CuerpoAcademico:
                    cAcademico['IdProfesor'] = ObjectId(profesorID)
                    insertRecord(bd, 'CuerpoAcademico', cAcademico)
                    
            if SelectedTables['ProgramasAcademicos'] == True:  
                print("\n-------------------Programas Academicos----------------------")
                # # ProgramaAcademico = {
                # #     'Programa': tablas[1]['contenido'][0][1],
                # #     'Fecha': tablas[1]['contenido'][0][1],
                # #     'TipoActualizacion': tablas[1]['contenido'][0][1]
                # # }
                # # print("\n Programa Academico: ", ProgramaAcademico)        
            
            print("\nTablas encontradas: ----------------------")
            for tabla in tablas:
                print(tabla['nombre'])
                
        except Exception as error:
            print("An exception occurred:", error)
        # except:
        #     print()
        #     print(f"\nEl archivo que intentas leer no tiene el formato adecuado para extraer la información y se ha omitido: {file}")
    
    mc[1].close()
    print("\n------------------------------------- Terminando Lectura-------------------------------------\n")
    fin = time.time() # Fin de la ejecución
    print(str(fin - inicio) + " Segundos") # Calcular tiempo de ejecución





