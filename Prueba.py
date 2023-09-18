from functions.dataFunctions import RetrieveAllRecords, RetrieveRecords, RetrieveRecordByID, InsertRecord, UpdateRecords, UpdateRecordByID, DeleteRecords, DeleteRecordByID
from functions.cleanData import cleanData
import difflib

# #### Retrieve All Data
# data = RetrieveAllRecords("Profesores")
# print(data)

# #### Retrieve Data
# record = {"prueba":"prueba"}
# data = RetrieveRecords("Profesores", record)
# print(data)

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
        # return None

# # Nombre de entrada
# nombre_entrada = "IBARRA CORONA DIEGO OCTAVIO"

# # Encontrar la mejor coincidencia
# nombre_principal = encontrar_similitud(nombre_entrada)

# if nombre_principal:
#     print(f"El nombre \"{nombre_entrada}\" se relaciona con el nombre principal: \"{nombre_principal}\"")
# else:
#     print("No se encontró una coincidencia cercana con ningún nombre principal.")






