from functions.generateData import generateData

def createDictionary(array = [], fields = [], separatorWord=''):
    counter=0
    result = []
    container = []
    inserted = False
    for row in array: 
        if row[0] == separatorWord and counter != 0: 
            inserted = True
        
        if inserted:            
            dictionary = generateData(container, fields)
            # print("\nDiccionario: ",dictionary)    
            result.append(dictionary)
            
            container = []
            inserted = False
        container.append(row)            
        counter = counter + 1
    
    
    
    return result
    
def tablePromep(array = [], fields = [], separatorWord=''):
    
    backtothefuture = {}
    field = array[0]; 
    date = array[1]
    cont = 0
    
    for title in field:
        backtothefuture[title] = date[cont]     
        cont += 1
    
    
    
    
    
    return backtothefuture