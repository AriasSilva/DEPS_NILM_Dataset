# 1. Implementación y uso del convertidor DEPS

## Implementación en NILMTK

Para su implementación en Anaconda (entorno nilmtk-env) es necesario habilitar una carpeta dentro del entorno, que contenga el convertidor y los archivos de metadatos.

El convertidor y los metadatos se pueden [descargar desde este enlace](https://downgit.github.io/#/home?url=https://github.com/AndresAriasSilva/DEPS_NILM_Dataset/tree/master/nilmtk_converter/deps).

La carpeta del convertidor DEPS debe ser alojada localmente en : ***nilmtk/dataset_converters/***

Luego, se debe indicar que se ha añadido el convertidor modificando el archivo ***__init__.py*** de la carpeta de los convertidores agregando la siguiente línea al archivo: `from .deps.convert_deps import convert_deps `

Finalmente reiniciar el kernel de python

![convertidor](/imagenes/convertidor.svg)

## Uso

Importación del convertidor:


```python
from nilmtk.dataset_converters import convert_deps
```

La función del convertidor es:

`convert_deps('C:/data/', 'C:/data/raw_data.csv', 'C:/data/DEPS.h5')`

En la función `convert_deps` se deben especificar los siguientes parámetros:

- `C:/data/`: ruta principal del dataset, acá se almacenan los archivos correspondientes al formato REDD por lo que se creará una carpeta llamada classroom_1 que contiene todos los archivos de los canales además del archivo de etiquetas labels.dat.

- `C:/data/raw_data.csv`: ruta completa del archivo de datos crudos en formato CSV

- `C:/data/DEPS.h5`: ruta completa del archivo de salida en formato HDF5.

### Conversión del dataset DEPS


```python
import time
start = time.time()
#convertidor
convert_deps('C:/Users/arias/Desktop/data',
             'C:/Users/arias/Desktop/data/raw_data.csv',
             'C:/Users/arias/Desktop/data/DEPS.h5', format='HDF')

#tiempo
print(str(round(time.time()-start,2))+'segundos')
```

    Converting C:/Users/arias/Desktop/data/raw_data.csv to REDD format...
    Directory  C:/Users/arias/Desktop/data/classroom_1 Already exists
               export data from Main_RST to channel_1.dat
               export data from Main_R to channel_2.dat
               export data from Main_S to channel_3.dat
               export data from Main_T to channel_4.dat
               export data from Lights_1 to channel_5.dat
               export data from Lights_2 to channel_6.dat
               export data from HVAC_1 to channel_7.dat
               export data from HVAC_2 to channel_8.dat
               export data from HVAC_4 to channel_9.dat
               export data from Rack to channel_10.dat
               export labels.dat
    Done converting raw data to REDD format!
     
    Loading data from 'Aula 2.2 Bis' to classroom N° 1 ... Loading channels 1 2 3 4 5 6 7 8 9 10 
    Loaded metadata
    Done converting YAML metadata to HDF5!
    Done converting DEPS data to HDF5!
    70.11segundos
    
