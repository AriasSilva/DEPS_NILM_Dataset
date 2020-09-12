#!/usr/bin/env python
# coding: utf-8
# python create_report.py

import pandas as pd
import datetime
import codecs
from plotly.io import to_html
import plotly.graph_objects as go
import plotly.express as px 
from plotly.subplots import make_subplots
from nilmtk import DataSet

def create_report(data_dir, html_dir):
    #report in spanish
    labels = ['Lights_1', 'Lights_2', 'HVAC_1', 'HVAC_2', 'HVAC_4', 'Rack']

    results = DataSet(data_dir)
    results_elec = results.buildings[1].elec

    #pie
    df1=pd.DataFrame(results_elec.submeters().fraction_per_meter(), columns=['Fraction'])
    df1['Energy']=round(df1['Fraction']*results_elec.total_energy()[0],1)
    df1['Device']=labels 
    fig1 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig1.add_trace(go.Pie(values=df1['Fraction'], name='Porcentaje', hoverinfo="label+percent+name",
                          textinfo='label+percent', labels=labels, sort=False), 1, 1)
    fig1.add_trace(go.Pie(values=df1['Energy'], name='Energía', hoverinfo="label+value+name", textinfo='label+value',
                          labels=labels, sort=False, texttemplate="%{value:.1f} kWh"), 1, 2)
    fig1.update_traces(hole=.3)
    fig1.update_layout(width=900, height=450,
         annotations=[dict(text='%', x=0.21, y=0.5, font_size=22, showarrow=False),
                      dict(text='kWh', x=0.81, y=0.5, font_size=22, showarrow=False)])
    pie=fig1.to_html()

    #lines
    df2=results_elec.select(instance=[5,6,7,8,9,10]).dataframe_of_meters(ac_type='active')
    df2.columns=labels[:6]
    fig2=px.line(df2, width=900, height=500,labels={'variable':'Dispositivo', 'index':'Fecha', 'value':'Potencia (W)'})
    lines=fig2.to_html()

    #metadata
    date=results.metadata['date']
    date=datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M:%S')
    sample_period=results.metadata['meter_devices']['mains']['sample_period']
    sample_period=str(round(sample_period/60.0))+' minutos'
    start=results.metadata['timeframe']['start']
    start=datetime.datetime.strptime(start,'%Y-%m-%dT%H:%M:%S+01:00').strftime('%d/%m/%Y %H:%M:%S')
    end=results.metadata['timeframe']['end']
    end=datetime.datetime.strptime(end,'%Y-%m-%dT%H:%M:%S+01:00').strftime('%d/%m/%Y %H:%M:%S')

    #HTML report
        msg ="""
    <html>
      <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 50; background:white; }</style>
      </head>
      <body>
        <h1><b>Reporte de Desagregación de la Demanda</b></h1>
        <table class="table table-striped" style="width: 900px; height: 70px;" border="2">
          <tbody>
            <tr>
              <td style="vertical-align: top; background-color: #f7fbee;">Recinto</td>
              <td style="vertical-align: top; background-color: #f7fbee;">Aula 2.2
                Bis - EPS - Universidad de Sevilla</td>
            </tr>
            <tr>
              <td style="vertical-align: top; background-color: #f7fbee;">Fecha
                Reporte</td>
              <td style="vertical-align: top; background-color: #f7fbee;">04/08/2020
                10:13:56<br>
              </td>
            </tr>
          </tbody>
        </table>
        <h2><b> Energía Consumida</b></h2>
        <table class="table table-striped" style="width: 900px; height: 83px;" border="2">
          <tbody>
            <tr>
              <td style="vertical-align: top; background-color: #f7fbee;">Fecha
                Inicio</td>
              <td style="vertical-align: top; background-color: #f7fbee;">03/03/2020
                00:00:00</td>
            </tr>
            <tr>
              <td style="vertical-align: top; background-color: #f7fbee;">Fecha Fin</td>
              <td style="vertical-align: top; background-color: #f7fbee;">05/03/2020
                00:00:00</td>
            </tr>
            <tr>
              <td style="vertical-align: top; background-color: #f7fbee;">Periodo de
                desagregación</td>
              <td style="vertical-align: top; background-color: #f7fbee;">10 minutos<br>
              </td>
            </tr>
          </tbody>
        </table>
        <p></p>
        <h4><b>Gráfico de energía desagregada</b></h4>
        """+pie+"""
        <h4><b>Gráfico de potencia instantánea desagregada</b> </h4>
        """+lines+"""
        <p><br>
        </p>
        <p>Este reporte es parte del proyecto <a href="https://ariassilva.github.io/DEPS_NILM_Dataset/"><span

              style="color: #337ab7;">DEPS-Dataset</span><br>
          </a></p>
        2020<span style="color: #337ab7;"><br>
        </span><br>
        <br>
      </body>
    </html>"""

    with codecs.open(html_dir, 'w', encoding='utf8') as f:
        f.write(msg)
        f.close()
    return print('done!')
        
create_report(data_dir='C:/data/predictions.h5', html_dir='C:/data/report.html')






