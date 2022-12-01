import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
from streamlit_lottie import st_lottie
from PIL import Image


# Page setting
st.set_page_config(page_title= 'Programas Internacionales', page_icon= ':airplane:',layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Funciones
@st.cache
def load_data(nrows):
    data = pd.read_csv('internacional.csv', nrows=nrows)
    return data

def load_lottiefile(filepath: str):
    with open (filepath, 'r') as f:
        return json.load(f)

def selec_periodo(periodo):
    if periodo == 'Enero-Junio':
        return r'Enero|Febrero|Junio|Mayo'
    elif periodo == 'Agosto-Diciembre':
        return r'Agosto|Septiembre|Diciembre'
    elif periodo == 'Verano':
        return r'Verano|Julio'
    else:
        return 'Invierno'

def dataPeriodo(periodo,año):
    df_filt = df_limp[(df_limp['PeriodoAcadémico'].str.contains(periodo)) & (df_limp['PeriodoAcadémico'].str.contains(año))]
    return df_filt

def metricaMayor(m1,m2):
    if m1 > m2:
        return m1,-m2
    else:
        return -m1,m2



# Titulo
st.title('Programas Internacionales :airplane:')
st.markdown('---')

# # Intro
# lottie_img = load_lottiefile('/Users/neira/Desktop/Concentración/Chuy/Intercambio Webapp/images/travelers.json')

st.markdown('### Introducción')
# col1, col2 = st.columns(2)
st.markdown('''
A continuación se muestra la **base de datos** del departamento de **Programas Internacionales**, la cual contiene registros de las solicitudes
de oportunidades de estudio en el extranjero de los alumnos del Tecnológico de Monterrey. Esta base de datos será utilizada para analizar y encontrar hallazgos
que permitan tomar decisiones estratégicas con base en los resultados. Se tomará la base de datos y se hará una limpieza que permita que los datos puedan ser analizados
de manera más eficiente. Además se mostraran visualizaciones para obtener una comprensión visual de los hallazgos.
''')
# lot = st_lottie(
#     lottie_img
# )
# col2.markdown(lot, unsafe_allow_html= True)
st.markdown('---')



# Data Frame
st.markdown('### DataFrame')
st.write('''
Este Data Frame contiene instancias de las solicitudes de estudios extranjeros, contiene datos categoricos como 'Nivel' de estudio, 'Estatus'
de asignación, etc. Dato Númericos como 'Promedio' , 'Núm. MatAprobadas', etc. Los alumnos pueden tener más de una instancia de solicitud, esto debido
a que el estatus de la solicitud puede terminar Rechazado, sin embargo esto no impide que puedan meter otra solicitud.
''')

df = load_data(1000)
st.dataframe(df.head(20))

st.caption('Ejemplo de 20 instancias del Data Frame')
st.markdown('---')







# Limpieza de Datos
st.markdown('### Limpieza de Datos')
st.write('1. Eliminar datos nulos')
st.code(''' df = df.dropna() #Eliminamos datos nulos del DF
df['Estatuslimpio'] = df['Estatus'].str[:1] # Creamos una nueva columna con la inicial del estatus''', language='python')

st.write('2. Limpiar columna de Estatus de Asignación')
st.code('''
df = df.replace(['A', 'P'], 'Asignado') #Se reemplazan las opciones de 'Asignado' y 'Pre-Asignado' por 'Asignado'
df = df.replace(['E', 'I', 'C', 'T', 'R', 'N'], 'Rechazado') #Se reemplazan las demás opciones por 'Rechazado' ''')

st.write('3. Limpiar columna de Programas')
st.code('''
df['Programa'] = df['Programa'].str[:3] #Se toman las 3 primeras siglas que indican la carrera''')

st.write('4. Limpiar columna de Oportunidades Seleccionadas')
st.code('''
df['OportunidadesSeleccionadas'] = df['OportunidadesSeleccionadas'].str[3:17] # Agarra la primera selección de la lista de oportunidades
df['OportunidadesSeleccionadas'] = df['OportunidadesSeleccionadas'].map(lambda x: x.rstrip('<')) # Elimna los caracteres despues del '<'
df['OportunidadesSeleccionadas'] = df['OportunidadesSeleccionadas'].map(lambda x: x.rstrip(',').lstrip(' ')) # Elimina los caracteres despues del ',' ''')

st.write('5. Construcción de valores de Intercambio Internación')
st.code('''
df.loc[df['OportunidadAsignada'].str.contains('INT') & (df['Estatuslimpio'] == 'Asignado'), 'Intercambio Internacional'] = 'Si' #Si es Intercambio y la solicitud es Asignada se define como Si
df['Intercambio Internacional'].fillna('No', inplace=True) #Las filas que no cumplan la condición se llenan con no''') 

st.write('6. Construcción de valores de Primera Opción')
st.code('''
df.loc[(df['OportunidadAsignada'] == df['OportunidadesSeleccionadas']) & (df['Estatuslimpio'] == 'Asignado'), 'PrimeraOpcion'] = 'Si'
df['PrimeraOpcion'].fillna('No', inplace=True)''')

st.write('7. Asignación de valores a las Columnas')
st.code('''
df['PaisSeleccionado'] = df['OportunidadesSeleccionadas'].str[:3]
df['PaisAsignado'] = df['OportunidadAsignada'].str[:3]''')

st.write('8. Reemplazar siglas de paises')
st.code('''
#Asignamos Nombre a las siglas
df = df.replace('ESP', 'España')
df = df.replace('FRA', 'Francia')
df = df.replace('CAN', 'Canada')
df = df.replace('ALE', 'Alemania')
df = df.replace('MEX', 'México')
df = df.replace('EUA', 'Estados Unidos')
df = df.replace('CZE', 'República Checa')
df = df.replace('ITA', 'Italia')
df = df.replace('AUS', 'Austria')
df = df.replace('ING', 'Inglaterra')
df = df.replace('CHN', 'China')
df = df.replace('CHL', 'Chile')
df = df.replace(['COR', 'COL', 'ARG','SUI','HOL','BEL','SVK','SUE',
'JAP','HUN','DIN','FIN','POL','SIN','AUT','TAI','CRO',
'URU','RUS','NZL','POR','SVN','MUN','TUR','EAU','BRA',
'SER','LVA','NOR','CHI','ISR','CUB','IRL','PAN','CRC',
'PER','SCO','HKG','ECU','PRC','ISL','IND','Mul','DOM',
'LTU','MYS','PRY','SAF','MCO','EST','IDN'], 'Otro')''')


st.write('8. Reemplazar Campus por Región')
st.code('''
def region(df): 
    if ('Aguascalientes' in df['Campus']) | ('Chihuahua' in df['Campus']) | ('Guadalajara' in df['Campus']) | ('León' in df['Campus']) | ('Morelia' in df['Campus']) | ('Sinaloa' in df['Campus']) | ('Sonora Norte' in df['Campus']):   
        return 'Occidente'
    elif ('Laguna' in df['Campus']) | ('Monterrey' in df['Campus']) | ('Saltillo' in df['Campus']) | ('Universidad Virtual' in df['Campus']) | ('EGADE Monterrey' in df['Campus']) | ('EGAP Monterrey' in df['Campus']):   
        return 'Norte'
    elif ('Ciudad de México' in df['Campus']) | ('Estado de México' in df['Campus']) | ('Santa Fe' in df['Campus']) | ('EGADE Santa Fe' in df['Campus']) | ('EGADE Ciudad de Mexico' in df['Campus']) | ('EGAP Santa Fe' in df['Campus']):   
        return 'Ciudad de Mexico'
    elif ('Cuernavaca' in df['Campus']) | ('Hidalgo​​​​​​' in df['Campus']) | ('Puebla' in df['Campus']) | ('Querétaro' in df['Campus']) | ('San Luis Potosí' in df['Campus']) | ('Tampico' in df['Campus']) | ('Toluca' in df['Campus']):   
        return 'Centro Sur'
    else:
        return 'Desarrollo Regional' 
        
df['Región'] = df.apply(region, axis = 1) ''')

st.markdown('---')

# Hipotesis 1
df_limp = pd.read_csv('programasinternacionaleslimpio.csv')
si_count = len(df_limp[df_limp['PrimeraOpcion'] == 'Si'])
no_count = len(df_limp[df_limp['PrimeraOpcion'] == 'No'])
m1 = round((si_count / df_limp['PrimeraOpcion'].count()) * 100, 2)
m2 = round((no_count / df_limp['PrimeraOpcion'].count()) * 100, 2)

si_per, no_per = metricaMayor(m1, m2)

st.markdown('### Hipotesis #1')
st.markdown('#### Pregunta #1 ¿el 96% de los estudiantes que aplican a un programa académico en el extranjero quedan en su primera opción?')
col1, col2 = st.columns(2)
col1.metric("Si quedan", si_count, f'{si_per}%')
col2.metric("No quedan", no_count, f'{no_per}%')

 ## Construcción de Sankey 
df_temp1 = df_limp.groupby(['Región', 'Intercambio Internacional'])['Matrícula'].count().reset_index()
df_temp1.columns = ['source', 'target', 'value']

df_temp2 = df_limp.groupby(['Intercambio Internacional', 'PrimeraOpcion'])['Matrícula'].count().reset_index()
df_temp2.columns = ['source', 'target', 'value']

df_temp3 = df_limp.groupby(['PrimeraOpcion', 'PaisAsignado'])['Matrícula'].count().reset_index()
df_temp3.columns = ['source', 'target', 'value']

links = pd.concat([df_temp1, df_temp2, df_temp3], axis = 0)
unique_source_target = list(pd.unique(links[['source', 'target']].values.ravel('K')))
mapping_dict = {k : v for v, k in enumerate(unique_source_target)}
links['source'] = links['source'].map(mapping_dict)
links['target'] = links['target'].map(mapping_dict)
links_dict = links.to_dict(orient = 'list')

#Sankey
fig = go.Figure(data=[go.Sankey(
    node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = 'black', width = 0.5),
        label = unique_source_target,
        color = 'blue'
    ),

    link = dict(
        source = links_dict['source'],
        target = links_dict['target'],
        value = links_dict['value']
    )
)] 
)
st.plotly_chart(fig, use_container_width=False)
st.markdown('---')





