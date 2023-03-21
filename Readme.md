



### Clonar el repositorio
``` 
git clone url_repo
```

### Cambiar el directorio de trabajo actual a la ruta raíz del repositorio
``` 
cd path_local_repositorio
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
Abrir una terminal desde la raíz del proyecto y lanzar los siguientes comandos:

```	
flask --app flask-crud-app/storemanager.py shell
db.create_all()
exit()
```
