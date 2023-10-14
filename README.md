# API Airbnb

## Recomendaciones --- [Opcional]
Instalar la extension [Material Icon Theme](https://marketplace.visualstudio.com/items?itemName=PKief.material-icon-theme
) del Visual Studio Code.

## Instalación

Ejecutar en un cmd en el directorio donde queremos que se cree la carpeta:

```sh
git clone https://github.com/Jose-Tapia-Catena/api-airbnb.git
cd airbnb
code .
```

Abrimos un terminal dentro de Visual Studio Code y ejecutamos el siguiente comando:

```sh
pip install -r requirements.txt
```
## Ejecución  

Dentro del terminal de VSC:

```sh
python.exe -m uvicorn app:app --reload --port 8001
```

Para ver todos los métodos de la api (insert, delete, find) en el buscador ir a:

```sh
http://127.0.0.1:8001/docs
```


MongoDB Compass 

```sh
mongodb+srv://administrator:<password>@cluster0.gxxlaa4.mongodb.net/test
```