# Hipotesis 2
st.markdown('### Hipotesis #2')
st.markdown('#### ¿Cada periodo el 80% de los alumnos se internacionalizan vía intercambio y solo el 20% se internacionaliza con un study abroad, certificación, verano o invierno?')

 ## Selección de periodo
col1, col2 = st.columns(2)
periodo = col1.selectbox(
    label= 'Seleccione el periodo',
    options= ['Invierno', 'Enero-Junio', 'Verano', 'Agosto-Diciembre'],
    index=1
)
año = col2.selectbox(
    label= 'Seleccione el Año',
    options= ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'],
    index=7
)

p = selec_periodo(periodo)
df_filt = dataPeriodo(p,año)

col1, col2 = st.columns(2)
inter_count = len(df_filt[df_filt['Intercambio Internacional'] == 'Intercambio Internacional'])
sa_count = len(df_filt[df_filt['Intercambio Internacional'] == 'Study Abroad'])
m1 = round((inter_count / df_filt['Intercambio Internacional'].count()) * 100, 2)
m2 = round((sa_count / df_filt['Intercambio Internacional'].count()) * 100, 2)

inter_per, sa_per = metricaMayor(m1, m2)

col1.metric("Intercambio", inter_count, f'{inter_per}%')
col2.metric("Study Abroad", sa_count, f'{sa_per}%')

