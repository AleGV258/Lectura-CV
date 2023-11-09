from functions.generateData import generateData
from functions.dataFunctions import connectionDB, retrieveAllRecords, retrieveRecords, retrieveRecordByID, insertRecord, updateRecords, updateRecordByID, deleteRecords, deleteRecordByID
from fuzzywuzzy import fuzz
import difflib
import psutil
import subprocess
import os















#### Contar instancias de un programa corriendo
# count = 0
# for process in psutil.process_iter(attrs=['pid', 'name']):
#         if 'WINWORD.EXE' in process.info['name']:
#                 count += 1
# print(f"Instancias de Microsoft Word en ejecución: {count}")












#### Comparar Nombres
# data = RetrieveAllRecords("Profesores")
# nombreComparar1 = "JOSE ALEJANDRO VARGAS DIAZ"
# nombreComparar2 = "MAURICIO ARTURO IBARRA CORONA"
# nombreComparar3 = "CARLOS OLMOS TREJO"
# nombreComparar4 = "GABRIELA XICONTECATL RAMIREZ"
# profesores = set([nombre["Nombre"] for nombre in data])

# print("\n", nombres)
# print("\n", nombreComparar)

# nombresAutor = set(nombreComparar.split(' '))
# for profesor in profesores:
#         similarity_ratio1 = fuzz.ratio(nombreComparar1, profesor)
#         similarity_ratio2 = fuzz.ratio(nombreComparar2, profesor)
#         similarity_ratio3 = fuzz.ratio(nombreComparar3, profesor)
#         similarity_ratio4 = fuzz.ratio(nombreComparar4, profesor)
#         if(similarity_ratio1 > 48):
#                 print(f"\nLa similitud entre los nombres es {similarity_ratio1}% {nombreComparar1} - {profesor}")
        # if(similarity_ratio2 > 48):
        #         print(f"\nLa similitud entre los nombres es {similarity_ratio2}% {nombreComparar2} - {profesor}")
        # if(similarity_ratio3 > 48):
        #         print(f"\nLa similitud entre los nombres es {similarity_ratio3}% {nombreComparar3} - {profesor}")
        # if(similarity_ratio4 > 48):
        #         print(f"\nLa similitud entre los nombres es {similarity_ratio4}% {nombreComparar4} - {profesor}")
        
        
        
        # nombres = set(profesor.split(' '))
        # interseccion = nombresAutor.intersection(nombres)
        # if(len(interseccion) >= 3):
        #         print("\n\n", nombresAutor, " + ", nombres, " + INTERSECCIONES: ", len(interseccion))














# mc = connectionDB()
# bd = mc[0]

# #### Retrieve All Data
# data = RetrieveAllRecords("Profesores")
# print(data)

# #### Retrieve Data
# record = {'TituloTesisProyectoIndividual': 'Metodología para la creación de cursos de formación y preparación de estudiantes de licenciatura en modalidad en línea', 'Grado': 'Maestría', 'FechaInicio': '04/02/2022', 'FechaTermino': '22/12/2023', 'No.Alumnos': '1', 'EstadoDireccionIndividualizada': 'En proceso', 'ParaConsiderarCurriculumCuerpoAcademico': 'Si', 'Miembros': '0', 'LGACs': '1'}
# data = retrieveRecords(bd, "DireccionesIndividualizadas", record)
# print("\n",data)

# #### Retrieve Data By ID
# data = RetrieveRecordByID("Profesores", "64ed0fea48358aee9d17d8f5")
# print(data)

# #### Insert Data
# record = {
#     "numero": "600",
#     "kkkkkkk": "hhhh6hh",
#     "prueba": "prueba2",
# }
# InsertRecord("Profesores", record)

# #### Update Data
# buscar = {"prueba":"prueba3"}
# reemplazar = {"prueba":"prueba6"}
# UpdateRecords("Profesores", buscar, reemplazar)

# #### Update Data By ID
# reemplazar = {"prueba":"actualizado23424234"}
# UpdateRecordByID("Profesores", "64ed603be3585f45adc937be", reemplazar)

# #### Delete Data
# record = {"prueba":"prueba2"}
# DeleteRecords("Profesores", record)

# #### Delete Data By ID
# DeleteRecordByID("Profesores", "64ed6038d52208b257f39429")

# profesores = RetrieveAllRecords("Profesores")
# print(profesores[0]["Nombre"])











# # Lista de nombres estandarizados
# nombres_estandarizados = ["JOSE ALEJANDRO VARGAS DIAZ", "JOSE VARGAS BAECHELER", "DIEGO OCTAVIO IBARRA CORONA", "MAURICIO ARTURO IBARRA CORONA"]

# # Función para encontrar la similitud entre dos nombres
# def encontrar_similitud(nombre_entrada):
#     mejor_coincidencia = difflib.get_close_matches(nombre_entrada, nombres_estandarizados, n=1, cutoff=0.5)
#     if mejor_coincidencia:
#         return mejor_coincidencia[0]
#     else:
#         return None

# # Nombre de entrada
# nombre_entrada = "IBARRA CORONA DIEGO OCTAVIO"

# # Encontrar la mejor coincidencia
# nombre_principal = encontrar_similitud(nombre_entrada)

# if nombre_principal:
#     print(f"El nombre \"{nombre_entrada}\" se relaciona con el nombre principal: \"{nombre_principal}\"")
# else:
#     print("No se encontró una coincidencia cercana con ningún nombre principal.")






