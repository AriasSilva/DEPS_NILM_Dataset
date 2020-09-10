# DEPS: NILM Dataset
Este repositorio es parte del Trabajo Final de Máster: "Desagregación de la demanda usando Non-Intrusive Load Monitoring Toolkit (NILMTK)” conducente al grado de Máster en Sistemas Inteligentes de Energía y Transporte de [Andrés Arias Silva](https://www.linkedin.com/in/ariassilva/). El proyecto cuenta con la colaboración de los docentes Dr. Enrique Personal y D. Antonio Parejo de la Universidad de Sevilla.

El objetivo de este trabajo es mostrar el uso y potenciales aplicaciones de la herramienta de desagregación de la demanda Non-Intrusive Load Monitoring Toolkit ([NILMTK](http://nilmtk.github.io/)) a través de la implementación de un caso real que involucra la creación de un dataset de uso público con datos de energía del Aula 2.2 Bis de la Escuela Politécnica Superior de la Universidad de Sevilla.

El dataset denominado **DEPS (Dataset de la Escuela Politécnica Superior)** se encuentra en formato HDF5 y puede ser descargado en el [siguiente enlace](https://uses0-my.sharepoint.com/:u:/g/personal/andarisil_alum_us_es/EdPESThCSWVBndyDSF3mZK0BuD5ggBxm8_pmoegA4MUgUg?e=G85wsj) usando la contraseña `deps2020`. Adicionalmente, se proporciona un convertidor para ser utilizado en NILMTK en caso de ser requerido el cual se encuentra en este repositorio.

## NILM

La desagregación de la demanda, también conocida como Non-Intrusive Load Monitoring (NILM), se define como una técnica computacional para estimar el consumo individual de energía eléctrica de diversos dispositivos utilizando la lectura agregada de un solo medidor [[1]](https://ieeexplore.ieee.org/document/192069?section=abstract)[[2]](https://spiral.imperial.ac.uk/handle/10044/1/49452).  Este concepto ha tomado relevancia entre los investigadores en la última década tal como lo indica este [análisis](/notebooks/Publicaciones/Publicaciones.ipynb) de publicaciones NILM:

Dentro de sus beneficios se destacan los siguientes:

- Información detallada de la factura eléctrica
- Aplicaciones de respuesta a la demanda o *demand response* (DR) 
- Identificación de averías y consumo ilegal de energía

En la siguiente figura se muestra un ejemplo de desagregación de la demanda usando el dataset [REDD](redd.csail.mit.edu):

![nilm](/imagenes/nilm.svg)

## NILMTK

NILMTK es un kit de herramientas de código abierto diseñado específicamente para permitir un acceso fácil y brindar un análisis comparativo de algoritmos de desagregación de demanda en diversos datasets. NILMTK proporciona un *pipeline* completo, intérpretes de diversos datasets y métricas de precisión, lo que reduce la barrera de entrada para investigadores y desarrolladores. La siguiente figura muestra el *pipeline* de NILMTK:

![pipeline](/imagenes/pipeline.svg)

Se recomienda instalar NILMTK bajo un *enviroment* de paquetes de Python, específicamente [Anaconda](https://www.anaconda.com/distribution/). Una guía de instalación de NILMTK en Windows se encuentra en el [siguiente enlace](https://github.com/nilmtk/nilmtk/blob/master/docs/manual/user_guide/install_user.md). 

Adicionalmente, toda la información sobre NILMTK se encuentra en [nilmtk.github.io](http://nilmtk.github.io/).

## Nuevo Dataset DEPS

Dentro de las instalaciones de la Escuela Politécnica Superior de la Universidad de Sevilla se encuentra el Aula 2.2 Bis, la cual está equipada con un cuadro eléctrico con diversos medidores. Estos medidores registran el consumo agregado y consumos individuales de determinados dispositivos del aula. Gracias a esto, se han registrado datos de consumo y se han almacenado junto con sus metadatos en un dataset que considera las siguientes fechas:

- Desde el lunes 24/02/2020 a las 00:00:00 hrs. al jueves 27/02/2020 a las 23:59:59 hrs.
- Desde el lunes 02/03/2020 a las 00:00:00 hrs. al viernes 06/03/2020 a las 23:59:59 hrs.

### Adquisición de datos

DEPS contiene datos agregados y metadatos de un sistema trifásico (R, S ,T) de seis dispositivos de consumo, conectados a diferentes fases. La siguiente tabla resume las medidas registradas en el dataset.

| Medidor                              | Medidas Registradas | Periodo de Muestreo |
| ------------------------------------ | ------------------- | ------------------- |
| 1x Medidor principal trifásico (RST) | P, Q                | 1 segundo           |
| 3 x Medidores por fase (R, S y T)    | P, Q, V, I          | 1 segundo           |
| 6 x Medidores de Dispositivos        | P, Q, V, I          | 1 segundo           |

El medidor principal (Main_RST) mide la potencia P y Q agregada, también opera como medidor por fase (Main_R, Main_S y Main_T) permitiendo registrar P, Q, V e I para cada una de ellas. En cuanto a los dispositivos, se cuenta con mediciones de P de dos grupos de iluminación (Lights_1 y Lights_2), mediciones de P, Q, V e I para tres equipos de aire acondicionado (HVAC_1, HVAC_2 y HVAC_4) y un rack de equipos informáticos (Rack). 

En la siguiente figura se muestra un esquema unilineal eléctrico de los medidores.

![circuito](/imagenes/circuito.svg)

### Convertidor NILMTK

Para la creación de un dataset compatible con NILMTK es necesario contar con un convertidor que estructure los datos y sus metadatos en el formato HDF5. En el presente trabajo se utiliza como referencia el convertidor REDD previamente desarrollado, incorporándole modificaciones para que los datos extraídos desde el Aula 2.2 Bis sean compatibles.

- El convertidor y los metadatos se pueden [descargar desde este enlace](https://downgit.github.io/#/home?url=https://github.com/AndresAriasSilva/DEPS_NILM_Dataset/tree/master/nilmtk_converter/deps).
- Para su mejor comprensión, se ha elaborado una [guía de implementación y uso del convertidor](/nilmtk_converter)

### Análisis y modelos de desagregación 

Con la ayuda de las diversas funciones de NILMTK se analizan datos y metadatos del dataset DEPS. En los siguientes notebooks se presentan diversos análisis que permiten posteriormente generar y comparar diversos modelos de desagregación usando varios periodos y métodos de muestreo basados en los algoritmos CO (*Combinatorial Optimisation*) y FHMM (*Factorial Hidden Markov Models*):

- [Análisis - NILMTK-DF](/notebooks)
- [Análisis - Diagnóstico y Estadísticas](/notebooks)
- [Preprocesamiento](/notebooks)
- [Entrenamiento](/notebooks)
- [Validación](/notebooks)
- [Desagregación](/notebooks)

Los resultados de los análisis de los diferentes modelos muestran, bajo diferentes métricas, que el rendimiento del modelo FHMM entrenado con datos potencia activa promedio con un periodo de 10 minutos posee un buen desempeño para su implementación. En la siguiente imagen se muestra un extracto de los análisis a las métricas obtenidas de los diferentes modelos implementados.



![F1](/imagenes/F1.svg)

### Reporte de desagregación

Utilizando el modelo con el mejor desempeño en el dataset DEPS, **se ha implementado un código para generar un reporte interactivo básico en HTML** de los resultados de la desagregación. 

A continuación se muestra una captura de pantalla del reporte, el cual puede ser consultado en el [siguiente enlace](https://andresariassilva.github.io/DEPS_NILM_Dataset/reporte/report.html) y cuyo código escrito en Python se encuentra [acá](/reporte/create_report.py).

[![reporte](/imagenes/reporte.png)](https://andresariassilva.github.io/DEPS_NILM_Dataset/reporte/report.html)
