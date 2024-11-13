import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# Importación de datos
columns = ["id","station","municipality","lat","lng"]
stations = pd.read_csv("data_stations.txt", names=columns)

columns_trips = ["id", "duration", "start_date", "start_station", "end_date", "end_station", "bike_number", "sub_type", "zip_code", "birth_date", "gender"]
trips = pd.read_csv("data_trips.txt", sep=",", names=columns_trips, on_bad_lines="skip")

st.title("Análisis de datos de viajes")
st.caption("En este dashboard se presentan varios resultados y gráficos que responden a diferentes cuestiones planteadas sobre los datos facilitados.")
st.divider()


# EJERCICIO A
# Calcular media duración viajes
duracion_media = trips["duration"].mean()

# Calcular número total trayectos
total_trayectos = trips.shape[0]

# Mostrar los resultados
st.write(f"**Duración media de los viajes:** {duracion_media:.2f} segundos")
st.write(f"**Número total de trayectos:** {total_trayectos}")

# Mostrar una gráfica de barras con el número total de trayectos (por ejemplo, por tipo de usuario)
trayectos_por_tipo = trips['sub_type'].value_counts().reset_index(name='trip_count')
bar_chart = px.bar(trayectos_por_tipo, x='sub_type', y='trip_count', title="Número total de trayectos por tipo de usuario")
st.plotly_chart(bar_chart)


# EJERCICIO B
# Convertir la duración de los viajes a minutos  (suponiendo que están en segundos)
trips['duration_minutes'] = trips['duration'] / 60
        
# Calcular la edad del cliente (suponiendo que birth_date es el año de nacimiento)
current_year = datetime.now().year
trips['age'] = current_year - trips['birth_date']
        
# Crear rangos de edad 
bins = [0, 18, 30, 40, 50, 60, 100]
labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '60+']
trips['age_group'] = pd.cut(trips['age'], bins=bins, labels=labels, right=False)
     
# Calcular los minutos por grupo de edad
minutos_por_edad = trips.groupby('age_group')['duration_minutes'].sum().round(1).reset_index(name='minutes_count')

# Mostrar gráfico de barras
bar_chart = px.bar(minutos_por_edad, x='age_group', y='minutes_count', title="Minutos de bibicleta según edad del cliente")
st.plotly_chart(bar_chart)
st.write(minutos_por_edad)


# EJERCICIO C
# Filtramos solo los viajes reales(duran más de 1 minuto)
trips_reales = trips[trips["duration_minutes"] > 1]

# Calcular la edad del cliente (suponiendo que birth_date es el año de nacimiento)
current_year = datetime.now().year
trips_reales['age'] = current_year - trips_reales['birth_date']
        
# Crear rangos de edad 
bins = [0, 18, 30, 40, 50, 60, 100]
labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '60+']
trips_reales['age_group'] = pd.cut(trips_reales['age'], bins=bins, labels=labels, right=False)
     
# Calcular los minutos por grupo de edad
minutos_reales_por_edad = trips_reales.groupby('age_group')['duration_minutes'].sum().round(1).reset_index(name='minutes_count')

# Mostrar gráfico de barras
bar_chart = px.bar(minutos_reales_por_edad, x='age_group', y='minutes_count', title="Minutos de bibicleta (de viajes de más de 1 minuto) según edad del cliente")
st.plotly_chart(bar_chart)
st.write(minutos_reales_por_edad)
st.divider()


# EJERCICIO D
# Cálculo de la media de los viajes reales en minutos, sin decimales
duracion_media_reales = trips_reales["duration"].mean()
duracion_media_min = duracion_media_reales // 60

# Mostrar resultado
st.header("Duración")
st.metric("Duración media de los viajes reales", f"{int(duracion_media_min)} min")

# Número de bicicletas
numero_bicis = trips['bike_number'].unique().shape[0]
st.write(f"**Número de bicicletas registradas:** {numero_bicis}")


# EJERCICIO E
bicicletas_viajes = trips['bike_number'].value_counts().reset_index(name='num_viajes')
st.write("Bicicletas y número de viajes que han realizado:")
st.write(bicicletas_viajes)


# EJERCICIO F
# Primero obtenemos el identificador de la estación 'Fan Pier' de la tabla stations
fan_pier_id = stations.loc[stations['station'] == '\'Fan Pier\'', 'id'].values[0]

# Filtramos los viajes que hayan salido de Fan Pier
trips_fan_pier = trips[trips['start_station'] == fan_pier_id]

# Ordenamos por duración en orden descendente y seleccionamos los 10 más largos
trips_fan_pier_10longest = trips_fan_pier.sort_values(by='duration', ascending=False).head(10)

st.write("Top 10 viajes más duraderos desde la estación Fan Pier:")
st.write(trips_fan_pier_10longest) 


