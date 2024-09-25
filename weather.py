import argparse
import requests
import sys
import json
import csv
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
#print(f"API_KEY: {API_KEY}") eliminar solo para debug...
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Consulta el clima actual de una ciudad con esta sencilla herramienta CLI."
    )
    
    parser.add_argument( # Argumento requerido para la ubicación
        "ubicacion",
        type=str,
        help="Especifica la ciudad y el país para consultar el clima (formato: ciudad, país). Ejemplo: 'Asunción, PY'"
    )
    
    parser.add_argument( # Argumento opcional para el formato de salida
        "--formato",
        type=str,
        choices=["json", "csv", "texto"],
        default="texto",
        help="Selecciona el formato de salida de los datos: 'json', 'csv' o 'texto' (predeterminado: 'texto')."
    )

    return parser.parse_args()

def get_weather(location):
    try:
        # Construye la URL de solicitud con la ubicación y la API Key
        url = f"{BASE_URL}?q={location}&appid={API_KEY}&units=metric&lang=es"
        response = requests.get(url)

        # Verifica si la respuesta de la API es exitosa
        if response.status_code == 200:
            data = response.json()
            # Procesa y devuelve los datos relevantes
            city = data.get("name", "N/A")
            country = data.get("sys", {}).get("country", "N/A")
            temperature = data.get("main", {}).get("temp", "N/A")
            weather_description = data.get("weather", [{}])[0].get("description", "N/A")

            return {
                "city": city,
                "country": country,
                "temperature": temperature,
                "description": weather_description.capitalize()
            }
        elif response.status_code == 404:
            print("Error: Ubicación no encontrada. Verifica la ortografía e intenta de nuevo.")
        elif response.status_code == 401:
            print("Error: API Key inválida. Verifica tu API Key y vuelve a intentarlo.")
        else:
            print(f"Error: No se pudieron obtener datos. Código de estado: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Se produjo un error al consultar el clima: {e}")
    return None

def print_weather(data, formato):
    if formato == "json":
        print(json.dumps(data, indent=4, ensure_ascii=False))
    elif formato == "csv":
        # Crea un CSV en la salida estándar
        csv_output = f"{data['city']},{data['country']},{data['temperature']},{data['description']}"
        print(csv_output)
    else:  # Texto por defecto
        print(f"Clima en {data['city']}, {data['country']}:")
        print(f"Temperatura: {data['temperature']}°C")
        print(f"Condiciones: {data['description']}")

def main():
    # Parsear argumentos de línea de comandos
    args = parse_arguments()

    # Consultar el clima usando la API
    weather_data = get_weather(args.ubicacion)

    # Verificar si se obtuvieron datos y mostrarlos en el formato especificado
    if weather_data:
        print_weather(weather_data, args.formato)
    else:
        print("No se pudieron obtener datos de clima.")

if __name__ == "__main__":
    main()
