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
    
    # Get para todos los datos de las tablas

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
    

    

    # Titulos de las tablas
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
    

    # Lista de campos que se buscaran en los datos
    camposProfesor = ["_id", "Nombre", "FechaNacimiento", "IES"]
    camposPROMEP = ["IESSolicitud", "Solicitud", "Vigencia", "Estado", "IdProfesor"]
    camposCuerpoAcademico = ["_id", "NombreCuerpoAcademico", "Clave", "GradoConsolidacion"]
    camposDirecciones = ["TituloTesisProyectoIndividual", "Grado", "EstadoDireccionIndividualizada", "LAGCs"]
    camposDocencias = ["NombreCurso", "InsitucionEducacionSuperior(IES)", "DependenciaEducacionSuperior(IES)"]
    camposGestionAcademica = ["TipoGestion", "CargoDentroComisionCuerpoColegiado", "FuncionEncomendada", "Aprobado", "Estado"]
    camposInvestigacion = ["TituloProyecto", "NombrePatrocinador", "TipoPatrocinador"]
    camposLogros = ["Tipo", "Titulo", "Pais", "Ano"]
    camposProfesorInvestigaciones = ["_id", "Nombre", "IdProfesor", "IdInvestigacion"]
    camposProfesoresLogros = ["Nombre", "IdProfesor", "IdLogro"]
    camposTutorias = ["Tutoria", "Nivel", "ProgramaEducativoParticipa", "EstadoTutelaje"]

    #creacion de las tablas mandando: NOMBRE DEL PDF, CAMPOS DE BUSQUEDA, DATOS DE LA BD, TITULOS DE LA TABLA
    creacionTabla("PROFESOR",  camposProfesor, profesorI, columnasProf)
    creacionTabla("BENEFICIOS_PROMEP",  camposPROMEP, beneficiosPROMEP, columnasPROMEP)
    creacionTabla("CUERPO_ACADEMICO",  camposCuerpoAcademico, cuerpoAcademico, columnasAcademico)
    creacionTabla("DIRECCIONES",  camposDirecciones, direccionIndividualizada, columnasDireccion)
    creacionTabla("DOCENCIAS",  camposDocencias, docencias, columnasDocencias)
    creacionTabla("GESTION_ACADEMICA",  camposGestionAcademica, gestionAcademica, cGAcademica)
    creacionTabla("INVESTIGACION",  camposInvestigacion, investigaciones, cInvestigacion)
    creacionTabla("LOGROS",  camposLogros, logros, cLogros)
    creacionTabla("PROFESOR_INVESTIGACIONES",  camposProfesorInvestigaciones, profesoresInvestigaciones, cProfesoresInvestigacion)
    creacionTabla("PROFESOR_LOGROS",  camposProfesoresLogros, profesorLogros, cProfesoresLogros)
    creacionTabla("TUTORIAS",  camposTutorias, tutorias, cTurorias)


    
    print("DOCUMENTOS CREADO")




def creacionTabla(nombreTabla, camposBusqueda, dataBase, camposTitulo):

    #Añadiendo titulos a la tabla
    dataFinal = [camposTitulo]

    #Repasar cada dato de la data
    for dato in dataBase:
        # Recorre el arreglo de los campos de busqueda para encontrarlos y añadirlos a la lista, si no los encuentra, solo deja el espacio en blanco
        dataFinal.append([dato.get(campo, "") for campo in camposBusqueda])

    
    #Crea el documento, se coloca el nombre y el tamaño
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