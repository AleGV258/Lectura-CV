
from functions.cleanData import cleanData
from functions.dataFunctions import connectionDB, retrieveAllRecords, retrieveRecords, retrieveRecordByID, insertRecord, updateRecords, updateRecordByID, deleteRecords, deleteRecordByID
from bson import ObjectId

mc = connectionDB()
bd = mc[0]


def cleanNames(profes='', relacion ={}, nombreTabla='', tablaInsertarRelacion='', idInsert=''):
    data = retrieveAllRecords(bd, "Profesores")
    profesores = set(nombre["Nombre"] for nombre in data)
    nuevosProfesores = set()

    ProfesorLogros = []

    if (len(profes.split(';')) > 1):
        autores = profes.replace(
            '; ', ';').replace('.', '').replace(',', '').split(';')
    else:
        autores = profes.replace(
            ', ', ',').replace('.', '').split(',')

    print('autores:', autores)

    for autor in autores:
        autor = autor.upper().replace('Á', 'A').replace('É', 'E').replace(
            'Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
        contador = 0

        nombreNormalizado = set(autor.split(' '))

        for profesor in profesores:
            nombreNormalizadoBD = set(profesor.split(' '))
            interseccion = nombreNormalizado.intersection(nombreNormalizadoBD)
            # print(nombresAutorSplit, " - \t", nombresSplit, " - \t", len(interseccion), " - \t", interseccion)
            if (len(interseccion) >= 3):
                contador = contador + 1
                break

        for nuevoProfesor in nuevosProfesores:
            nombreNormalizadoBD = set(nuevoProfesor.split(' '))
            interseccion = nombreNormalizado.intersection(nombreNormalizadoBD)
            if (len(interseccion) >= 3):
                contador = contador + 1
                break
        if (contador == 0):
            # print("\nSe agrego: ", autor)
            nuevosProfesores.add(autor)
        # print("\n", len(profesores), " - ", profesores)
        ProfesorLogrosRow = {
            'Autor': cleanData(autor, False),
        }
        # print(ProfesorLogrosRow)
        ProfesorLogros.append(ProfesorLogrosRow)
    # logro['OtrosDatos'][0]['Autor'] = ProfesorLogros

    # Insertar Nuevos Profesores Encontrados
    for nuevoProfesor in nuevosProfesores:
        # if (nombreProfesor != cleanData(profesor, False)):
        record = {
            'Nombre': cleanData(nuevoProfesor, False),
        }
        insertRecord(bd, "Profesores", record)

    data = retrieveAllRecords(bd, "Profesores")
    profesores = {nombre["_id"]: nombre["Nombre"] for nombre in data}
    # Insertar Logros hacía un Profesor
    # print("\nLogros: ", Logros[0])

    # for relacion in tablaRelacion:
    busqueda = retrieveRecords(bd, nombreTabla, relacion)
    if (len(busqueda) == 0):
        rowID = insertRecord(bd, nombreTabla, relacion)
        for autor in ProfesorLogros:
            nombreProfesorSplit = set(autor['Autor'].split(' '))
            for profesorID, profesorNombre in profesores.items():
                profesorNombreSplit = set(profesorNombre.split(' '))
                interseccion = nombreProfesorSplit.intersection(
                    profesorNombreSplit)
                if (len(interseccion) >= 3):
                    objetoAInsertar = {
                        'Nombre': profesorNombre,
                        'IdProfesor': ObjectId(profesorID),
                        idInsert: ObjectId(rowID)
                    }
                    insertRecord(bd, tablaInsertarRelacion, objetoAInsertar)
                    break
