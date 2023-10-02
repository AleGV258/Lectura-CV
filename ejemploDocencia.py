
docencia = [
    ['Nombre del curso', 'Bases de Datos'], 
    ['Institución de Educación Superior (IES)', 'Universidad Autónoma de Querétaro'], 
    ['Dependencia de Educación Superior (IES)', 'TECNOLOGÍAS DE INFORMACIÓN Y COMUNICACIONES'], 
    ['Programa educativo', 'INFORMATICA'], 
    ['Nivel', 'Licenciatura'], 
    ['Fecha de inicio', 'Número de alumnos', 'Duración en semanas', 'Horas de asesoría al mes', 'Horas semanales dedicadas a este curso'], 
    ['17/01/2022', '19', '18', '1', '4'],
    ['Nombre del curso', 'Bases de Datos I'], 
    ['Institución de Educación Superior (IES)', 'Universidad Autónoma de Querétaro'], 
    ['Dependencia de Educación Superior (IES)', 'TECNOLOGÍAS DE INFORMACIÓN Y COMUNICACIONES'], 
    ['Programa educativo', 'INGENIERIA DE SOFTWARE'], 
    ['Nivel', 'Licenciatura'], 
    ['Fecha de inicio', 'Número de alumnos', 'Duración en semanas', 'Horas de asesoría al mes', 'Horas semanales dedicadas a este curso'], 
    ['17/01/2022', '21', '18', '1', '4'], 
    ['Nombre del curso', 'Desarrollo de Interfaces de Hardware II'], 
    ['Institución de Educación Superior (IES)', 'Universidad Autónoma de Querétaro'], 
    ['Dependencia de Educación Superior (IES)', 'TECNOLOGÍAS DE INFORMACIÓN Y COMUNICACIONES'], 
    ['Programa educativo', 'INGENIERIA EN COMPUTACION'], 
    ['Nivel', 'Licenciatura'], 
    ['Fecha de inicio', 'Número de alumnos', 'Duración en semanas', 'Horas de asesoría al mes', 'Horas semanales dedicadas a este curso'], 
    ['17/01/2022', '13', '18', '1', '4']
]

posicion = 5
separacion = 7

nuevas_filas = int(len(docencia)/7 * 3)
suma = int(len(docencia) + nuevas_filas)

matriz_vacia = [[] for _ in range(suma)]

posiciones = 0
while posicion < len(docencia):
    # print(posicion)
    # print(docencia[posicion], docencia[posicion + 1])
    temp = [[], [], [], [], []]
    for i in range(len(docencia[posicion])):
        temp[i].append(docencia[posicion][i])
        temp[i].append(docencia[posicion + 1][i])

    print(temp)

    for j in range(10):
        if(j < 5 and j+posiciones < len(docencia)):
            # print(posiciones+j, j)
            matriz_vacia[j + posiciones] = docencia[j + posiciones]
        else:
            matriz_vacia[j + posiciones] = temp[j - 5]
        
        print(j + posiciones, matriz_vacia[j + posiciones])
    posiciones = posiciones + 10

    posicion += separacion




