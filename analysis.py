# Descripción de los datos

from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd

# Importar archivos
cabs_info = pd.read_csv('moved_project_sql_result_01.csv')
location_info = pd.read_csv('moved_project_sql_result_04.csv')

cabs_info.info()
location_info.info()

print(cabs_info.duplicated().sum())

print(location_info.duplicated().sum())

location_info.head()

# Analisis de datos

# Identificar los 10 principales barrios en términos de finalización del recorrido

top_ten_neighborhoods = location_info.sort_values(
    by='average_trips', ascending=False).head(10)
print(top_ten_neighborhoods)

# Graficar empresas de taxis y número de viajes.

top_companies = cabs_info.sort_values(
    by='trips_amount', ascending=False).head(10)
plt.figure(figsize=(12, 6))
plt.bar(top_companies['company_name'], top_companies['trips_amount'])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Graficar los 10 barrios principales por número de finalizaciones


plt.figure(figsize=(16, 12))
plt.bar(top_ten_neighborhoods['dropoff_location_name'],
        top_ten_neighborhoods['average_trips'])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.xlabel('Barrios')
plt.ylabel('Número de finalizaciones')
plt.show()

# Probar hipotesis: la duración promedio de los viajes desde el Loop hasta el Aeropuerto Internacional O'Hare cambia los sábados lluviosos".

# importar archivos de viajes desde Loop hasta O'Hare
trips_loop_ohare = pd.read_csv('moved_project_sql_result_07.csv')
trips_loop_ohare.info()

# Convertir a datetime
trips_loop_ohare['start_ts'] = pd.to_datetime(trips_loop_ohare['start_ts'])
trips_loop_ohare.head()


# Extraer el dia de la semana (0=Lunes, entonces 5=sabado)
trips_loop_ohare['day_of_week'] = trips_loop_ohare['start_ts'].dt.dayofweek

# Filtrar sábados lluviosos
trips_sat_rainy = trips_loop_ohare[(trips_loop_ohare['day_of_week'] == 5) & (
    trips_loop_ohare['weather_conditions'] == 'Bad')]

# Filtrar sábados no lluviosos
trips_sat_good = trips_loop_ohare[(trips_loop_ohare['day_of_week'] == 5) & (
    trips_loop_ohare['weather_conditions'] == 'Good')]

alpha_2 = .05  # Nivel de significancia 5%
print(f"Nivel de significancia (α): {alpha_2}")


# Realizar prueba t
t_stat, p_value = stats.ttest_ind(
    trips_sat_rainy['duration_seconds'], trips_sat_good['duration_seconds'])

print(f"Estadistico t: {t_stat:.4f}")
print(f"Valor p:{p_value:.4f}")

print(
    f"Duración promedio sábados lluviosos: {trips_sat_rainy['duration_seconds'].mean():.2f} segundos")
print(
    f"Duración promedio sábados no lluviosos: {trips_sat_good['duration_seconds'].mean():.2f} segundos")

if p_value < alpha_2:
    print(
        f"\nConclusión: Rechazamos la H₀ (p-value {p_value:.4f} < α {alpha_2})")
    print("La duracion promedio de los viajes desde Loop hasta el Aeropuerto Internacional O'Hare los sábados lluviosos y los sábados soleados SI son significativamente diferentes")
else:
    print(
        f"\nConclusión: No rechazamos la H₀ (p-value {p_value:.4f} ≥ α {alpha_2})")
    print("No hay evidencia suficiente de que la duracion promedio de los viajes entre Loop  y el Aeropuerto Internacional O'Hare los sábados lluviosos y los sábados soleados sean diferentes")
