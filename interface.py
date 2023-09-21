import tkinter as tk
from tkinter import filedialog, font
import os
from LecturaCV import lecturaCV

backgroundColor = "#f3f3f4"
fTitle= ("Arial", 15, "bold")
fText = ("Arial", 10)
fBotton = ("Arial", 13)

folder_path = ""
documentosArray = []


def toggle_input():
    if filtro_autor.get() == True:
        entry1.grid(row=1, column=0, padx=5, pady=5)
    else:
        entry1.grid_forget()

    if filtro_anio.get() == True:
        entry2.grid(row=3, column=0, padx=5, pady=5)
    else:
        entry2.grid_forget()
    
    if filtro_documento.get() == True:
        entry3.grid(row=5, column=0, padx=5, pady=5)
    else:
        entry3.grid_forget()
    
    if filtro_area_conocimiento.get() == True:
        entry4.grid(row=7, column=0, padx=5, pady=5)
    else:
        entry4.grid_forget()
        
def crear_etiquetas(documentos=[]):
    counter = 0
    for document in documentos:
        counter = counter + 1
        print(document)
        tk.Label(listado, font=fText,text=document, bg=backgroundColor).grid(row=counter, padx=10, pady=5)

def select_folder():
    global folder_path
    global documentosArray
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_label.config(text=f"Carpeta: {folder_path}")
        documents =  os.listdir(folder_path) # Ruta de los archivos
        print(documents)
        crear_etiquetas(documents)
        documentosArray = documents

# Create the main window
root = tk.Tk()
root.title("Formulario")
root.configure(bg='white')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{int(screen_width*0.53)}x{int(screen_height*0.8)}")
# root.attributes('-fullscreen', True)
# root.geometry("800x600")
# root.attributes('-transparentcolor', 'grey')
# Create a frame to contain

folder_frame = tk.Frame(root, bg=backgroundColor)
folder_frame.pack(pady=20)
# Create a label to display the selected folder path
folder_path_label = tk.Label(folder_frame, text="Seleccionar carpeta:", font=fText,padx=10, pady=10, bg=backgroundColor)
folder_path_label.pack(side="left")
# Create a button to open the folder selection dialog
select_button = tk.Button(folder_frame, text="Seleccionar Carpeta",font=fBotton, command=select_folder)
select_button.pack(side="left")

# for font in font.families():
#     print(font)

# Frame para checkboxes
select_tables_frame = tk.Frame(root,  bg=backgroundColor)
select_tables_frame.pack()
# select_tables_frame.config(width=nuevo_ancho, height=nuevo_alto)
titulo = tk.Label(select_tables_frame, text="Seleccionar tablas para insertar a la base de datos", font=fTitle, bg=backgroundColor)
titulo.grid(row=0, padx=140, pady=10)

checkBoxes_frame = tk.Frame(select_tables_frame,bg=backgroundColor)
checkBoxes_frame.grid(row=1, padx=30)
# Agregar contenido a la segunda columna (columna 0)
check_info_Profesor = tk.BooleanVar()
check_button = tk.Checkbutton(checkBoxes_frame, text="Información del Profesor", font=fText, variable=check_info_Profesor,  bg=backgroundColor)
check_button.grid(row=0, column=0,sticky="W", padx=30, pady=2)

check_logros_Profesor = tk.BooleanVar()
check_button = tk.Checkbutton(checkBoxes_frame, text="Logros del Profesor", font=fText,variable=check_logros_Profesor,  bg=backgroundColor)
check_button.grid(row=1, column=0,sticky="W", padx=30, pady=2)

check_invest_Profesor = tk.BooleanVar()
check_button = tk.Checkbutton(checkBoxes_frame, text="Investigaciones del Profesor", font=fText,variable=check_invest_Profesor,  bg=backgroundColor)
check_button.grid(row=2, column=0,sticky="W", padx=30, pady=2)

check_gest_academica = tk.BooleanVar()
check_button = tk.Checkbutton(checkBoxes_frame, text="Gestión Académica", font=fText,variable=check_gest_academica,  bg=backgroundColor)
check_button.grid(row=3, column=0,sticky="W", padx=30, pady=2)

check_docencias = tk.BooleanVar()
check_button = tk.Checkbutton(checkBoxes_frame, text="Docencias", font=fText,variable=check_docencias,  bg=backgroundColor)
check_button.grid(row=4, column=0,sticky="W", padx=30, pady=2)

# Agregar contenido a la segunda columna (columna 1)
check_benf_promep = tk.BooleanVar()
check_button = tk.Checkbutton(checkBoxes_frame, text="Beneficios PROMEP", font=fText,variable=check_benf_promep,  bg=backgroundColor)
check_button.grid(row=0, column=1,sticky="W", padx=30, pady=2)

check_cuerpo_academico = tk.BooleanVar()
check_button = tk.Checkbutton(checkBoxes_frame, text="Cuerpo Académico", font=fText,variable=check_cuerpo_academico,  bg=backgroundColor)
check_button.grid(row=1, column=1,sticky="W", padx=30, pady=2)