figSun = px.sunburst(data_frame=df_filt, path=['Intercambio Internacional', 'PrimeraOpcion', 'PaisAsignado'])
st.plotly_chart(figSun, use_container_width=False)

st.markdown('---')

# # Mapa de los países más visitados
# st.markdown('### Países más visitados')
# df = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(df)
# st.markdown('---')

# # Widgets
# st.markdown('### Widgets que me serviran más alrato')
# col1, col2, col3, col4, col5, col6 = st.columns(6)
# ## Botón 
# if col1.button('Say hello'):
#     st.write('Why hello there')
# else:
#     st.write('Goodbye')

# ## Download Botón
# @st.cache
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv().encode('utf-8')

# csv = convert_df(df)

# col2.download_button(
#     label="Download data as CSV",
#     data=csv,
#     file_name='large_df.csv',
#     mime='text/csv',
# )

# ## Checkbox
# agree = col3.checkbox('I agree')

# if agree:
#     st.write('Great!')

# ## Radio
# genre = col4.radio(
#     "What's your favorite movie genre",
#     ('Comedy', 'Drama', 'Documentary'))

# if genre == 'Comedy':
#     st.write('You selected comedy.')
# else:
#     st.write("You didn't select comedy.")

# ## Selectbox
# option = col5.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone'))

# st.write('You selected:', option)

# ## Multiselect
# options = col6.multiselect(
#     'What are your favorite colors',
#     ['Green', 'Yellow', 'Red', 'Blue'],
#     ['Yellow', 'Red'])

# st.write('You selected:', options)

# # Widgets/Slider
# st.markdown('### Sliders')
# col1, col2 = st.columns(2)

# ## Range Slider
# values = col1.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0))
# st.write('Values:', values)

# ## Datetime Slider
# start_time = col2.slider(
#     "When do you start?",
#     value=datetime(2020, 1, 1, 9, 30),
#     format="MM/DD/YY - hh:mm")
# st.write("Start time:", start_time)

# # Widgets/ Inputs
# col1, col2, col3, col4, col5, col6 = st.columns(6)

# ## Text Input
# title = col1.text_input('Movie title', 'Life of Brian')
# st.write('The current movie title is', title)

# ## Number Input
# number = col2.number_input('Insert a number')
# st.write('The current number is ', number)

# ## Date Input
# d = col3.date_input(
#     "When's your birthday",
#     date(2019, 7, 6))
# st.write('Your birthday is:', d)