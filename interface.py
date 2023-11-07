import tkinter as tk
from tkinter import filedialog
from pygubu.widgets.tkscrolledframe import TkScrolledFrame
from LecturaCV import lecturaCV
from CreatePDF import createTable
import time
import os
import threading
import queue

class InterfazCV:
    def __init__(self, master=None):
        # Variables
        self.selectedTables = {}
        self.folderPath = ""
        self.documentosArray = []
        self.queue = queue.Queue()
        
        # Master
        self.master = master
        self.master.resizable(False, False)
        
        # Frame Principal
        self.frm_principal = tk.Frame(master)
        self.frm_principal.configure(
            background="#E9E0EB",
            relief="flat",
            takefocus=True)
        self.frm_principal.grid(column=1, row=1, sticky="nsew")
        
        # Label de Título de la App
        self.label_titulo = tk.Label(self.frm_principal)
        self.label_titulo.configure(
            background="#1B1725",
            compound="top",
            font="{Glacial Indifference} 20 {bold}",
            foreground="#ffffff",
            justify="center",
            pady=15,
            relief="flat",
            state="normal",
            text='Lectura de Curriculums',
            width=0)
        self.label_titulo.grid(column=0, columnspan=2, row=0, sticky="ew")
        
        # Botón de Panel de Exportar
        self.btn_exportar = tk.Button(self.frm_principal)
        self.btn_exportar.configure(
            background="#82589F",
            borderwidth=1,
            cursor="circle",
            state="normal",
            disabledforeground="#000",
            font="{Glacial Indifference} 16 {bold}",
            foreground="#fff",
            justify="center",
            overrelief="flat",
            pady=6,
            relief="flat",
            text='Exportar Información',
            width=50,
            command=self.mostrar_frm_exportar)
        self.btn_exportar.grid(column=1, row=1)
        
        # Botón de Panel de Importar
        self.btn_importar = tk.Button(self.frm_principal)
        self.btn_importar.configure(
            background="#E9E0EB",
            borderwidth=1,
            cursor="arrow",
            state="disabled",
            disabledforeground="#000",
            font="{Glacial Indifference} 16 {bold}",
            foreground="#fff",
            justify="center",
            overrelief="flat",
            pady=6,
            relief="flat",
            text='Importar Datos',
            width=50,
            command=self.mostrar_frm_importar)
        self.btn_importar.grid(column=0, row=1)
        
        # Frame que contiene todo lo de Importar
        self.frm_importar = tk.Frame(self.frm_principal)
        self.frm_importar.configure(background="#E9E0EB", height=200)
        
        # Botón para seleccionar Directorio
        self.btn_path = tk.Button(self.frm_importar)
        self.btn_path.configure(
            background="#534B62",
            borderwidth=0,
            cursor="circle",
            default="active",
            font="{Glacial Indifference} 16 {bold}",
            foreground="#fff",
            justify="center",
            overrelief="flat",
            pady=6,
            relief="flat",
            takefocus=True,
            text='Seleccionar Carpeta',
            width=30,
            command=self.select_folder)
        self.btn_path.grid(column=0, columnspan=2, padx="400 0", row=0)
        self.agregar_efecto_hover(self.btn_path)
        
        # Frame para los checkboxes de Importar
        self.frm_tablas = tk.Frame(self.frm_importar)
        self.frm_tablas.configure(background="#AF9EB7", height=200, width=700)
        self.frm_tablas.grid(column=0, ipady=15, padx=20, row=1, sticky="nsew")
        
        # Label de Título para los checkboxes
        self.label_checkboxes = tk.Label(self.frm_tablas)
        self.label_checkboxes.configure(
            background="#AF9EB7",
            font="{Glacial Indifference} 16 {bold}",
            justify="center",
            relief="flat",
            text='Seleccionar Tablas para\nInsertar en la Base de Datos:',
            width=56)
        self.label_checkboxes.grid(column=0, columnspan=2, pady=20, row=0)
        
        # Checkbox de Logros Profesores
        self.check_logros_Profesor = tk.BooleanVar()
        self.check_logros = tk.Checkbutton(self.frm_tablas)
        self.check_logros.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="left",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Logros de Profesor',
            variable=self.check_logros_Profesor)
        self.check_logros.grid(column=0, padx=40, pady=15, row=2, sticky="w")
        
        # Checkbox de Cuerpo Académico
        self.check_cuerpo_academico = tk.BooleanVar()
        self.check_cuerpo = tk.Checkbutton(self.frm_tablas)
        self.check_cuerpo.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="center",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Cuerpo Académico',
            variable=self.check_cuerpo_academico)
        self.check_cuerpo.grid(column=1, padx=40, pady=20, row=2, sticky="w")
        
        # Checkbox de Investigaciones
        self.check_invest_Profesor = tk.BooleanVar()
        self.check_investigaciones = tk.Checkbutton(self.frm_tablas)
        self.check_investigaciones.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="left",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Investigaciones de Profesor',
            variable=self.check_invest_Profesor)
        self.check_investigaciones.grid(
            column=0, padx=40, pady=0, row=3, sticky="w")
        
        # Checkbox de Programas Académicos
        self.check_prog_academicos = tk.BooleanVar()
        self.check_programas = tk.Checkbutton(self.frm_tablas)
        self.check_programas.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="center",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Programas Académicos',
            variable=self.check_prog_academicos)
        self.check_programas.grid(column=1, padx=40, row=3, sticky="w")
        
        # Checkbox de Gestión Académica
        self.check_gest_academica = tk.BooleanVar()
        self.check_gestion = tk.Checkbutton(self.frm_tablas)
        self.check_gestion.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="left",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Gestión Académica',
            variable=self.check_gest_academica)
        self.check_gestion.grid(column=0, padx=40, pady=15, row=4, sticky="w")
        
        # Checkbox de Tutorías
        self.check_tutorias_Profesor = tk.BooleanVar()
        self.check_tutorias = tk.Checkbutton(self.frm_tablas)
        self.check_tutorias.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="center",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Tutorías',
            variable=self.check_tutorias_Profesor)
        self.check_tutorias.grid(column=1, padx=40, pady=20, row=4, sticky="w")
        
        # Checkbox de Docencias
        self.check_docencias_Profesor = tk.BooleanVar()
        self.check_docencias = tk.Checkbutton(self.frm_tablas)
        self.check_docencias.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="center",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Docencias',
            variable=self.check_docencias_Profesor)
        self.check_docencias.grid(column=0, padx=40, pady=0, row=5, sticky="w")
        
        # Checkbox de Direcciones Individualizadas
        self.check_dir_individualizada = tk.BooleanVar()
        self.check_direccion = tk.Checkbutton(self.frm_tablas)
        self.check_direccion.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="center",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Dirección Individualizada',
            variable=self.check_dir_individualizada)
        self.check_direccion.grid(column=1, padx=40, row=5, sticky="w")
        
        # Checkbox de Beneficios PROMEP
        self.check_benf_promep = tk.BooleanVar()
        self.check_promep = tk.Checkbutton(self.frm_tablas)
        self.check_promep.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="center",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Beneficios PROMEP',
            variable=self.check_benf_promep)
        self.check_promep.grid(column=1, padx=40, row=1, sticky="w")
        
        # Checkbox de Todos los checkbox anteriores
        self.check_todo_Profesor = tk.BooleanVar()
        self.check_todo = tk.Checkbutton(self.frm_tablas)
        self.check_todo.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="left",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Seleccionar todas las Tablas',
            variable=self.check_todo_Profesor,
            command=self.check_todo_selected)
        self.check_todo.grid(column=0, padx=40, row=1, sticky="w")
        
        # Canvas para los archivos encontrados en el directorio
        self.cnv_archivos = tk.Canvas(self.frm_importar)
        self.cnv_archivos.configure(background="#AF9EB7", bd=2, highlightthickness=1, highlightbackground='#AF9EB7')
        self.cnv_archivos.grid(column=1, ipady=15, padx=20, row=1, sticky="nsew")
        
        # Label de Título para los archivos encontrados en el directorio
        self.label_archivos = tk.Label(self.cnv_archivos)
        self.label_archivos.configure(
            background="#AF9EB7",
            font="{Glacial Indifference} 16 {bold}",
            justify="center",
            relief="flat",
            text='Archivos Encontrados\nen Directorio',
            width=30)
        self.label_archivos.grid(column=0, pady=20, row=0)
        
        # Scroll para los archivos encontrados en el directorio
        self.scroll_archivos = TkScrolledFrame(
            self.cnv_archivos, scrolltype="vertical")
        self.scroll_archivos.innerframe.configure(background="#AF9EB7")
        self.scroll_archivos.configure(usemousewheel=True)
        self.scroll_archivos.grid(column=0, ipadx=86, ipady=22, row=1)
                
        # Label placeholder de los archivos econtrados
        self.label_archivo = tk.Label(self.scroll_archivos.innerframe)
        self.label_archivo.configure(
            background="#AF9EB7",
            font="{Glacial Indifference} 16 {}",
            justify="center",
            relief="flat",
            state="normal",
            text='No se encontraron archivos\nen el directorio específicado',
            width=30,
            wraplength=400)
        self.label_archivo.grid(column=0, padx=20, pady=20, row=1)
        
        # Separador de archivos
        self.separator = tk.Frame(self.scroll_archivos.innerframe)
        self.separator.configure(background="#000", height=2, width=300)
        self.separator.grid(column=0, row=0)
        
        # Label donde se coloca texto proveniente con la información del script
        self.label_notificacion_importar = tk.Label(self.frm_importar)
        self.label_notificacion_importar.configure(
            background="#E9E0EB",
            font="{Glacial Indifference} 16 {bold}",
            foreground="#808080",
            wraplength=1100,
            text='Carga el directorio con los archivos (Curriculums) que deseas cargar a la base de datos')
        self.label_notificacion_importar.grid(
            column=0, columnspan=2, pady=30, row=4)
        
        # Botón para importar la información encontrada a la Base de Datos
        self.btn_BaseDatos = tk.Button(self.frm_importar)
        self.btn_BaseDatos.configure(
            background="#534B62",
            borderwidth=0,
            cursor="circle",
            default="active",
            font="{Glacial Indifference} 16 {bold}",
            foreground="#fff",
            justify="center",
            overrelief="flat",
            pady=6,
            relief="flat",
            takefocus=True,
            text='Cargar Datos en la Base de Datos',
            width=60,
            command=self.importar_informacion)
        self.btn_BaseDatos.grid(column=0, columnspan=2, pady="0 30", row=5)
        self.agregar_efecto_hover(self.btn_BaseDatos)
        
        # Label para el path del directorio seleccionado
        self.label_path = tk.Label(self.frm_importar)
        self.label_path.configure(
            background="#E9E0EB",
            font="{Glacial Indifference} 16 {}",
            justify="left",
            wraplength=500,
            text='Selecciona el Directorio:')
        self.label_path.grid(
            column=0,
            columnspan=2,
            padx="0 250",
            pady=30,
            row=0)
        
        # Frame que contiene todo lo de Importar
        self.frm_importar.grid(column=0, columnspan=2, row=2, sticky="ew")
        self.frm_importar.grid_anchor("center")
        
        # Frame que contiene todo lo de Exportar
        self.frm_exportar = tk.Frame(self.frm_principal)
        self.frm_exportar.configure(background="#E9E0EB", height=200)
        self.frm_exportar.grid_anchor("center")
        self.frm_exportar.bind("<Visibility>", self.false, add="")
        
        # Label donde se coloca texto proveniente con la información del script
        self.label_notificacion_exportar = tk.Label(self.frm_exportar)
        self.label_notificacion_exportar.configure(
            background="#E9E0EB",
            font="{Glacial Indifference} 16 {bold}",
            foreground="#808080",
            wraplength=1100,
            text='Exporta la información de la base de datos a un Informe')
        self.label_notificacion_exportar.grid(column=0, pady=30, row=1)
        
        # Botón para exportar por ciertos filtros hacía un Informe
        self.btn_informe = tk.Button(self.frm_exportar)
        self.btn_informe.configure(
            background="#534B62",
            borderwidth=0,
            cursor="circle",
            default="active",
            font="{Glacial Indifference} 16 {bold}",
            foreground="#fff",
            justify="center",
            overrelief="flat",
            pady=6,
            relief="flat",
            takefocus=True,
            text='Exportar la información a un Informe',
            width=60,
            command=self.exportar_informe)
        self.btn_informe.grid(column=0, pady="0 30", row=2)
        
        # Frame donde se encuentran los Inputs de los filtros
        self.frm_filtros = tk.Frame(self.frm_exportar)
        self.frm_filtros.configure(background="#AF9EB7", height=200, width=700)
        self.frm_filtros.grid(column=0, ipadx=20, ipady=15, pady="40 0", row=0)
        
        # Label de Título donde se encuentran los Inputs de los filtros
        self.label_filtros = tk.Label(self.frm_filtros)
        self.label_filtros.configure(
            background="#AF9EB7",
            font="{Glacial Indifference} 20 {bold}",
            justify="center",
            relief="flat",
            text='Aplicar Filtros\npara Exportar la Información',
            width=56)
        self.label_filtros.grid(column=0, columnspan=2, pady=27, row=0)
        
        # Checkbox para el filtro de Año
        self.check_ano_Profesor = tk.BooleanVar()
        self.check_ano = tk.Checkbutton(self.frm_filtros)
        self.check_ano.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="left",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Filtrar por Año',
            variable=self.check_ano_Profesor,
            command=self.toggle_input_ano)
        self.check_ano.grid(column=0, padx=40, pady=20, row=2, sticky="w")
        
        # Checkbox para el filtro de Tipo de Documentos
        self.check_documento_Profesor = tk.BooleanVar()
        self.check_documento = tk.Checkbutton(self.frm_filtros)
        self.check_documento.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="left",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Filtrar por Tipo de Documento',
            variable=self.check_documento_Profesor,
            command=self.toggle_input_documento)
        self.check_documento.grid(column=0, padx=40, pady=0, row=3, sticky="w")
        
        # Checkbox para el filtro de Área de Conocimiento
        self.check_conocimiento_Profesor = tk.BooleanVar()
        self.check_conocimiento = tk.Checkbutton(self.frm_filtros)
        self.check_conocimiento.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="left",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Filtrar por Área de Conocimiento',
            variable=self.check_conocimiento_Profesor,
            command=self.toggle_input_conocimiento)
        self.check_conocimiento.grid(
            column=0, padx=40, pady=20, row=4, sticky="w")
        
        # Check para el filtro de Otro tipo de Filtro
        self.check_otro_Profesor = tk.BooleanVar()
        self.check_otro = tk.Checkbutton(self.frm_filtros)
        self.check_otro.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="center",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Filtrar por Otro',
            variable=self.check_otro_Profesor,
            command=self.toggle_input_otro)
        self.check_otro.grid(column=0, padx=40, pady=0, row=5, sticky="w")
        
        # Check para el filtro de Autor
        self.check_autor_Profesor = tk.BooleanVar()
        self.check_autor = tk.Checkbutton(self.frm_filtros)
        self.check_autor.configure(
            background="#AF9EB7",
            activebackground="#AF9EB7",
            cursor="circle",
            borderwidth=0,
            font="{Glacial Indifference} 16 {}",
            justify="left",
            offrelief="flat",
            offvalue=False,
            onvalue=True,
            overrelief="flat",
            selectcolor="#E9E0EB",
            takefocus=True,
            text='Filtrar por Autor',
            variable=self.check_autor_Profesor,
            command=self.toggle_input_autor)
        self.check_autor.grid(column=0, padx=40, row=1, sticky="w")
        
        # Inputfield del filtro de Autor
        self.input_autor = tk.Entry(self.frm_filtros)
        self.input_autor.configure(
            background="#E9E0EB",
            disabledbackground="#80738B",
            disabledforeground="#AF9EB7",
            font="{Glacial Indifference} 18 {}",
            foreground="#000",
            justify="center",
            relief="flat",
            state="disabled",
            takefocus=True,
            width=30)
        self.input_autor["state"] = "normal"
        self.input_autor.delete("0", "end")
        self.input_autor.insert("0", 'Nombre de Autor')
        self.input_autor["state"] = "disabled"
        self.input_autor.grid(column=1, ipadx=4, ipady=4, padx=40, row=1, sticky="e")
        
        # Inputfield del filtro de Año
        self.input_ano = tk.Entry(self.frm_filtros)
        self.input_ano.configure(
            background="#E9E0EB",
            disabledbackground="#80738B",
            disabledforeground="#AF9EB7",
            font="{Glacial Indifference} 18 {}",
            foreground="#000",
            justify="center",
            relief="flat",
            state="disabled",
            takefocus=True,
            width=30)
        self.input_ano["state"] = "normal"
        self.input_ano.delete("0", "end")
        self.input_ano.insert("0", 'Año')
        self.input_ano["state"] = "disabled"
        self.input_ano.grid(column=1, ipadx=4, ipady=4, padx=40, row=2, sticky="e")
        
        # Inputfield del filtro de Tipo de Documento
        self.input_documento = tk.Entry(self.frm_filtros)
        self.input_documento.configure(
            background="#E9E0EB",
            disabledbackground="#80738B",
            disabledforeground="#AF9EB7",
            font="{Glacial Indifference} 18 {}",
            foreground="#000",
            justify="center",
            relief="flat",
            state="disabled",
            takefocus=True,
            width=30)
        self.input_documento["state"] = "normal"
        self.input_documento.delete("0", "end")
        self.input_documento.insert("0", 'Tipo de Documento')
        self.input_documento["state"] = "disabled"
        self.input_documento.grid(column=1, ipadx=4, ipady=4, padx=40, row=3, sticky="e")
        
        # Inputfield del filtro de Área de Conocimiento
        self.input_conocimiento = tk.Entry(self.frm_filtros)
        self.input_conocimiento.configure(
            background="#E9E0EB",
            disabledbackground="#80738B",
            disabledforeground="#AF9EB7",
            font="{Glacial Indifference} 18 {}",
            foreground="#000",
            justify="center",
            relief="flat",
            state="disabled",
            takefocus=True,
            width=30)
        self.input_conocimiento["state"] = "normal"
        self.input_conocimiento.delete("0", "end")
        self.input_conocimiento.insert("0", 'Área de Conocimiento')
        self.input_conocimiento["state"] = "disabled"
        self.input_conocimiento.grid(column=1, ipadx=4, ipady=4, padx=40, row=4, sticky="e")
        
        # Inputfield del filtro de Otro
        self.input_otro = tk.Entry(self.frm_filtros)
        self.input_otro.configure(
            background="#E9E0EB",
            disabledbackground="#80738B",
            disabledforeground="#AF9EB7",
            font="{Glacial Indifference} 18 {}",
            foreground="#000",
            justify="center",
            relief="flat",
            state="disabled",
            takefocus=True,
            width=30)
        self.input_otro["state"] = "normal"
        self.input_otro.delete("0", "end")
        self.input_otro.insert("0", 'Otros')
        self.input_otro["state"] = "disabled"
        self.input_otro.grid(column=1, ipadx=4, ipady=4, padx=40, row=5, sticky="e")
        
        # Ventana Principal del Frame Principal
        self.mainwindow = self.frm_principal

    def run(self):
        self.mainwindow.mainloop()

    def false(self, event=None):
        pass
    
    def mostrar_frm_importar(self):
        self.btn_importar.configure(state="disabled", bg="#E9E0EB", foreground="#000", cursor="arrow")
        self.btn_exportar.configure(state="normal", bg="#82589F", foreground="#fff", cursor="circle")
        self.frm_importar.grid(column=0, columnspan=2, row=2, sticky="ew")
        self.frm_exportar.grid_remove()

    def mostrar_frm_exportar(self):
        self.btn_importar.configure(state="normal", bg="#82589F", foreground="#fff", cursor="circle")
        self.btn_exportar.configure(state="disabled", bg="#E9E0EB", foreground="#000", cursor="arrow")
        self.frm_importar.grid_remove()
        self.frm_exportar.grid(column=0, columnspan=2, ipadx=137, row=2)

    def agregar_efecto_hover(self, boton):
        boton.bind("<Enter>", lambda event, btn=boton: self.cambiar_color_hover(btn, "#574b90"))
        boton.bind("<Leave>", lambda event, btn=boton: self.cambiar_color_hover(btn, "#534B62"))

    def cambiar_color_hover(self, boton, color):
        boton.configure(bg=color)
        
    def check_todo_selected(self):
        if(self.check_todo_Profesor.get()):
            self.check_logros_Profesor.set(True)
            self.check_invest_Profesor.set(True)
            self.check_gest_academica.set(True)
            self.check_docencias_Profesor.set(True)
            self.check_benf_promep.set(True)
            self.check_cuerpo_academico.set(True)
            self.check_prog_academicos.set(True)
            self.check_tutorias_Profesor.set(True)
            self.check_dir_individualizada.set(True)
        else:
            self.check_logros_Profesor.set(False)
            self.check_invest_Profesor.set(False)
            self.check_gest_academica.set(False)
            self.check_docencias_Profesor.set(False)
            self.check_benf_promep.set(False)
            self.check_cuerpo_academico.set(False)
            self.check_prog_academicos.set(False)
            self.check_tutorias_Profesor.set(False)
            self.check_dir_individualizada.set(False)
    
    def select_folder(self):
        self.folderPath = filedialog.askdirectory()
        if self.folderPath:
            self.label_path.config(text=f"Carpeta: {self.folderPath}")
            self.label_path.grid(padx="0 500")
            self.documents =  os.listdir(self.folderPath)
            self.crear_etiquetas(self.documents)
            self.documentosArray = self.documents
            self.label_notificacion_importar.configure(text=f'Cargados documentos de {self.folderPath}')
            # print("\n", self.documents)
    
    def ejecutar_lecturaCV(self):
        lecturaCV(self.folderPath, self.documentosArray, self.selectedTables, self.queue)
        
    def actualizar_mensaje(self, txt):
        self.label_notificacion_importar.configure(text=txt)
        
    def actualizar_mensaje_en_bucle(self):
        while True:
            try:
                mensaje = self.queue.get_nowait()
                self.actualizar_mensaje(mensaje)
            except queue.Empty:
                pass
            time.sleep(1)
        
    def importar_informacion(self):
        self.selectedTables={
            "LogrosProfesor": self.check_logros_Profesor.get(),
            "InvestigacionesProfesor": self.check_invest_Profesor.get(),
            "GestionAcademica": self.check_gest_academica.get(),
            "Docencias": self.check_docencias_Profesor.get(),
            "BeneficiosPROMEP": self.check_benf_promep.get(),
            "CuerpoAcademico": self.check_cuerpo_academico.get(),
            "ProgramasAcademicos": self.check_prog_academicos.get(),
            "Tutorias": self.check_tutorias_Profesor.get(),
            "DireccionIndividualizada": self.check_dir_individualizada.get()
        }
        self.hilo = threading.Thread(target=self.ejecutar_lecturaCV)
        self.hilo.start()
        self.actualizar_mensaje_thread = threading.Thread(target=self.actualizar_mensaje_en_bucle)
        self.actualizar_mensaje_thread.daemon = True
        self.actualizar_mensaje_thread.start()
            
    def crear_etiquetas(self, documentos = []):
        self.counter = 0
        if(len(documentos) != 0):
            self.label_archivo.grid_remove()
            for document in documentos:
                self.separator = tk.Frame(self.scroll_archivos.innerframe)
                self.separator.configure(background="#000", height=2, width=300)
                self.separator.grid(column=0, row=self.counter)
                self.counter = self.counter + 1
                self.label_archivo = tk.Label(self.scroll_archivos.innerframe)
                self.label_archivo.configure(
                    background="#AF9EB7",
                    font="{Glacial Indifference} 16 {}",
                    justify="center",
                    relief="flat",
                    state="normal",
                    text=document,
                    width=30,
                    wraplength=400)
                self.label_archivo.grid(column=0, padx=20, pady=20, row=self.counter)
                self.counter = self.counter + 1
        else:
            self.label_archivo.grid()
            
    def toggle_input_autor(self):
        if(self.check_autor_Profesor.get()):
            self.input_autor.config(state="normal")
            if(self.input_autor.get() == "Nombre de Autor"):
                self.input_autor.delete("0", "end")
                self.input_autor.insert("0", "")
        else:
            self.input_autor.config(state="disabled")
            
    def toggle_input_otro(self):
        if(self.check_otro_Profesor.get()):
            self.input_otro.config(state="normal")
            if(self.input_otro.get() == "Otros"):
                self.input_otro.delete("0", "end")
                self.input_otro.insert("0", "")
        else:
            self.input_otro.config(state="disabled")
            
    def toggle_input_conocimiento(self):
        if(self.check_conocimiento_Profesor.get()):
            self.input_conocimiento.config(state="normal")
            if(self.input_conocimiento.get() == "Área de Conocimiento"):
                self.input_conocimiento.delete("0", "end")
                self.input_conocimiento.insert("0", "")
        else:
            self.input_conocimiento.config(state="disabled")
            
    def toggle_input_ano(self):
        if(self.check_ano_Profesor.get()):
            self.input_ano.config(state="normal")
            if(self.input_ano.get() == "Año"):
                self.input_ano.delete("0", "end")
                self.input_ano.insert("0", "")
        else:
            self.input_ano.config(state="disabled")
            
    def toggle_input_documento(self):
        if(self.check_documento_Profesor.get()):
            self.input_documento.config(state="normal")
            if(self.input_documento.get() == "Tipo de Documento"):
                self.input_documento.delete("0", "end")
                self.input_documento.insert("0", "")
        else:
            self.input_documento.config(state="disabled")
            
    def exportar_informe(self):
        self.filtersData = {
            "autor": {"state":self.check_autor_Profesor.get(), "data":self.input_autor.get()},
            "ano": {"state":self.check_ano_Profesor.get(), "data":self.input_ano.get()},
            "documento": {"state":self.check_documento_Profesor.get(), "data":self.input_documento.get()},
            "areaConocimiento": {"state":self.check_conocimiento_Profesor.get(), "data":self.input_conocimiento.get()},
            "otro": {"state":self.check_otro_Profesor.get(), "data":self.input_otro.get()}
        }
        print(self.filtersData)
        createTable(self.filtersData)
        
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Lectura de Curriculums")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app = InterfazCV(root)
    app.run()
