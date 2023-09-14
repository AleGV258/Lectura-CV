from DataFunctions import RetrieveAllRecords, RetrieveRecords, RetrieveRecordByID, InsertRecord, UpdateRecords, UpdateRecordByID, DeleteRecords, DeleteRecordByID
from functions.cleanData import cleanData

# string = "Hola mí nombre \t$#%[es michell alejandro y tengo 22 !?¿¡+-<>años de edad, espero llegar a mi casa y viciarme *^^un día más al bendito , juego que me quita ,:;:; mi sanidad mental el LÓL"

# prueba = cleanData(string, False)
# print(prueba)

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







