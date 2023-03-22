
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
Si todo va bien debería correr en localhost:5001


### Lanzar load_data.py para cargar los datos generados con la API

La aplicación debe estar corriendo (ver paso previo).

Abrir una terminal adicional, activar el entorno virtual y lanzar el script de carga con el siguiente comando:

```
source .venv/bin/activate
python load_data.py
```


### Curls de ejemplo 

Agregar un producto:
```
curl --request POST --url http://127.0.0.1:5001/product --header 'Content-Type: application/json' \
 --data '{ "brand":"plátano de canarias", "type_product":"fruit", "calories":"60.0",	
            "satured_fat_percentage":3.0, "sugar_percentage": 5.0}'
```


Modificar un producto:

```
curl --request PUT --url http://127.0.0.1:5001/product/1 --header 'Content-Type: application/json' \
  --data '{  "brand":"Plátano canario", "type_product":"fruit", "calories":"120.0",
             "satured_fat_percentage":2.0, "sugar_percentage": 5.0 }'
```

Agregar un establecimiento:
```
curl --request POST --url http://127.0.0.1:5001/store --header 'Content-Type: application/json' \
 --data '{ "name":"Mercadona",	"address":"plaza españa, 5, Madrid", "opening_hours":"10:00-18:00"}'
```

Asignar un precio a un producto dado en cierto establecimiento:
```
curl --request PUT --url http://127.0.0.1:5001/product/1/price --header 'Content-Type: application/json' \
  --data '{ "price":"5.5", "store_id":1}'
```

Devolver todos los productos de un cierto establecimiento
```
curl --request GET --url http://127.0.0.1:5001/store/4/products
```