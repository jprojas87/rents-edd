===========================================================
            PROYECTO CRUD-EDD (Python + FastAPI)
===========================================================

Este proyecto es una versión simplificada de un CRUD que 
utiliza Estructuras de Datos implementadas manualmente 
(Listas enlazadas, Colas, Pilas, Hash Tables, etc.) en vez 
de una base de datos.

El almacenamiento es completamente en memoria usando estas 
estructuras de datos personalizadas.

Este documento explica cómo instalar, configurar y ejecutar 
el proyecto desde cero en cualquier sistema operativo.

-----------------------------------------------------------
1. REQUISITOS
-----------------------------------------------------------

Necesitas tener instalado:

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Extensión de Python para tu IDE (si usas VS Code)
- git (para clonar el repositorio)

IMPORTANTE:
Si usas Windows, es altamente recomendado ejecutar este 
proyecto usando WSL2 (Ubuntu), ya que es mucho más compatible 
con entornos de desarrollo modernos.


-----------------------------------------------------------
2. DESCARGAR EL PROYECTO
-----------------------------------------------------------

Clona el repositorio desde GitHub:

    git clone https://github.com/usuario/crud-edd.git

Entra a la carpeta del proyecto:

    cd crud-edd


-----------------------------------------------------------
3. CONFIGURACIÓN DEL ENTORNO (SEGÚN TU SISTEMA)
-----------------------------------------------------------

===========================================================
A) WINDOWS (USANDO WSL2 + UBUNTU)
===========================================================

1. Abrir Ubuntu (WSL2).
2. Navegar a la carpeta del proyecto (montada desde Windows):

       cd /mnt/c/Users/TU_USUARIO/path/al/proyecto/crud-edd

3. Instalar pip (si no está instalado):

       sudo apt install python3-pip -y

4. Instalar venv para Python:

       sudo apt install python3-venv -y
       o si usas Python 3.12:
       sudo apt install python3.12-venv -y

5. Crear un entorno virtual dentro del proyecto:

       python3 -m venv .venv

6. Activar el entorno virtual:

       source .venv/bin/activate

   Deberías ver: (.venv) al inicio de la línea.

7. Instalar dependencias del proyecto:

       pip install fastapi uvicorn


===========================================================
B) LINUX NATIVO (UBUNTU / DEBIAN)
===========================================================

1. Abrir una terminal.
2. Navegar a la carpeta del proyecto:

       cd crud-edd

3. Instalar pip y venv:

       sudo apt install python3-pip python3-venv -y

4. Crear entorno virtual:

       python3 -m venv .venv

5. Activar entorno virtual:

       source .venv/bin/activate

6. Instalar dependencias:

       pip install fastapi uvicorn


===========================================================
C) MACOS (INTEL O M1/M2/M3)
===========================================================

1. Abrir una terminal.
2. Navegar al proyecto:

       cd crud-edd

3. Instalar pip y venv (si no están disponibles):

       brew install python3

4. Crear entorno virtual:

       python3 -m venv .venv

5. Activar entorno virtual:

       source .venv/bin/activate

6. Instalar dependencias:

       pip install fastapi uvicorn


-----------------------------------------------------------
4. ESTRUCTURA DEL PROYECTO
-----------------------------------------------------------

El proyecto debe tener esta estructura:

    crud-edd/
        datastructures/     <-- tú copias tus estructuras manuales aquí
        domain/
        repository/
        services/
        api/
        .venv/
        README.txt

Dentro de datastructures NO se genera código automáticamente:
tú debes copiar tus implementaciones manuales de:

- Lista enlazada
- Cola
- Pila
- Hash Table
- Etc.


-----------------------------------------------------------
5. EJECUTAR EL SERVIDOR
-----------------------------------------------------------

Asegúrate de tener el entorno virtual activado:

    source .venv/bin/activate

Luego ejecuta:

    uvicorn api.main:app --reload

Si todo está bien deberías ver:

    Uvicorn running on http://127.0.0.1:8000

Abre tu navegador y entra a:

    http://127.0.0.1:8000/docs

Ahí encontrarás:

- CRUD de propiedades
- CRUD de reseñas
- CRUD de comentarios
- CRUD de favoritos

La API es totalmente funcional sin base de datos porque usa
las estructuras de datos manuales como almacenamiento.


-----------------------------------------------------------
6. DESACTIVAR EL ENTORNO VIRTUAL
-----------------------------------------------------------

Cuando termines de trabajar:

    deactivate


-----------------------------------------------------------
7. ERRORES COMUNES Y SOLUCIONES
-----------------------------------------------------------

1) ERROR: "Command 'pip3' not found"
   SOLUCIÓN:
       sudo apt install python3-pip -y

2) ERROR: "No module named venv"
   SOLUCIÓN:
       sudo apt install python3-venv -y
       o:
       sudo apt install python3.12-venv -y

3) ERROR: "uvicorn: command not found"
   SOLUCIÓN:
       pip install uvicorn
       (asegúrate de que el venv esté activo)

4) ERROR: al correr uvicorn no reconoce los imports
   SOLUCIÓN:
       Debes ejecutar el comando desde la carpeta raíz del proyecto.


-----------------------------------------------------------
8. LISTO :)
-----------------------------------------------------------

Después de seguir los pasos de este archivo, el proyecto está 
completamente configurado y puedes empezar a trabajar o 
modificar el código con total seguridad.
