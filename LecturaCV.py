import win32com.client
import os
import queue
import time
from bson import ObjectId
from functions.createDictionary import createDictionary, horizontalTable, dictionaryMixTable
from functions.cleanData import cleanData
from functions.cleanNames import cleanNames
from functions.generateData import generateData
from functions.dataFunctions import connectionDB, retrieveAllRecords, retrieveRecords, retrieveRecordByID, insertRecord, updateRecords, updateRecordByID, deleteRecords, deleteRecordByID


def lecturaCV(actualPath, files, selectedTables, queue):
    inicio = time.time() # Inicio de la ejecución
    txtNotification = "Iniciando la Lectura y Carga de los Datos, te pedimos paciencia, ya que la lectura puede tardar hasta 2 minutos por archivo, por la cantidad de información que contenga y velocidad de la red, además te pedimos no abrir documentos de Word mientras se realiza la lectura"
    queue.put(txtNotification)
    print("\n-------------------------------------- Iniciando Lectura --------------------------------------")
    # actualPath2 = os.path.dirname(os.path.abspath(__file__)) # Directorio actual
    # files = os.listdir(actualPath + "\\files") # Ruta de los archivos

    mc = connectionDB()
    bd = mc[0]
    word = win32com.client.Dispatch("Word.Application") # Generar instancia de word
    print(files)
    for index, file in enumerate(files, start = 1): # Por c/archivo en el directorio
        try:
            inicioArchivo = time.time() # Inicio de la ejecución del archivo en específico
            doc = word.Documents.Open(actualPath.replace("/", "\\") + "\\" + file) # Ruta del archivo
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
            txtNotification = f"Terminando lectura del archivo {file}. Iniciando la carga de datos"
            queue.put(txtNotification)
            

    
            # SEPARACIÓN DE DATOS DE LAS TABLAS
            print('\n------------------Profesores--------------------')
            estudiosRealizados = dictionaryMixTable(tablas[2]['contenido'],['Nivel de estudios','Estudios en','Área     > Disciplina','Institución otorgante','Institución otorgante no considerada en el catálogo'], 'Nivel de estudios','País')  
            datosLaborales = generateData(tablas[3]['contenido'], ['Nombramiento', 'Tipo de nombramiento','Dedicación','Institución de Educación Superior','Dependencia de Educación Superior','Unidad Académica','Inicio del contrato', 'Fin del contrato', 'Cronología'])
            nombreProfesor = tablas[1]['contenido'][0][1].upper().replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
            print('\neRealizados:', estudiosRealizados)
            print('\ndatosLaborales:', datosLaborales)
            print('\nnombreProfesor:', nombreProfesor)
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
                txtNotification = f"Actualizando records de Profesor del archivo {file}"
                queue.put(txtNotification)
                profesorID = updateRecords(bd, "Profesores", {"Nombre":nombreProfesor}, profesorRecord)
                if(profesorID == []):
                    profesorID = dataBusqueda[0]["_id"]
            else:
                txtNotification = f"Insertando records de Profesor del archivo {file}"
                queue.put(txtNotification)
                profesorID = insertRecord(bd, "Profesores", profesorRecord)


            # counteri=0 
            for tabla in tablas:
                # print("\n Tabla ",counteri, ": ",tabla['nombre'])
                # counteri= counteri + 1

                if selectedTables['LogrosProfesor'] == True and tabla['nombre'] == 'Producción':  
                    txtNotification = f"Insertando records de Producción y Logros del archivo {file}"
                    queue.put(txtNotification)
                    print('\n------------------Logros--------------------')
                    Logros = createDictionary(tabla['contenido'], ['Tipo', 'Año', 'Título', 'País'], 'Tipo')
                    # print("\nLogros: ", Logros)
                    for logro in Logros:
                        cleanNames(logro['OtrosDatos']['Autor'], logro, 'Logros', 'ProfesorLogros', 'IdLogro')
                    
                if selectedTables['InvestigacionesProfesor'] == True and tabla['nombre'] == 'Proyectos de investigación':
                    txtNotification = f"Insertando records de Investigaciones del Profesor del archivo {file}"
                    queue.put(txtNotification)
                    print('\n------------------Investigaciones--------------------')
                    Investigaciones = createDictionary(tabla['contenido'],['Título del proyecto','Nombre del patrocinador','Fecha de inicio','Fecha de fin del proyecto','Tipo de patrocinador','TipoPatrocinador','Investigadores participantes','Alumnos participantes','Actividades realizadas','Para considerar en el currículum de cuerpo académico','Miembros','LGACs'], 'Título del proyecto')
                    # print("\nInvestigaciones: ", Investigaciones)     
                    for investigacion in Investigaciones:
                        cleanNames(investigacion['InvestigadoresParticipantes'], investigacion, 'Investigaciones', 'ProfesorInvestigaciones', 'IdInvestigacion')
                    
                if selectedTables['GestionAcademica'] == True and tabla['nombre'] == 'Gestión académica': 
                    txtNotification = f"Insertando records de Gestión Académica del archivo {file}" 
                    queue.put(txtNotification)
                    print('\n------------------Gestion Academica--------------------')
                    GestionAcademica = dictionaryMixTable(tabla['contenido'],['Tipo gestión','Cargo dentro de la comisión o cuerpo colegiado','Función encomendada','Órgano colegiado al que fué presentado','Aprobado','Resultados obtenidos','Estado'], 'Tipo gestión', 'Fecha de inicio')
                    # print("\nGestion Academica: ", GestionAcademica)     
                    for gestion in GestionAcademica:
                        busqueda = retrieveRecords(bd, "GestionesAcademicas", gestion)
                        if (len(busqueda) == 0):
                            gestion['IdProfesor'] = ObjectId(profesorID)
                            insertRecord(bd, 'GestionesAcademicas', gestion)
                
                if selectedTables['Tutorias'] == True and tabla['nombre'] == 'Tutoría':
                    txtNotification = f"Insertando records de Tutorías del archivo {file}"
                    queue.put(txtNotification)
                    print('\n------------------Tutorias--------------------')
                    Tutorias = createDictionary(tabla['contenido'],['Tutoría','Nivel', 'Programa educativo en el que participa', 'Fecha de inicio', 'Fecha de término', 'Tipo de tutelaje', 'Estado del tutelaje'], 'Tutoría')
                    # print("\nTutorias: ", Tutorias)
                    for tutoria in Tutorias:
                        busqueda = retrieveRecords(bd, "Tutorias", tutoria)
                        if (len(busqueda) == 0):
                            tutoria['IdProfesor'] = ObjectId(profesorID)
                            insertRecord(bd, 'Tutorias', tutoria)
                        
                if selectedTables['DireccionIndividualizada'] == True and tabla['nombre'] == 'Dirección individualizada':
                    txtNotification = f"Insertando records de Dirección Individualizada del archivo {file}"
                    queue.put(txtNotification)
                    print('\n------------------Dirección Individualizada--------------------')
                    DireccionIndividualizada = dictionaryMixTable(tabla['contenido'],['Título de la tesis o proyecto individual','Grado'], 'Título de la tesis o proyecto individual','Fecha de inicio')
                    # print("\nDirección Individualizada: ", DireccionIndividualizada)        
                    for direccion in DireccionIndividualizada:
                        busqueda = retrieveRecords(bd, "DireccionesIndividualizadas", direccion)
                        if (len(busqueda) == 0):
                            direccion['IdProfesor'] = ObjectId(profesorID)
                            insertRecord(bd, 'DireccionesIndividualizadas', direccion)
                
                if selectedTables['Docencias'] == True and tabla['nombre'] == 'Docencia':
                    txtNotification = f"Insertando records de Docencias del archivo {file}"
                    queue.put(txtNotification)
                    print('\n------------------Docencias--------------------')
                    Docencias = dictionaryMixTable(tabla['contenido'],['Nombre del curso','Institución de Educación Superior (IES)', 'Dependencia de Educación Superior (IES)', 'Programa educativo','Nivel'], 'Nombre del curso','Fecha de inicio')  
                    # print("\n Docencias: ", Docencias)
                    for docencia in Docencias:
                        busqueda = retrieveRecords(bd, "Docencias", docencia)
                        if (len(busqueda) == 0):
                            docencia['IdProfesor'] = ObjectId(profesorID)
                            insertRecord(bd, 'Docencias', docencia)
                
                if selectedTables['BeneficiosPROMEP'] == True and tabla['nombre'] == 'Beneficios externos a PROMEP':
                    txtNotification = f"Insertando records de Beneficios externos a PROMEP del archivo {file}"
                    queue.put(txtNotification)
                    print("\n-------------------Beneficios externos a PROMEP----------------------")
                    # Obtención de diccionarios de Beneficios PROMEP
                    BeneficiosPROMEP = horizontalTable(tabla['contenido'])
                    # print("\nBeneficios PROMEP: ", BeneficiosPROMEP)
                    for beneficio in BeneficiosPROMEP:
                        busqueda = retrieveRecords(bd, "BeneficiosPROMEP", beneficio)
                        if (len(busqueda) == 0):
                            beneficio['IdProfesor'] = ObjectId(profesorID)
                            insertRecord(bd, 'BeneficiosExternosPROMEP', beneficio)
                            
                if selectedTables['BeneficiosPROMEP'] == True and tabla['nombre'] == 'Beneficios PROMEP':
                    txtNotification = f"Insertando records de Beneficios PROMEP del archivo {file}"
                    queue.put(txtNotification)
                    print("\n-------------------Beneficios PROMEP----------------------")
                    # Obtención de diccionarios de Beneficios PROMEP
                    BeneficiosPROMEP = horizontalTable(tabla['contenido'])
                    # print("\nBeneficios PROMEP: ", BeneficiosPROMEP)
                    for beneficio in BeneficiosPROMEP:
                        busqueda = retrieveRecords(bd, "BeneficiosPROMEP", beneficio)
                        if (len(busqueda) == 0):
                            beneficio['IdProfesor'] = ObjectId(profesorID)
                            insertRecord(bd, 'BeneficiosPROMEP', beneficio)
                        
                if selectedTables['CuerpoAcademico'] == True and tabla['nombre'] == 'Cuerpo Académico':
                    txtNotification = f"Insertando records de Cuerpo Académico del archivo {file}" 
                    queue.put(txtNotification)
                    print("\n-------------------Cuerpo Academico----------------------")
                    print("\nAntes: ", tabla['contenido'])
                    CuerpoAcademico = horizontalTable(tabla['contenido'])
                    print("\nCuerpo Academico: ", CuerpoAcademico)
                    for cAcademico in CuerpoAcademico:
                        busqueda = retrieveRecords(bd, "CuerpoAcademico", cAcademico)
                        if (len(busqueda) == 0):
                            cAcademico['IdProfesor'] = ObjectId(profesorID)
                            insertRecord(bd, 'CuerpoAcademico', cAcademico)
                        
                # if selectedTables['ProgramasAcademicos'] == True tabla['nombre'] == 'Cuerpo Académico':
                #     print("\n-------------------Programas Academicos----------------------")
                    # # ProgramaAcademico = {
                    # #     'Programa': tablas[1]['contenido'][0][1],
                    # #     'Fecha': tablas[1]['contenido'][0][1],
                    # #     'TipoActualizacion': tablas[1]['contenido'][0][1]
                    # # }
                    # # print("\n Programa Academico: ", ProgramaAcademico)        
                
                # print("\nTablas encontradas: ----------------------")
                # for tabla in tablas:
                #     print(tabla['nombre'])
                
            finArchivo = time.time() # Fin de la ejecución
            txtNotification = f"Terminando lectura y carga de datos del archivo {file}, tiempo transcurrido: {str(finArchivo - inicioArchivo)} segundos. Iniciando lectura del siguiente archivo"
            if(index == len(files)):
                fin = time.time()
                txtNotification = f"Terminando lectura y carga de datos de todos los archivos en el directorio: {actualPath}\nTiempo total transcurrido: {str(fin - inicio)} segundos"
            queue.put(txtNotification)

        except Exception as error:
            txtNotification = f"Ah ocurrido un error al cargar o leer los datos en el archivo ({file})\nError: {error}"
            queue.put(txtNotification)
            print("An exception occurred:", error)
    
    mc[1].close()
    print("\n------------------------------------- Terminando Lectura-------------------------------------\n")
    fin = time.time() # Fin de la ejecución
    print(str(fin - inicio) + " Segundos") # Calcular tiempo de ejecución
    
