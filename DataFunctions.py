import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

# Conexion con la base de datos
def connectionDB(collection):
    load_dotenv()
    MONGODB_URI = os.environ['MONGO_URI']
    connection = MongoClient(MONGODB_URI)
    db = connection.DataCV
    colection = db[collection]
    return colection, connection

# Obtención de todos los documentos de una colección
def RetrieveAllRecords(collection):
    data = []
    mc = connectionDB(collection)
    records = mc[0].find()
    for record in records:
        data.append(record)
    print(f"Records encontrados {len(data)}") if (len(data) != 0) else print("Records no encontrados")
    mc[1].close()
    return data

# Obtención de uno o varios documentos por cualquier campo {field: value}
def RetrieveRecords(collection, record):
    data = []
    mc = connectionDB(collection)
    records = mc[0].find(record)
    for record in records:
        data.append(record)
    print(f"Records encontrados {len(data)}") if (len(data) != 0) else print("Records no encontrados")
    mc[1].close()
    return data
    
# Obtención de un documento por un id (id del documento)
def RetrieveRecordByID(collection, record):
    mc = connectionDB(collection)
    try:
        result = mc[0].find_one({"_id":ObjectId(record)})
        print("Record encontrado") if (result != None) else print("ID no valido")
    except:
        print("Ese no es un ObjectId")
        result = None
    mc[1].close()
    return result

# Insertar un nuevo documento
def InsertRecord(collection, record):
    mc = connectionDB(collection)
    result = mc[0].insert_one(record)
    print("Record insertado") if (result.inserted_id) else print("Record no insertado")
    mc[1].close()

# Actualizar uno o varios documentos por cualquier campo {field: value}, {field: value}
def UpdateRecords(collection, recordAnterior, recordNuevo):
    mc = connectionDB(collection)
    result = mc[0].update_many(recordAnterior, {"$set": recordNuevo})
    print(f"Records actualizados {result.modified_count}") if (result.modified_count != 0) else print("Records no actualizados")
    mc[1].close()

# Actualizar por un id (id del documento), {field: value}
def UpdateRecordByID(collection, recordAnterior, recordNuevo):
    mc = connectionDB(collection)
    try:
        result = mc[0].update_one({"_id":ObjectId(recordAnterior)}, {"$set": recordNuevo})
        print("Record actualizado") if (result.modified_count != 0) else print("Records no actualizados")
    except:
        print("Ese no es un ObjectId")
    mc[1].close()
    
# Borrar uno o varios documentos por cualquier campo {field: value}
def DeleteRecords(collection, record):
    mc = connectionDB(collection)
    result = mc[0].delete_many(record)
    print(f"Records eliminados {result.deleted_count}") if (result.deleted_count != 0) else print("Records no eliminados")
    mc[1].close()

# Borrar por un id (id del documento)
def DeleteRecordByID(collection, record):
    mc = connectionDB(collection)
    try:
        result = mc[0].delete_one({"_id":ObjectId(record)})
        print("Record eliminado por ID") if (result.deleted_count == 1) else print("ID no valido")
    except:
        print("Ese no es un ObjectId")
    mc[1].close()