check_prog_academicos = tk.BooleanVar()
check_button = tk.Checkbutton(checkBoxes_frame, text="Programas Académicos",font=fText, variable=check_prog_academicos,  bg=backgroundColor)
check_button.grid(row=2, column=1,sticky="W", padx=30, pady=2)

check_tutorias = tk.BooleanVar()
check_button = tk.Checkbutton(checkBoxes_frame, text="Tutorías", font=fText,variable=check_tutorias,  bg=backgroundColor)
check_button.grid(row=3, column=1,sticky="W", padx=30, pady=2)

check_dir_individualizada = tk.BooleanVar()
check_button = tk.Checkbutton(checkBoxes_frame, text="Dirección Individualizada",font=fText,variable=check_dir_individualizada,  bg=backgroundColor)
check_button.grid(row=4, column=1,sticky="W", padx=30, pady=2)



columns = tk.Frame(root, bg=backgroundColor)
columns.pack(pady=30)
titulo = tk.Label(columns, text="Filtros", font=fTitle, bg=backgroundColor)
titulo.grid(row=0, padx=170,pady=10)

filters = tk.Frame(columns, bg=backgroundColor)
filters.grid(row=1, column=0, padx=30)


#Campos
filtro_autor = tk.BooleanVar()
check_button = tk.Checkbutton(filters, text="Filtrar por autor", font=fText, variable=filtro_autor, command=toggle_input, bg=backgroundColor)
check_button.grid(row=0, column=0,sticky="W", padx=30, pady=2)
# filtro_autor.trace("w", toggle_entry)
# print("\nFiltro: ",filtro_autor)

entry1 = tk.Entry(filters)
entry2 = tk.Entry(filters)
entry3 = tk.Entry(filters)
entry4 = tk.Entry(filters)
# entry1 = tk.Entry(filters, state=tk.DISABLED)
# entry1.grid(row=0, column=1, padx=5, pady=5)



filtro_anio = tk.BooleanVar()
check_button = tk.Checkbutton(filters, text="Filtrar por año",font=fText, variable=filtro_anio, command=toggle_input, bg=backgroundColor)
check_button.grid(row=2, column=0,sticky="W", padx=30, pady=2)

filtro_documento = tk.BooleanVar()
check_button = tk.Checkbutton(filters, text="Filtrar por tipo de documento", font=fText,variable=filtro_documento, command=toggle_input, bg=backgroundColor)
check_button.grid(row=4, column=0,sticky="W", padx=30, pady=2)

filtro_area_conocimiento = tk.BooleanVar()
check_button = tk.Checkbutton(filters, text="Filtrar por area de conocimiento", font=fText,variable=filtro_area_conocimiento, command=toggle_input, bg=backgroundColor)
check_button.grid(row=6, column=0,sticky="W", padx=30, pady=2)





titulo_directorio = tk.Label(columns, text="Archivos encontrados en Directorio", font=fTitle)
titulo_directorio.grid(row=0, column=1, padx=10, pady=10, )
# Listado de documentos encontrados
listado = tk.Frame(columns, bg=backgroundColor)
listado.grid(row=1, column=1, sticky="n")
# listado.grid(sticky="n")


        
# tk.Label(listado, text="Seleccionar carpeta:", padx=10, pady=10).grid(row=1, column=0, padx=30)
# tk.Label(listado, text="Seleccionar carpeta:", padx=10, pady=10).grid(row=2, column=0, padx=30)
crear_etiquetas()

def exportDocument():
    print("Exportando")

    SelectedTables={
        "InfoProfesor": check_info_Profesor.get(),
        "LogrosProfesor": check_logros_Profesor.get(),
        "InvestigacionesProfesor": check_invest_Profesor.get(),
        "GestionAcademica": check_gest_academica.get(),
        "Docencias": check_docencias.get(),
        "BeneficiosPROMEP": check_benf_promep.get(),
        "CuerpoAcademico": check_cuerpo_academico.get(),
        "ProgramasAcademicos": check_prog_academicos.get(),
        "Tutorias": check_tutorias.get(),
        "DireccionIndividualizada": check_dir_individualizada.get()
    }
    Filters = {
        "autor":{"estado": filtro_autor, "data":}
        "anio":{"estado": filtro_anio, "data":}
        "documento":{"estado": filtro_documento, "data":}
        "areaConocimiento":{"estado": filtro_area_conocimiento, "data":}
    }
    
    print(SelectedTables)
    print(Filters)
    # print(folder_path)
    # print(documentosArray)
    lecturaCV(folder_path, documentosArray)
    # msg=messagebox.showinfo( "Hello Python", "Hello World")



button_frame = tk.Frame(root, bg="white")
button_frame.pack()

export_button = tk.Button(button_frame, text ="Exportar Informe", font=fBotton,command = exportDocument)
export_button.place(x=0,y=0)
export_button.grid( pady=0)
# Start the Tkinter main loop
root.mainloop()