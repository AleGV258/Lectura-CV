# Lectura Currículos para ETL 📂

_La aplicación de lectura de currículos busca facilitar la centralización de la información de documentos proporcionados por entidades externas a la facultad de informática de la UAQ, en este caso información profesional sobre profesores de la facultad de informática_

## Comenzando 🚀

_Para obtener el proyecto en local y que se permita la edición, mejora e innovación, se debe clonar en la máquina local para poder acceder a estos archivos, este proyecto fue realizado con el apoyo de ```Centro de Desarrollo```_

Mira **Despliegue** para conocer como desplegar el proyecto.

### Pre-requisitos ✏️

_Antes de inicializar el proyecto y ejecutarlo, debes tener en cuenta los siguientes puntos_

- La aplicación almacena y lleva a cabo el proceso de ETL en cualquier archivo CV, en cualquier base de datos de ```MongoDB```, pero se recomienda crear su propia base de datos desde 0 de ```MongoDB```, para almacenar correctamente la información

- Para esto se recomienda crear tu propio cluster desde ```MongoDB Atlas``` y almacenar la URI para su posterior conectividad

- La aplicación hace uso de un archivo ```.env``` en el cual se debe colocar la URI de la base de datos con el nombre ```MONGO_URI``` para que funcione la conectividad

- Debido a que en ciertas redes se bloquea el acceso a ```MongoDB``` se recomienda hacer uso de una VPN que permita la conectividad

## Construido con 🛠️

_Herramientas, lenguajes de programación y demás recursos usados para su construcción_

* [Python](https://www.python.org/downloads/) – (3.10 o superior) Lenguaje de programación usado para su construcción 
* [Pygubu-Designer](https://github.com/alejandroautalan/pygubu-designer) – Aplicación de desarrollo rápida que permite construir las interfaces de usuario de la aplicación.
* [MongoDB Atlas](https://www.mongodb.com/atlas) – Plataforma para la creación y administración de la base de datos
* [MongoDB Compass](https://www.mongodb.com/products/tools/compass) – Aplicación para la visualización y administración de los datos e información de la base de datos

## Despliegue 📦

_Se demuestra cómo se debe desplegar el proyecto para su correcto funcionamiento_

1. Descarga o clona el proyecto localmente

2. Una vez instalado ```Python``` se debe navegar entre los directorios para llegar al directorio raiz del proyecto desde consola

3. Antes de inicializar el proyecto se deben instalar las siguientes librerias de ```Python```
```python
pip install tk
pip install reportlab
pip install python-dotenv
pip install pymongo
pip install pywin32
pip install pygubu
pip install pygubu-designer
pip install reportlab
```

4. Para incializar el proyecto se debe ejecutar el comando 
```python
py Interface.py
```

5. Una vez el programa se encuentre corriendo se podrá interactuar y llevar a cabo su funcionalidad

### Notas Adicionales 📋

_Se colocan notas que son de utilidad para la manipulación del proyecto y/o sistema_

- Si se desea modificar más fácilmente la interfaz de usuario, se recomienda abrir ```Pygubu-Designer``` y abrir el archivo denominado ```Modelo-LecturaCV.ui```

## Recursos Adicionales 💥

_Documentos, enlaces y más información referente a la construcción del proyecto, sistema o aplicación_

* [Figma](https://www.figma.com/file/I1Cb2SfUBRSHAuwZtn7n7C/Lectura-de-CV?type=design&node-id=0%3A1&mode=design&t=3XbOK3KuaujEw89O-1) – Modelos y prototipos creados para la aplicación
* [LucidChart](https://lucid.app/lucidchart/d2f34fda-5d00-4a72-9c1e-68c1151e10dc/edit?invitationId=inv_f7ee5e3d-2ca5-4807-bbd2-87ce0cf75a3f) – Modelo de la base de datos

## Autores ✒️

_Las personas implicadas en el desarrollo del proyecto_

* **Michell García** - [AleGV258](https://github.com/AleGV258)
* **Daniel León** - [DanielLeonP](https://github.com/DanielLeonP)
* **Uriel Baeza** - [OlafGG](https://github.com/OlafGG)
* **Israel Nieto** - [Israelnu](https://github.com/Israelnu)
* **Daniel Aros** - [DanielAros](https://github.com/DanielAros)
