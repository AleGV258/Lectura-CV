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
    print(f"Records encontrados {len(data)} en colección {collection}") if (len(data) > 0) else print(f"Records no encontrados en colección {collection}")
    mc[1].close()
    return data

# Obtención de uno o varios documentos por cualquier campo {field: value}
def RetrieveRecords(collection, record):
    data = []
    mc = connectionDB(collection)
    records = mc[0].find(record)
    for record in records:
        data.append(record)
    print(f"Records encontrados {len(data)} en colección {collection}") if (len(data) > 0) else print(f"Records no encontrados en colección {collection}")
    mc[1].close()
    return data
    
# Obtención de un documento por un id (id del documento)
def RetrieveRecordByID(collection, record):
    mc = connectionDB(collection)
    try:
        result = mc[0].find_one({"_id":ObjectId(record)})
        print(f"Record encontrado en colección {collection} con ID: {record}") if (result != []) else print(f"ID no valido en colección {collection} con ID: {record}")
    except:
        print(f"Ese no es un ObjectId en colección {collection}: {record}")
        result = []
    mc[1].close()
    return result

# Insertar un nuevo documento
def InsertRecord(collection, record):
    mc = connectionDB(collection)
    result = mc[0].insert_one(record)
    mc[1].close()
    if (result.inserted_id):
        print(f"Record insertado en colección {collection} con ID: {result.inserted_id}")
        return result.inserted_id
    else:
        print(f"Record no insertado en colección {collection}")
        return []

# Actualizar uno o varios documentos por cualquier campo {field: value}, {field: value}
def UpdateRecords(collection, recordAnterior, recordNuevo):
    mc = connectionDB(collection)
    result = mc[0].update_many(recordAnterior, {"$set": recordNuevo})
    mc[1].close()
    if (result.modified_count > 0):
        print(f"Records actualizados {result.modified_count} en colección {collection} con ID: {result.upserted_id}")
        return result.upserted_id
    else:
        print(f"Records no actualizados en colección {collection}")
        return []
    
# Actualizar por un id (id del documento), {field: value}
def UpdateRecordByID(collection, recordAnterior, recordNuevo):
    mc = connectionDB(collection)
    try:
        result = mc[0].update_one({"_id":ObjectId(recordAnterior)}, {"$set": recordNuevo})
        print(f"Record actualizado en colección {collection} con ID: {result.upserted_id}") if (result.modified_count > 0) else print(f"Records no actualizados en colección {collection}")
    except:
        print(f"Ese no es un ObjectId en colección {collection} con ID: {recordAnterior}")
    mc[1].close()
    
# Borrar uno o varios documentos por cualquier campo {field: value}
def DeleteRecords(collection, record):
    mc = connectionDB(collection)
    result = mc[0].delete_many(record)
    print(f"Records eliminados {result.deleted_count} en colección {collection}") if (result.deleted_count > 0) else print(f"Records no eliminados en colección {collection}")
    mc[1].close()

# Borrar por un id (id del documento)
def DeleteRecordByID(collection, record):
    mc = connectionDB(collection)
    try:
        result = mc[0].delete_one({"_id":ObjectId(record)})
        print(f"Record eliminado por ID en colección {collection} con ID: {record}") if (result.deleted_count == 1) else print(f"ID no valido en colección {collection}")
    except:
        print(f"Ese no es un ObjectId en colección {collection} con ID: {record}")
    mc[1].close()