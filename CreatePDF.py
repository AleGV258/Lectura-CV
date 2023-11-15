from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from functions.dataFunctions import connectionDB, retrieveAllRecords, retrieveRecords, retrieveRecordByID, insertRecord, updateRecords, updateRecordByID, deleteRecords, deleteRecordByID
import json
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Frame
from reportlab.lib import colors



def createTable(filtros = {}):
    print("\n Filtros recibidos: ", filtros)
    

    mc = connectionDB()
    db = mc[0]
    
    # Recupera todos los registros de la colección "Profesores" de la base de datos
    #profesorI = retrieveAllRecords(db, "Profesores") #Comentado por que no puedo usar la base de datos xd

    #Prueba estatica de datos
    profesorI = retrieveAllRecords(db, "Profesores")
    beneficiosPROMEP = retrieveAllRecords(db, "BeneficiosPROMEP")
    cuerpoAcademico = retrieveAllRecords(db, "CuerpoAcademico")
    direccionIndividualizada = retrieveAllRecords(db, "DireccionesIndividualizadas")
    docencias = retrieveAllRecords(db, "Docencias")
    gestionAcademica = retrieveAllRecords(db, "GestionesAcademicas")
    investigaciones = retrieveAllRecords(db, "Investigaciones")
    logros = retrieveAllRecords(db, "Logros")
    profesoresInvestigaciones = retrieveAllRecords(db, "ProfesorInvestigaciones")
    profesorLogros = retrieveAllRecords(db, "ProfesorLogros")
    tutorias = retrieveAllRecords(db, "Tutorias")
    

    # Aplicar la función de filtro a los datos si hay alguno
    
    #datosFiltrados1 = filter(filter_func, profesorI)

    # Convertir el resultado filtrado a una lista
    datosFiltrados = profesorI

    # Crear un archivo PDF llamado "tabla_desde_json.pdf"
    

    # Crear una lista de nombres de columnas
    columnasProf = ["_id", "Nombre", "FechaNacimiento", "IES"]
    columnasPROMEP = ["IES Solicitud", "Solicitud", "Vigencia", "Estado", "id Profesor"]
    columnasAcademico = ["id", "Nombre Academico", "clave", "Consolidacion"]
    columnasDireccion = ["Titulo", "grado", "Direccion Individualizada", "LAGCs"]
    columnasDocencias = ["Curso", "Institucion", "Dependencia"]
    cGAcademica = ["Tipo", "Cargo", "Funcion", "Aprobado", "Estado"]
    cInvestigacion = ["Titulo", "Nombre", "Tipo"]
    cLogros = ["Tipo", "Titulo", "pais", "Año"]
    cProfesoresInvestigacion = ["_id", "Nombre", "id_profesor", "id_investigacion"]
    cProfesoresLogros = ["Nombre", "idProfesor", "idLogro"]
    cTurorias = ["Tutoria", "Nivel", "programa", "Estado"]
    #for i in filtros:
    #    columnas.append(i)

    # Crear una lista de listas a partir de los datos filtrados
    dataFinalProf = [columnasProf]
    dataFinalPROMEP = [columnasPROMEP]
    dataFinalAcademicos = [columnasAcademico]
    dataFinalDireccion = [columnasDireccion]
    dataFinalDocencias = [columnasDocencias]
    dataFinalGAcademicas = [cGAcademica]
    dataFinalInvestigacion = [cInvestigacion]
    dataFinalLogros = [cLogros]
    dataFinalPinvestifaciones = [cProfesoresInvestigacion]
    dataFinalPLogros = [cProfesoresLogros]
    dataFinalTutorias = [cTurorias]

    for profesor in datosFiltrados:
        dataFinalProf.append([
            profesor.get("_id", ""),
            profesor.get("Nombre", ""),
            profesor.get("FechaNacimiento", ""),
            profesor.get("IES", "")
        ])

    for promep in beneficiosPROMEP: 
        dataFinalPROMEP.append([
            promep.get("IESSolicitud", ""),
            promep.get("Solicitud", ""),
            promep.get("Vigencia", ""),
            promep.get("Estado", ""),
            promep.get("IdProfesor", "") 
        ])

    for academicos in cuerpoAcademico:
        dataFinalAcademicos.append([
            academicos.get("_id", ""),
            academicos.get("NombreCuerpoAcademico"),
            academicos.get("Clave"),
            academicos.get("GradoConsolidacion"),
        ]) 

    for direccion in direccionIndividualizada:
        dataFinalDireccion.append([
            direccion.get("TituloTesisProyectoIndividual", ""),
            direccion.get("Grado", ""),
            direccion.get("EstadoDireccionIndividualizada", ""),
            direccion.get("LAGCs"),
        ])
    for docencia in docencias:
        dataFinalDocencias.append([
            docencia.get("NombreCurso", ""),
            docencia.get("InsitucionEducacionSuperior(IES)"),
            docencia.get("DependenciaEducacionSuperior(IES)"),
        ])

    for GAcademica in gestionAcademica: 
        dataFinalGAcademicas.append([
            GAcademica.get("TipoGestion", ""),
            GAcademica.get("CargoDentroComisionCuerpoColegiado", ""),
            GAcademica.get("FuncionEncomendada", ""),
            GAcademica.get("Aprobado", ""),
            GAcademica.get("Estado", ""),
        ])

    for investigacion in investigaciones:
        dataFinalInvestigacion.append([
            investigacion.get("TituloProyecto", ""),
            investigacion.get("NombrePatrocinador", ""),
            investigacion.get("TipoPatrocinador")
        ])

    for logro in logros:
        dataFinalLogros.append([
            logro.get("Tipo", ""),
            logro.get("Titulo", ""),
            logro.get("Pais", ""),
            logro.get("Ano", ""),
        ])
    
    for pInvestigacion in profesoresInvestigaciones:
        dataFinalPinvestifaciones.append([
            pInvestigacion.get("_id", ""),
            pInvestigacion.get("Nombre", ""),
            pInvestigacion.get("IdProfesor", ""),
            pInvestigacion.get("IdInvestigacion", "")
        ])

    for pLogro in profesorLogros:
        dataFinalPLogros.append([
            pLogro.get("Nombre", ""),
            pLogro.get("IdProfesor", ""),
            pLogro.get("IdLogro", "")
        ])

    for tutoria in tutorias:
        dataFinalTutorias.append([
            tutoria.get("Tutoria", ""),
            tutoria.get("Nivel", ""),
            tutoria.get("ProgramaEducativoParticipa", ""),
            tutoria.get("EstadoTutelaje", "")
        ])



    creacionTabla("Profesor", dataFinalProf)
    creacionTabla("PROMEP", dataFinalPROMEP)
    creacionTabla("Academicos", dataFinalAcademicos)
    creacionTabla("Direccion", dataFinalDireccion)
    creacionTabla("Docencias", dataFinalDocencias)
    creacionTabla("Gestion Academica", dataFinalGAcademicas)
    creacionTabla("Investigaciones", dataFinalInvestigacion)
    creacionTabla("Logros", dataFinalLogros)
    creacionTabla("Profesores Investigaciones", dataFinalPinvestifaciones)
    creacionTabla("Profesores Logros", dataFinalPLogros)
    creacionTabla("Tutorias", dataFinalTutorias)
    
    
    print("DOCUMENTOS CREADO")




def creacionTabla(nombreTabla, dataFinal):

    doc = SimpleDocTemplate(nombreTabla+".pdf", pagesize=letter)
    # Crear una tabla con los datos
    tabla = Table(dataFinal)

    # Aplicar estilo a la tabla
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, '#27a39d'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Borde interno
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ])

    tabla.setStyle(estilo)

    # Crear el objeto Story y agregar la tabla al contenido
    story = []
    story.append(tabla)

    # Construir el PDF
    doc.build(story)