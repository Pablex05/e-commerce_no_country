# C2-G11
E-commerce Project

# pasos para ejecutar el proyecto
## 1-Instalar Python
### En Linux
    sudo apt-get install python3
### En Windows
    descargar e instalar el paquete de instalacion desde la pagina https://www.python.org/downloads/
## 2-Instalar Pip
### En Linux
    sudo apt install python3-pip
### En Windows 
    1.descargar el archivo desde este link https://bootstrap.pypa.io/get-pip.py
    2.ejecutar con el siguiente comando "python get-pip.py"
## 3-Instalar virtual venv
### En Linux
    sudo apt install python3.8-venv
### En Windows
    pip install virtaulenv
## 4-Crear el entorno virtual
### En Linux
    python3 -m venv [ruta de la carpeta]
### En Windows
    python -m venv [ruta de la carpeta]
## 5-entrar y Activar el entorno virtual
### En Linux
    source bin/activate
### En Windows 
    source .venv/bin/activate
## 6-Instalar desde Requirements
    pip3 install -r requirements.txt
## 7-Instalar Pillow
    python -m pip install Pillow
## 8-Ejecutar servidor
## En Linux
    python3 manage.py runserver
## En Windows
    python manage.py runserver
