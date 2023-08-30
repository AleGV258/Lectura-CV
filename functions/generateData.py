def generateData (array = [], fields=[]): 
    data = {
        'OtrosDatos': []
    }
    for arr in array:
        if arr[0] in fields: 
            data[arr[0]] = arr[1]
        else:
            data['OtrosDatos'].append( { arr[0]: arr[1].replace('\r\x07', ", ")})
    return data
