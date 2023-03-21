
## Instalación

Abrir una terminal y seguir los siguientes pasos:

### Clonar el repositorio
``` 
git clone https://github.com/joseallones/storemanager-flasksqlalchemy.git
```

### Cambiar el directorio de trabajo actual a la ruta raíz del repositorio:
``` 
cd storemanager-flasksqlalchemy
``` 

### Crear entorno virtual

```	
python -m venv .venv	
```

### Activar entorno virtual
```	
source .venv/bin/activate
```

### Instalar dependencias
```	
pip install -r requirements.txt
```

### Lanzar generate_data.py para generar datos iniciales
```	
python generate_data.py
```
Los ficheros .csvs se almacenan en la carpeta csvs


### Crear el esquema de la base de datos

```	
flask --app flask-crud-app/storemanager.py shell
db.create_all()
exit()
```


### Arrancar la aplicación

```	
python flask-crud-app/storemanager.py 
```



### Lanzar load_data.py para cargar los datos generados con la API

La aplicación debe estar corriendo (ver paso previo).

Abrir una terminal adicional, activar el entorno virtual y lanzar el script de carga con el siguiente comando:

```
source .venv/bin/activate
python load_data.py
```	