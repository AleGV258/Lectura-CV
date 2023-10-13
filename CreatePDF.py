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
# {'autor': {'state': True, 'data': 'ALEJANDRO'}, 
# 'ano': {'state': False, 'data': '2019'}, 
# 'documento': {'state': True, 'data': 'Patente'}, 
# 'areaConocimiento': {'state': True, 'data': ''}, 
# 'otro': {'state': False, 'data': 'Otros'}}
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
    profesorI = [
    {
        "autor": "ALEJANDRO",
        "ano": 2019,
        "documento": "Patente",
        "areaConocimiento": "Ciencias de la Computación",
        "otro" : {"dia" : "no", "fecha" : 20192, "_id" : 290256}
    },
    {
        "autor": "María",
        "ano": 2020,
        "documento": "Tesis",
        "areaConocimiento": "Matemáticas"
    },
    {
        "autor": "Carlos",
        "ano": 2019,
        "documento": "Artículo",
        "areaConocimiento": "Física"
    },
    {
        "autor": "Ana",
        "ano": 2020,
        "documento": "Tesis",
        "areaConocimiento": "Biología"
    }
]

    # Filtra los datos de acuerdo a los filtros recibidos
    #datosFiltrados = profesorI

    #Intento de crear los filtros, estos se guardaran en una lista y despues de 
    # tomamos la lista para poder  realizar los filtros bases
    #Si no los encuentra sigue, aunque creo que tiene un problema, se vuelven a insertar los impresos
    #Solo quedaria eso para verificar si funciona
    
    #  ____ _    ____ ____     /|\
    # |  | |    |__| |___     / | \             Y el isra
    # |__| |___ |  | |          |

    #Intento de arreglar el problema del codigo
    #def filter_func(profesor):
        #print("Esto es loq ue tiene profesor", profesor)
        #for filtro_key, filtro_info in filtros.items():
            #if filtro_info['state']:
                #print("FiltroInfo------------------",filtro_info)
                #print("Buscando la mierda en la sopa", filtro_key)
            #    if profesor.get(filtro_key, '') != filtro_info['data']:
                    #print("iltro Key---------------", filtro_key, "Dta que esta buscando", filtro_info['data'])
                    #print("datos que esta buscando en profesor", profesor.get(filtro_key, ''))
            #        return False 
            #return True

    def filter_func(profesor):
        for filtro_key, filtro_info in filtros.items():
            if filtro_info['state']:
                if profesor.get(filtro_key, '') != filtro_info['data']:
                    return False
        return True


    x = len(filtros)
    # Aplicar la función de filtro a los datos si hay alguno
    
    datosFiltrados1 = filter(filter_func, profesorI)

    # Convertir el resultado filtrado a una lista
    datosFiltrados = list(datosFiltrados1)

    print(datosFiltrados)

    # Crear un archivo PDF llamado "tabla_desde_json.pdf"
    doc = SimpleDocTemplate("tabla_desde_python.pdf", pagesize=letter)

    # Crear una lista de nombres de columnas
    columnas = []
    for i in filtros:
        columnas.append(i)

    # Crear una lista de listas a partir de los datos filtrados
    dataFinal = [columnas]
    
    for profesor in datosFiltrados:
        fila = [profesor.get(col, '') for col in columnas]
        dataFinal.append(fila)

    # Crear una tabla con los datos
    tabla = Table(dataFinal)

    # Aplicar estilo a la tabla
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
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
filtrosPrueba = {'autor': {'state': True, 'data': 'Ana'}, 
        'ano': {'state': True, 'data': 2019}, 
        'documento': {'state': True, 'data': 'Patente'}, 
        'areaConocimiento': {'state': False, 'data': ''}, 
        'otro': {'state': False, 'data': 'Otros'}}

createTable(filtrosPrueba)
