from functions.cleanData import cleanData

def generateData(array = [], fields = []): 
    data = {
        'OtrosDatos': []
    }
    for arr in array:
        if arr[0] in fields:
            data[cleanData(arr[0], True)] = cleanData(arr[1], False)
        else:
            data['OtrosDatos'].append({cleanData(arr[0], True): cleanData(arr[1], False)})
    return data
