def cleanData(cell, title):
    cell = cell.strip()
    replacesKey = {'\x07':', ', '\x0b':' ', '\xa0':' ', '\r':'', '\n':'', '\t':'', '.':'', ' ,':',', '(es)':'', 'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', 'Á':'A', 'É':'E', 'Í':'I', 'Ó':'O', 'Ú':'U', 'ü':'u', 'Ü':'U', 'ñ':'n', 'Ñ':'N', 'ç':'c', 'Ç':'C', '¿':'', '?':'', '¡':'', '!':'', '*':'', '#':'', '$':'', '%':'', '-':'', '<':'', '>':'', '{':'', '}':'', '[':'', ']':'', ';':'', ':':'', '+':'', '^':'',' de ':' ', ' el ':' ', ' la ':' ', ' los ':' ', ' las ':' ', ' un ':' ', ' una ':' ', ' unos ':' ', ' unas ':' ', ' del ':' ', ' al ':' ', ' por ':' ', ' para ':' ', ' con ':' ', ' sin ':' ', ' sobre ':' ', ' bajo ':' ', ' ante ':' ', ' tras ':' ', ' entre ':' ', ' hacia ':' ', ' hasta ':' ', ' según ':' ', ' durante ':' ', ' mediante ':' ', ' excepto ':' ', ' salvo ':' ', ' aunque ':' ', ' aun ':' ', ' fue ':' ', ' como ':' ', ' cuando ':' ', ' donde ':' ', ' mientras ':' ', ' si ':' ', ' que ':' ', ' en ':' ', ' es ':' ', ' e ':' ', ' y ':' ', ' o ':' ', ' u ':' ', ' a':'A', ' b':'B', ' c':'C', ' d':'D', ' e':'E', ' f':'F', ' g':'G', ' h':'H', ' i':'I', ' j':'J', ' k':'K', ' l':'L', ' m':'M', ' n':'N', ' o':'O', ' p':'P', ' q':'Q', ' r':'R', ' s':'S', ' t':'T', ' u':'U', ' v':'V', ' w':'W', ' x':'X', ' y':'Y', ' z':'Z', ' ':''}
    replacesValue = {'\x07':', ', '\x0b':' ', '\xa0':' ', '\r':'', '\n':'', '\t':'', ' ,':',', '-':' '}
    if(title == True):
        for key, value in replacesKey.items():
            cell = cell.replace(key, value)
    elif(title == False):
        for key, value in replacesValue.items():
            cell = cell.replace(key, value)
    return cell