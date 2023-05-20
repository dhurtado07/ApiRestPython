# ApiRestPython
Este el proyecto final para el diplomado en FullStack para la materia Nociones de programacion
@Autor Denys Hurtado Mamani

## El proyecto tambien esta deployado en Render.com
https://apirest-denys.onrender.com/

## Prerrequisitos:
* Python debe estar instalado.
* PostgreSQL debe estar instalado.

## Pasos para configurar y ejecutar el proyecto:

## 1. Clonar el repositorio.
```
git clone url_repositorio
```
## 2. Instalación de dependencias:
```
pip install flask
pip install flask-cors
pip install psycopg2
```
## 3. Crear la base de datos en PostgreSQL:
```
CREATE DATABASE api_users;
```
## 4. Crear la tabla 'usuarios' en la base de datos:
```
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    cedula_identidad VARCHAR(10) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE NOT NULL
);
```
## 5. Configurar las credenciales de PostgreSQL en el archivo app.py:
```
conn = psycopg2.connect(
    host="servidor",
    database="nombre_base_de_datos",
    user="usuario",
    password="contraseña"
)
```
## 6. Ejecutar el proyecto:
```
python app.py
```
Esto despliega la dirección http://127.0.0.1:5000. Acceda a ella usando su navegador.
Recuerda reemplazar los valores de "servidor", "nombre_base_de_datos", "usuario" y "contraseña" en el paso 5 con la información correcta de su entorno

