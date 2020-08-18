# DEPS: NILM Dataset
[TOC]

Este repositorio es parte del Trabajo Final de Máster: "Desagregación de la demanda usando Non-Intrusive Load Monitoring Toolkit (NILMTK)”  del alumno [Andrés Arias Silva](https://www.linkedin.com/in/ariassilva/).

El objetivo de este trabajo es mostrar el uso y potenciales aplicaciones de la herramienta de desagregación de la demanda Non-Intrusive Load Monitoring Toolkit ([NILMTK](http://nilmtk.github.io/)) a través de la implementación de un caso real que involucra la creación de un dataset de uso público con datos de energía del Aula 2.2 Bis de la Escuela Politécnica Superior de la Universidad de Sevilla.

El dataset denominado DEPS (Dataset de la Escuela Politécnica Superior) se encuentra en formato HDF5 y puede ser descargado en el siguiente enlace. Adicionalmente, se proporciona un convertidor para ser utilizado en NILMTK en caso de ser requerido.



## NILM

La desagregación de la demanda, también conocida como Non-Intrusive Load Monitoring  (NILM), se define como una técnica computacional para estimar el consumo individual de energía eléctrica de diversos dispositivos utilizando la lectura agregada de un solo medidor [[1]](https://ieeexplore.ieee.org/document/192069?section=abstract)[[2]](https://spiral.imperial.ac.uk/handle/10044/1/49452).

Dentro de sus beneficios se destacan los siguientes:

- Información detallada de la factura eléctrica
- Aplicaciones de respuesta a la demanda o *demand response* (DR): 
- Identificación de averías y consumo ilegal de energía

![nilm](C:\Users\arias\Documents\GitHub\DEPS_NILM_Dataset\imagenes\nilm.svg)

> Ejemplo de desagregación de la demanda usando el dataset REDD: [redd.csail.mit.edu.]()

## NILMTK

NILMTK es un kit de herramientas de código abierto diseñado específicamente para permitir un acceso fácil y brindar un análisis comparativo de algoritmos de desagregación de demanda en diversos datasets. NILMTK proporciona un pipeline completo, intérpretes de diversos datasets y métricas de precisión, lo que reduce la barrera de entrada para que los investigadores implementen un nuevo algoritmo y comparen su rendimiento. 

Los desarrolladores de la herramienta recomiendan instalar NILMTK bajo un entorno virtual o *enviroment* de paquetes de Python, específicamente [Anaconda]([www.anaconda.com/distribution](https://www.anaconda.com/distribution/).). Una guía de instalación de NILMTK en Windows se encuentra en el [siguiente enlace](). 

Adicionalmente, toda la información sobre NILMTK se encuentra en http://nilmtk.github.io/

## DEPS

Dentro de las instalaciones de la Escuela Politécnica Superior (EPS) de la Universidad de Sevilla (US) se encuentra el Aula 2.2 Bis, la cual está equipada con un cuadro eléctrico con diversos medidores. Estos medidores registran diversas variables eléctricas incluido el consumo agregado del aula y consumos individuales de determinados dispositivos. 

### Adquisición de datos

DEPS contiene datos agregados y metadatos de un sistema trifásico (R,S ,T) de seis dispositivos de consumo, conectados a diferentes fases. La siguiente tabla resume las medidas registradas en el dataset.

| Medidor                           | Medidas Registradas | Periodo de Muestreo |
| --------------------------------- | ------------------- | ------------------- |
| 1x Medidor trifásico principal 3F | P, Q                | 1 segundo           |
| 3 x Medidores por fase (R, S, T)  | P, Q, V, I          | 1 segundo           |
| 6 x Medidores de Dispositivos     | P, Q, V, I          | 1 segundo           |

El medidor principal (Main_RST) mide P y Q agrgegadas y también opera como medidor por fase (Main_R, Main_S y Main_T) permitiendo registrar P,  Q, V e I  para cada una de ellas. En cuanto a los dispositivos, se cuenta con mediciones de P de dos grupos de iluminación (Lights_1 y Lights_2), mediciones de P, Q, V e I para tres equipos de aire acondicionado (HVAC_1, HVAC_2 y HVAC_4) y un rack de equipos informáticos (Rack). 

En la siguiente figura se muestra un esquema unilineal eléctrico de los medidores.

![circuito](C:\Users\arias\Documents\GitHub\DEPS_NILM_Dataset\imagenes\circuito.svg)

> Figura de elaboración propia

### Convertidor NILMTK



### Análisis del dataset DEPS



### Reporte

