#import semua modules
import numpy as np
import dash
from dash import dcc, html, Output, Input, State
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# from main import *

#inisiasi aplikasi
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


#membaca file
air_masuk1 = "Chart Air Masuk "

air_keluar1 = "Chart Air Keluar "

url_masuk = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVE6RWRi3EG9vL2iBq7Vw2RK3SW2-iIwAaFus3nU2HLbbzhZ3Jb3xVdv6Kd-nJ-hu4gu8ftRZ4mJvF/pub?output=csv&sheet={air_masuk1}"
url_keluar = url="https://docs.google.com/spreadsheets/d/e/2PACX-1vQQVBtC-xGgAwkkTOMCEEJp78FbJTlBxWD39LXtRdRs9S5Pl4yjFjT7XZpGie1BgUpSrTVGgda74ste/pub?output=csv&sheet={air_keluar1}"


df_masuk = pd.read_csv(url_masuk)
df_keluar = pd.read_csv(url_keluar)



#membangun komponen
header = html.Div([html.H1("Aplikasi Simulasi Kapasitas Embung E ITERA"), html.H3("Kelompok 7")],style={
    "textAlign" : "center",
    "height": "4 rem",
    "padding": "2rem 1rem",
    "background-color": "lightgreen",
})
footer = html.Div([html.H1("Tentang Kami"), html.H5("Kelompok 7"), html.P("Ketua Kelompok : Juan"), html.P("Sekertaris Kelompok : Evrilia"), html.P("Anggota Kelompok : | Kevin | Alfredo | Tasya | Anggi | Tria "),html.P('Berikut pertanggungjawaban kelompok kami bisa dilihat di "Dokumentasi" berikut.'),dbc.Button("Dokumentasi", color="info", href="https://drive.google.com/drive/folders/158PC3il9WsR1KsVVsoNUHCFRbpisiyLY?usp=sharing")],style={
    "textAlign" : "none",
    "top": 0,
    "left": 0,
    "right": " 4 rem",
    "height": "2 rem",
    "padding": "1rem 1rem",
    "background-color": "lightgray",
})




subtitle = html.P("Ketika melakukan simulasi Neraca Air suatu embung, komponen yang paling penting adalah inflow dan kebutuhan air. Jika kapasitas penyimpanan embung adalah tetap, embung bisa kering atau menjadi penuh dan mulai limpas. Dengan mempertimbangkan aspek-aspek seperti tersebut diatas, Neraca Air di embung dapat ditulis sebagai berikut:S(t) = S(t-1)+ (I-O)dt",style={})

datamasuk_gam = go.FigureWidget()
datamasuk_gam.add_bar(name="Chart Air Curah Hujan", x=df_masuk['Bulan'], y=df_masuk['Data-masuk'])
datamasuk_gam.add_bar(name="Chart Air Debit Air", x=df_masuk['Bulan'], y=df_masuk['Data-masuk-2'])
datamasuk_gam.layout.title = 'Chart Inflow Embung '

datakeluar_gam = go.FigureWidget()
datakeluar_gam.add_scatter(name="Outflow Suhu Temperatur" , x=df_keluar['Bulan'], y=df_keluar['Data-keluar'])
datakeluar_gam.add_scatter(name="Outflow Kecepatan Angin" , x=df_keluar['Bulan'], y=df_keluar['Data-keluar-2'])
datakeluar_gam.layout.title = 'Chart Outflow Embung'

simulation_fig = go.FigureWidget()
# simulation_fig.add_scatter(name='Outflow', x=df_outflow['Bulan'], y=df_outflow['Data'])
simulation_fig.layout.title = 'Simulation'


#layout aplikasi
app.layout = html.Div(
    [
        dbc.Row([header, subtitle])  ,
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=datamasuk_gam)]),
               
            ]
            ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=datakeluar_gam)]),
                
            ]
            ),
        html.Div(
            [
                dbc.Button('Simulasi', color="danger",id='run-button', n_clicks=0)
            ],style = {'textAlign': 'center'})
        , 
        html.Div(id='output-container-button', children='Klik tombol "Simulasi" untuk menjalankan .', style = {'textAlign': 'center'}),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id='simulation-result', figure=simulation_fig)])
            ]
        ),
        footer
    ]
    
)

#interaksi aplikasi
@app.callback(
    Output(component_id='simulation-result', component_property='figure'),
    Input('run-button', 'n_clicks')
)


def graph_update(n_clicks):
    # filtering based on the slide and dropdown selection
    if n_clicks >=1:
        #program numerik ---start----
        inout1 =  (df_masuk['jumlah'].values - df_keluar['jumlah'].values)
        N = len(inout1)
        u = np.zeros(N)
        u0 = 196800
        u[0] = u0
        dt = 1

        #metode Euler
        for n in range(N-1):
            u[n + 1] = u[n] + dt*inout1[n] 
        #program numerik ---end----


        # the figure/plot created using the data filtered above 
        simulation_fig = go.FigureWidget()
        simulation_fig.add_scatter(name='Simulation', x=df_keluar['Bulan'], y=u)
        simulation_fig.layout.title = 'Hasil Simulasi'

        return simulation_fig
    else:
        simulation_fig = go.FigureWidget()
        simulation_fig.layout.title = 'Simulasi Kapasitas Embung E ITERA '

        return simulation_fig

    


#jalankan aplikasi
if __name__=='__main__':
    app.run_server()

#debug=True, port=1191
