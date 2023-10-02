from functions.generateData import generateData
from functions.cleanData import cleanData

def createDictionary(array = [], fields = [], separatorWord = ''):
    counter = 0
    result = []
    container = []
    inserted = False
    for row in array: 
        if row[0] == separatorWord and counter != 0: 
            inserted = True
            # print("\n Nuevo logro",row) 
        if inserted:            
            dictionary = generateData(container, fields)
            # print("\nDiccionario: ", dictionary)   
            result.append(dictionary)
            
            container = []
            inserted = False
        container.append(row)
        # print("\n Entra",row)            
        counter = counter + 1
        if counter == len(array):
            dictionary = generateData(container, fields)
            result.append(dictionary)
            
    return result


def horizontalTable(array = []):
    fields = array[0];
    
    counter = 0
    result = []
    
    for row in array: 
        # print("\nRow:",row)
        if counter > 0: 
            dictionary = {}
            for i in range(len(fields)):
                # print("\n",fields[i], ": ", row[i])
                dictionary[cleanData(fields[i], True)] =cleanData(row[i], False)
            result.append(dictionary)            
        counter = counter + 1
            
    return result

def dictionaryMixTable(array=[], fields=[], separatorWord='', horizontalWord='Fecha de inicio'):
    counter = 0
    result = []
    container = []
    inserted = False

    isHorizontal = False
    valuesHorizontal = []

    for row in array:
        if row[0] == separatorWord and counter != 0:
            inserted = True
            isHorizontal = False
            # print("\n Nuevo logro",row)
        if inserted:
            dictionary = generateData(container, fields)
            # print("\nDiccionario: ", dictionary)
            container = []
            inserted = False
            
            fieldsHorizontal = valuesHorizontal[0]
            # print("\nValues:", fieldsHorizontal)
            counterHor = 0
            for nRow in valuesHorizontal:
                if counterHor > 0:                    
                    for i in range(len(fieldsHorizontal)):
                        dictionary[cleanData(fieldsHorizontal[i], True)] = cleanData(nRow[i], False)
                counterHor = counterHor + 1
            
            result.append(dictionary)

        if row[0] == horizontalWord:
            isHorizontal = True

        if isHorizontal == True:
            valuesHorizontal.append(row)
        else:
            container.append(row)
        # print("\n Entra",row)
        counter = counter + 1
        if counter == len(array):
            dictionary = generateData(container, fields)
            result.append(dictionary)

    return result