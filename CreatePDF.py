from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from functions.dataFunctions import connectionDB, retrieveAllRecords, retrieveRecords, retrieveRecordByID, insertRecord, updateRecords, updateRecordByID, deleteRecords, deleteRecordByID
import json
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Frame
from reportlab.lib import colors

# Cargar datos desde el archivo JSON
#with open("datos.json", "r") as json_file:
 #   datos = json.load(json_file)


# ____ _ _    ___ ____ ____ ____          ____ _    ____ ____       |
# |___ | |     |  |__/ |  | [__     __    |  | |    |__| |___     \ | /
# |    | |___  |  |  \ |__| ___]          |__| |___ |  | |         \|/
                                                            
# --------------------------- DATOS QUE SE DEBEN FILTRAR
# Existen 4 principales filtros Año, Area de Conocimiento, Nombre de Autor, Tipo de Documento

# Nombre de Autor se encuentra en las tablas Logros e Investigaciones
# Retrieve records from (Logros o Investigaciones)
#
# busqueda = {"Nombre":"MAURICIO ARTURO IBARRA CORONA"}
# data = RetrieveRecords("Profesores", busqueda)
# print(data)
#
# De la forma anterior solo se regresaran los que coincidan con la busqueda, ahora ojo, esto regresara solo la informacion de la tabla profesor, se requiere extraer el id y hacerlo coincidir con las tablas profesorlogros y profesorinvestigaciones

# Año se encuentra en varias tablas pero solo vamos a filtrarlo en Logros e Investigaciones, en logros no hay mayor problema que buscar {"Ano":"2019"}, pero en Investigaciones tienes traer todas las investigaciones y por cada fechainicio y fechafinproyecto, separar la fecha por / , una vez hecho esto coincidir lo s años y regresar esto

# Tipo de Documento se encuentra en la tabla Logros y es simplemente filtrar por {"Tipo":"Productividad Innovadora"}
# Si se ingresa algo como "Patente", esto no se encuentra directamente en tipo se tiene que ingresar a otros datos y buscar lo siguiente {"TipoProduccionInnovadora":"Patente"}

# Area de Conocimiento se encuentra en un "stand by" ese todavia no lo consideres, le tengo que preguntar una cosa primero al profe
# Otros se encuentra en un "stand by" ese todavia no lo consideres 

# los filtros se te devuelven de la siguiente manera:
#  
#
    # Si state es False no se considera aunque data tenga información

# ------------------------------------------------------

# ____ _ _    ___ ____ ____ ____          ____ _    ____ ____      /|\
# |___ | |     |  |__/ |  | [__     __    |  | |    |__| |___     / | \
# |    | |___  |  |  \ |__| ___]          |__| |___ |  | |          |


def createTable(filtros = {}):
    print("\n Filtros recibidos: ", filtros)
    

    mc = connectionDB()
    db = mc[0]
    
    # Recupera todos los registros de la colección "Profesores" de la base de datos
    #profesorI = retrieveAllRecords(db, "Profesores") #Comentado por que no puedo usar la base de datos xd

    #Prueba estatica de datos
    profesorI = retrieveAllRecords(db, "Profesores")

    print(profesorI)
    #def filter_func(profesor):
    #    for filtro_key, filtro_info in filtros.items():
    #        if filtro_info['state']:
    #            if profesor.get(filtro_key, '') != filtro_info['data']:
    #                return False
    #    return 
    #listaData = []
    #for profesorData in profesorI['data']:
     #   filtroData = profesorData
    #    listaData.add(filtroData)
    #print(filtroData)
    #def filter_func(profesor):
    #    for filtro_key, filtro_info in filtros.items():
    ##        if filtro_info['state']:
     #           if profesor.get(filtro_key, '') != filtro_info['data']:
    #                return False
    #    return True


    # Aplicar la función de filtro a los datos si hay alguno
    
    #datosFiltrados1 = filter(filter_func, profesorI)

    # Convertir el resultado filtrado a una lista
    datosFiltrados = profesorI

    print(datosFiltrados)

    # Crear un archivo PDF llamado "tabla_desde_json.pdf"
    doc = SimpleDocTemplate("tabla_desde_python.pdf", pagesize=letter)

    # Crear una lista de nombres de columnas
    columnas = ["_id", "Nombre", "FechaNacimiento", "IES"]
    #for i in filtros:
    #    columnas.append(i)

    # Crear una lista de listas a partir de los datos filtrados
    dataFinal = [columnas]
    
    for profesor in datosFiltrados:
        dataFinal.append([
            profesor.get("_id", ""),
            profesor.get("Nombre", ""),
            profesor.get("FechaNacimiento", ""),
            profesor.get("IES", "")
        ])


    print(dataFinal,"------------------------------")
    # Crear una tabla con los datos
    tabla = Table(dataFinal)

    # Aplicar estilo a la tabla
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, '#27a39d'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Borde interno
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ])

    tabla.setStyle(estilo)

    # Crear el objeto Story y agregar la tabla al contenido
    story = []
    story.append(tabla)

    # Construir el PDF
    doc.build(story)
    print("DOCUMENTO CREADO")
#Prueba del codigo con datos estaticos
#filtrosPrueba = {'autor': {'state': False, 'data': 'ALEJANDRO'}, 
#        'ano': {'state': True, 'data': '2019'}, 
#        'documento': {'state': True, 'data': 'Patente'}, 
#        'areaConocimiento': {'state': False, 'data': ''}, 
#        'otro': {'state': False, 'data': 'Otros'}}