# EJERCICIO G
# Crearemos un selector en el que el usuario podrá elegir la estación que desee
# Podrá ver cuantos viajes han salido y regresado a la misma estación seleccionada
st.subheader("Viajes circulares por estación")

# Creamos un diccionario con los nombres de las estaciones y sus identificadores para el selector
station_dict = stations.set_index('id')['station'].to_dict()

# Creamos un filtro de selección de estación en Streamlit
selected_station_name = st.selectbox("Selecciona una estación:", sorted(station_dict.values()))

# Obtenemos el ID de la estación seleccionada
selected_station_id = [id for id, name in station_dict.items() if name == selected_station_name][0]

# Filtrar los viajes que salen y regresan a la misma estación
round_trips = trips[(trips['start_station'] == selected_station_id) & (trips['end_station'] == selected_station_id)]

# Contamos los viajes redondos
round_trip_count = len(round_trips)

st.write(f"**Número de viajes que salieron y regresaron a la estación '{selected_station_name}':** {round_trip_count}")


# EJERCICIO H
st.divider()
st.header("Análisis temporal")
st.write("En esta sección, el usuario tiene disponible para su visualización varios análisis temporales de los datos anteriores.")

# Convertimos las fechas a objetos de tipo datetime
trips['start_date'] = pd.to_datetime(trips['start_date'])
trips['end_date'] = pd.to_datetime(trips['end_date'])

# Extraer diferentes componentes de tiempo para el análisis
trips['start_date_only'] = trips['start_date'].dt.date  # Solo la fecha sin la hora
trips['start_hour'] = trips['start_date'].dt.hour   # Hora de inicio
trips['start_day_of_week'] = trips['start_date'].dt.day_name()  # Día de la semana
trips['start_year'] = trips['start_date'].dt.year   # Año

# Mostrar selector para el tipo de análisis
analysis_type = st.selectbox("Selecciona el tipo de análisis temporal:", 
    ["Distribución diaria de viajes", "Distribución por hora", "Días de la semana"])

# Análisis según la opción seleccionada
if analysis_type == "Distribución diaria de viajes":
    # Contar el número de viajes por día
    daily_trips = trips.groupby('start_date_only').size().reset_index(name='trip_count')
    fig = px.line(daily_trips, x='start_date_only', y='trip_count', title="Número de viajes por día")
    st.plotly_chart(fig)

elif analysis_type == "Distribución por hora":
    # Contar el número de viajes por hora del día
    hourly_trips = trips.groupby('start_hour').size().reset_index(name='trip_count')
    fig = px.bar(hourly_trips, x='start_hour', y='trip_count', title="Número de viajes por hora del día")
    st.plotly_chart(fig)

elif analysis_type == "Días de la semana":
     # Contar el número de viajes por día de la semana
    weekday_trips = trips.groupby('start_day_of_week').size().reset_index(name='trip_count')
    # Ordenar los días para que aparezcan en orden de lunes a domingo
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_trips['start_day_of_week'] = pd.Categorical(weekday_trips['start_day_of_week'], categories=weekday_order, ordered=True)
    weekday_trips = weekday_trips.sort_values('start_day_of_week')
    fig = px.bar(weekday_trips, x='start_day_of_week', y='trip_count', title="Número de viajes por día de la semana")
    st.plotly_chart(fig)


# Indicadores KPIs
st.divider()
st.header("Indicadores")

# KPI 1, Numero total de viajes realizados, vamos a considerar viajes reales
total_viajes = len(trips_reales)
st.metric("Número total de viajes reales realizados", total_viajes)

# KPI 2, Duracion promedio de los viajes
st.metric("Duración promedio de los viajes", f"{duracion_media_min:.2f} min")

# KPI 3, Uso por estación de inicio
st.write("Estaciones más usadas para iniciar trayectos:")
trips_per_station = trips['start_station'].value_counts().reset_index()
trips_per_station.columns = ['Estación','Número de viajes']
st.write(trips_per_station)

# KPI 4, Porcentaje de viajes realizados por usuarios registrados frente a usuarios ocasionales
porcentaje_casual = (len(trips[trips['sub_type'] == '\'Casual\'']) / total_viajes) * 100
porcentaje_registrado = (len(trips[trips['sub_type'] == '\'Registered\'']) / total_viajes) * 100

st.write("Porcentaje de viajes realizados por usuarios registrados frente a usuarios ocasionales.")
col1, col2 = st.columns(2)
col1.metric("Usuarios ocasionales", f"{porcentaje_casual:.1f}%")
col2.metric("Usuarios registrados", f"{porcentaje_registrado:.1f}%")

# KPI 5, índice de rotación de bicicletas
# Calcular el índice de rotación promedio
indice_rotacion_promedio = bicicletas_viajes['num_viajes'].mean()
st.write("Índice de rotación promedio de bicicletas.")
st.metric("Media de viajes por bicicleta", f"{indice_rotacion_promedio:.2f}")
