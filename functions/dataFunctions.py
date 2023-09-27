import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

# Conexion con la base de datos
def connectionDB():
    load_dotenv()
    MONGODB_URI = os.environ['MONGO_URI']
    connection = MongoClient(MONGODB_URI)
    db = connection.DataCV
    return db, connection

# Obtención de todos los documentos de una colección
def retrieveAllRecords(db, collection):
    data = []
    records = db[collection].find()
    for record in records:
        data.append(record)
    print(f"Records encontrados {len(data)} en colección {collection}") if (len(data) > 0) else print(f"Records no encontrados en colección {collection}")
    return data

# Obtención de uno o varios documentos por cualquier campo {field: value}
def retrieveRecords(db, collection, record):
    data = []
    records = db[collection].find(record)
    for record in records:
        data.append(record)
    print(f"Records encontrados {len(data)} en colección {collection}") if (len(data) > 0) else print(f"Records no encontrados en colección {collection}")
    return data
    
# Obtención de un documento por un id (id del documento)
def retrieveRecordByID(db, collection, record):
    try:
        result = db[collection].find_one({"_id":ObjectId(record)})
        print(f"Record encontrado en colección {collection} con ID: {record}") if (result != []) else print(f"ID no valido en colección {collection} con ID: {record}")
    except:
        print(f"Ese no es un ObjectId en colección {collection}: {record}")
        result = []
    return result

# Insertar un nuevo documento
def insertRecord(db, collection, record):
    result = db[collection].insert_one(record)
    if (result.inserted_id):
        print(f"Record insertado en colección {collection} con ID: {result.inserted_id}")
        return result.inserted_id
    else:
        print(f"Record no insertado en colección {collection}")
        return []

# Actualizar uno o varios documentos por cualquier campo {field: value}, {field: value}
def updateRecords(db, collection, recordAnterior, recordNuevo):
    result = db[collection].update_many(recordAnterior, {"$set": recordNuevo})
    if (result.modified_count > 0):
        print(f"Records actualizados {result.modified_count} en colección {collection} con ID: {result.upserted_id}")
        return result.upserted_id
    else:
        print(f"Records no actualizados en colección {collection}")
        return recordAnterior["_id"]
    
# Actualizar por un id (id del documento), {field: value}
def updateRecordByID(db, collection, recordAnterior, recordNuevo):
    try:
        result = db[collection].update_one({"_id":ObjectId(recordAnterior)}, {"$set": recordNuevo})
        print(f"Record actualizado en colección {collection} con ID: {result.upserted_id}") if (result.modified_count > 0) else print(f"Records no actualizados en colección {collection}")
    except:
        print(f"Ese no es un ObjectId en colección {collection} con ID: {recordAnterior}")
    
# Borrar uno o varios documentos por cualquier campo {field: value}
def deleteRecords(db, collection, record):
    result = db[collection].delete_many(record)
    print(f"Records eliminados {result.deleted_count} en colección {collection}") if (result.deleted_count > 0) else print(f"Records no eliminados en colección {collection}")

# Borrar por un id (id del documento)
def deleteRecordByID(db, collection, record):
    try:
        result = db[collection].delete_one({"_id":ObjectId(record)})
        print(f"Record eliminado por ID en colección {collection} con ID: {record}") if (result.deleted_count == 1) else print(f"ID no valido en colección {collection}")
    except:
        print(f"Ese no es un ObjectId en colección {collection} con ID: {record}")