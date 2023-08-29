import win32com.client # Para leer .doc → ´pip install pywin32´
import os
import time




def RecocorrerInfoArray (array = [], fields=[]): 
    data = {
        'OtrosDatos': []
    }
    for arr in array:
        if arr[0] in fields: 
            data[arr[0]] = arr[1]
        else:
            data['OtrosDatos'].append( { arr[0]: arr[1].replace('\r\x07', ", ")})
    return data

    






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
                        print({'nombre': nombre, 'contenido': contenido})
                        print(counter)
                        print('')
                        print('')
                        print('')
                        tablas.append({'nombre': nombre, 'contenido': contenido})
                        contenido = []
                                                
                    nombre = row_content[0]                    
                    # print(row_content)
                    
                elif len(row_content)  > 1:
                    contenido.append(row_content)
                    # print(f"\t {row_content}")
                    
        # doc.Close() # Cerrar el doc
        # word.Quit() # Eliminar la instancia del word
        
        
        Profesor = {
            'Nombre': tablas[1]['contenido'][0][1],
            'RFC': tablas[1]['contenido'][2][1],
            'CURP':  tablas[1]['contenido'][3][1],
            'FechaNacimiento':  tablas[1]['contenido'][5][1],
            'IES':  tablas[1]['contenido'][6][1],
            'EstudioRealizado':  tablas[2]['contenido'],
            'DatosLaborales':  tablas[3]['contenido'],
            'Area':  tablas[4]['contenido'][0][1],
            'DIciplina':  tablas[4]['contenido'][1][1]
        }
        
        contador=0
        Logros = []
        Logro_Arreglo = []
        insertando = False
        for logro in tablas[5]['contenido']: 
            if logro[0] == 'Tipo' and contador != 0: 
                insertando = True
            
            if insertando:
                array = ['Tipo', 'Año', 'Título', 'País']
                logroDiccionario = RecocorrerInfoArray(Logro_Arreglo, array)
          
                Logros.append(logroDiccionario)
                
                Logro_Arreglo = []
                insertando = False
            Logro_Arreglo.append(logro)            
            contador = contador + 1
           
        #
        # ProfesorLogros = {
        #     'IdProfesor': tablas[1]['contenido'][0][1],
        #     'IdLogro': tablas[1]['contenido'][0][1]
        # }
        
        
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
        contador=0
        Investigaciones = []
        Investigacion_Arreglo = []
        insertando = False
        for investigacion in tablas[11]['contenido']: 
            if investigacion[0] == 'Título del proyecto' and contador != 0: 
                insertando = True
            
            if insertando:
                array = ['Título del proyecto','Nombre del patrocinador','Fecha de inicio','Fecha de fin del proyecto','Tipo de patrocinador','TipoPatrocinador','Investigadores participantes','Alumnos participantes','Actividades realizadas','Para considerar en el currículum de cuerpo académico','Miembros','LGACs']
                investigacionDiccionario = RecocorrerInfoArray( Investigacion_Arreglo, array)
                
                Investigaciones.append(investigacionDiccionario)
          
                
                Investigacion_Arreglo = []
                insertando = False
            Investigacion_Arreglo.append(logro)            
            contador = contador + 1
       
        print("\nInvestigaciones: ", Investigaciones)
        ########################################################################################################
        #  def tablasCreacion(contador, arrayArreglo, insertado=false, tabla, nombreTitulo, array):
        #    arrayGUardado = []
        #      for dato in tabla['contenido']:
        #       if dato[0] == nombreTitulo and contador != 0:
        #           insertado = TRUE 
        #       if insertado: 
        #           arrayDiccionario = RecocorrerInfoArray(arrayArreglo, array)
        #           arrayGuardado.append(arrayDiccionario)

        #           arrayArreglo = []
        #           insertado = Falso
        #       arrayArreglo.append(dato)
        #       contador = contador + 1
        #   return arrayGUardado
        #####################################################################################################
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
        # BeneficiosPROMEP = {
        #     'IES': tablas[1]['contenido'][0][1],
        #     'Solicitud': tablas[1]['contenido'][0][1],
        #     'Vigencia': tablas[1]['contenido'][0][1],
        #     'Estado': tablas[1]['contenido'][0][1]
        # }
        # CuerpoAcademico = {
        #     'Nombre': tablas[1]['contenido'][0][1],
        #     'Clave': tablas[1]['contenido'][0][1],
        #     'GradoConsolidacion': tablas[1]['contenido'][0][1],
        #     'LineaAcademica': tablas[1]['contenido'][0][1]
        # }
        # ProgramaAcademico = {
        #     'Programa': tablas[1]['contenido'][0][1],
        #     'Fecha': tablas[1]['contenido'][0][1],
        #     'TipoActualizacion': tablas[1]['contenido'][0][1]
        # }
        # Tutorias = {
        #     'Tutoria': tablas[1]['contenido'][0][1],
        #     'Nivel': tablas[1]['contenido'][0][1],
        #     'ProgramaEducativo': tablas[1]['contenido'][0][1],
        #     'FechaInicio': tablas[1]['contenido'][0][1],
        #     'FechaTermino': tablas[1]['contenido'][0][1],
        #     'TipoTutelaje': tablas[1]['contenido'][0][1],
        #     'EstadoTutelaje': tablas[1]['contenido'][0][1]
        # }
        # DireccionIndividualizada = {
        #     'Titulo': tablas[1]['contenido'][0][1],
        #     'Grado': tablas[1]['contenido'][0][1],
        #     'OtrosDatos': tablas[1]['contenido'][0][1]
        # }
        
        print('------------------RESULTADOS--------------------')
        print("\nNombre: ",Profesor)
        print("\nLogros: ",Logros)
        
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


