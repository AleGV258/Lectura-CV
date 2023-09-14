import win32com.client # Para leer .doc → ´pip install pywin32´
import os
import time
from functions.createDictionary import createDictionary, tablePromep
from functions.cleanData import cleanData

inicio = time.time() # Inicio de la ejecución
print("\n-------------------------------------- Iniciando Lectura --------------------------------------")
ruta_actual = os.path.dirname(os.path.abspath(__file__)) # Directorio actual
files = os.listdir(ruta_actual + "\\files") # Ruta de los archivos

print(files)

for index, file in enumerate(files, start = 1): # Por c/archivo en el directorio
    try:
        word = win32com.client.Dispatch("Word.Application") # Generar instancia de word
        word.Visible = False # Ocultar doc para el usuario
        doc = word.Documents.Open(ruta_actual + '\\files\\' + file) # Ruta del archivo

        tablas = []
        nombre = ''
        contenido = []
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
        word.Quit() # Eliminar la instancia del word
        
        print('\n------------------Profesor--------------------')
        Profesor = {
            'Nombre': tablas[1]['contenido'][0][1],
            'RFC': tablas[1]['contenido'][2][1],
            'CURP':  tablas[1]['contenido'][3][1],
            'FechaNacimiento':  tablas[1]['contenido'][5][1],
            'IES':  tablas[1]['contenido'][6][1],
            'EstudioRealizado':  tablas[2]['contenido'],
            'DatosLaborales':  tablas[3]['contenido'],
            'Area':  tablas[4]['contenido'][0][1],
            'Disciplina':  tablas[4]['contenido'][1][1]
        }
        print("\nProfesorAAA: ", Profesor)
        
        print('\n------------------Logros--------------------')
        Logros = createDictionary(tablas[5]['contenido'],['Tipo', 'Año', 'Título', 'País'], 'Tipo')
        print("\nLogros: ", Logros)

        
        for logro in Logros:
            print("\n Autores: ")
            ProfesorLogros = []
            autores = logro['OtrosDatos'][0]['Autor'].split(', ')
            for autor in autores:
                ProfesorLogrosRow ={
                    "Autor": autor
                }
                print(ProfesorLogrosRow)
                ProfesorLogros.append(ProfesorLogrosRow)
            logro['OtrosDatos'][0]['Autor']= ProfesorLogros
        print("\nLogros: ", Logros)
        
        # print("\nProfesLogros: ", ProfesorLogros)
        # # ProfesorLogros = {
        # #     'IdProfesor': tablas[1]['contenido'][0][1],
        # #     'IdLogro': tablas[1]['contenido'][0][1]
        # # }
        
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
        # print('\n------------------Docencias--------------------')
        # Docencias = createDictionary()
        # print("\nDocencias: ", Docencias)  
        
        # Investigaciones = {
        #     'Titulo': tablas[1]['contenido'][0][1],
        #     'Patrocinador': tablas[1]['contenido'][0][1],
        #     'FechaInicio': tablas[1]['contenido'][0][1],
        #     'FechaTerminado': tablas[1]['contenido'][0][1],
        #     'TipoPatrocinador': tablas[1]['contenido'][0][1],
        #     'AlumnosParticipantes': tablas[1]['contenido'][0][1],
        #     'ActividadesRealizadas': tablas[1]['contenido'][0][1],
        #     'ConsideradoParaCurriculum': tablas[1]['contenido'][0][1],
        #     'Miembros': tablas[1]['contenido'][0][1],
        #     'LGACs': tablas[1]['contenido'][0][1],
        # }
        # print('\n------------------Investigaciones--------------------')
        # Investigaciones = createDictionary(tablas[11]['contenido'],['Título del proyecto','Nombre del patrocinador','Fecha de inicio','Fecha de fin del proyecto','Tipo de patrocinador','TipoPatrocinador','Investigadores participantes','Alumnos participantes','Actividades realizadas','Para considerar en el currículum de cuerpo académico','Miembros','LGACs'], 'Título del proyecto')
        # print("\nInvestigaciones: ", Investigaciones)     
        
        # ProfesorInvestigaciones = {
        #     'IdProfesor': tablas[1]['contenido'][0][1],
        #     'IdInvestigacion': tablas[1]['contenido'][0][1]
        # }
        
        # GestionAcademica = {
        #     'Tipo': tablas[1]['contenido'][0][1],
        #     'Cargo': tablas[1]['contenido'][0][1],
        #     'Funcion': tablas[1]['contenido'][0][1],
        #     'OrganoPresentado': tablas[1]['contenido'][0][1],
        #     'Aprobado': tablas[1]['contenido'][0][1],
        #     'Resultado': tablas[1]['contenido'][0][1],
        #     'Estado': tablas[1]['contenido'][0][1],
        #     'OtrosDatos': tablas[1]['contenido'][0][1]
        # }        
        # print('\n------------------Gestion Academica--------------------')
        # GestionAcademica = createDictionary(tablas[9]['contenido'],['Tipo gestión','Cargo dentro de la comisión o cuerpo colegiado','Función encomendada','Órgano colegiado al que fué presentado','Aprobado','Resultados obtenidos','Estado'], 'Tipo gestión')
        # print("\nGestion Academica: ", GestionAcademica)
        
        # print("\n-------------------Beneficios PROMEP----------------------")
        # # Obtención de diccionarios de Beneficios PROMEP
        # # BeneficiosPROMEP= tablePromep(tablas[12]['contenido'],['IES', 'Solicitud', 'Vigencia', 'Estado'])
        # # print("\nBeneficios PROMEP: ", BeneficiosPROMEP)
        
        
        # print("\n-------------------Cuerpo Academico----------------------")
        # # CuerpoAcademico = {
        # #     'Nombre': tablas[1]['contenido'][0][1],
        # #     'Clave': tablas[1]['contenido'][0][1],
        # #     'GradoConsolidacion': tablas[1]['contenido'][0][1],
        # #     'LineaAcademica': tablas[1]['contenido'][0][1]
        # # }
        # # CuerpoAcademico = tablePromep(tablas[13]['contenido'],['Nombre','Clave','Grado Consolidación','Línea Académica'])
        # # print("\nCuerpo Academico: ", CuerpoAcademico)
        
        # # ProgramaAcademico = {
        # #     'Programa': tablas[1]['contenido'][0][1],
        # #     'Fecha': tablas[1]['contenido'][0][1],
        # #     'TipoActualizacion': tablas[1]['contenido'][0][1]
        # # }
        # # print("\n Programa Academico: ", ProgramaAcademico)
        
        # # Tutorias = {
        # #     'Tutoria': tablas[1]['contenido'][0][1],
        # #     'Nivel': tablas[1]['contenido'][0][1],
        # #     'ProgramaEducativo': tablas[1]['contenido'][0][1],
        # #     'FechaInicio': tablas[1]['contenido'][0][1],
        # #     'FechaTermino': tablas[1]['contenido'][0][1],
        # #     'TipoTutelaje': tablas[1]['contenido'][0][1],
        # #     'EstadoTutelaje': tablas[1]['contenido'][0][1]
        # # }
        # print('\n------------------Tutorias--------------------')
        # Tutorias = createDictionary(tablas[7]['contenido'],['Tutoría','Nivel', 'Programa educativo en el que participa', 'Fecha de inicio', 'Fecha de término', 'Tipo de tutelaje', 'Estado del tutelaje'], 'Tutoría')
        # print("\nTutorias: ", Tutorias)
        
        # # DireccionIndividualizada = {
        # #     'Titulo': tablas[1]['contenido'][0][1],
        # #     'Grado': tablas[1]['contenido'][0][1],
        # #     'OtrosDatos': tablas[1]['contenido'][0][1]
        # # }
        # print('\n------------------Dirección Individualizada--------------------')
        # DireccionIndividualizada = createDictionary(tablas[8]['contenido'],['Título de la tesis o proyecto individual','Grado'], 'Título de la tesis o proyecto individual')
        # print("\nDirección Individualizada: ", DireccionIndividualizada)
        
        
    except Exception as error:
        print("An exception occurred:", error)
    # except:
    #     print()
    #     print(f"\nEl archivo que intentas leer no tiene el formato adecuado para extraer la información y se ha omitido: {file}")

print("\n------------------------------------- Terminando Lectura -------------------------------------\n")
fin = time.time() # Fin de la ejecución
print(str(fin - inicio) + " Segundos") # Calcular tiempo de ejecución


