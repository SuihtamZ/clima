import argparse
import requests
import sys
import json
import csv

API_KEY = "3ed578c52d2cb9d7afd4c835118e3e80" 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Aplicación CLI para consultar el clima de una ubicación específica."
    )
    
    # Argumento requerido para la ubicación
    parser.add_argument(
        "ubicacion",
        type=str,
        help="Ubicación para consultar el clima (formato: ciudad, país)"
    )
    
    # Argumento opcional para el formato de salida
    parser.add_argument(
        "--formato",
        type=str,
        choices=["json", "csv", "texto"],
        default="texto",
        help="Formato de salida (json, csv o texto). Por defecto es texto."
    )

    return parser.parse_args()

def get_weather(location):
    try:
        # Construye la URL de solicitud con la ubicación y la API Key
        url = f"{BASE_URL}?q={location}&appid={API_KEY}&units=metric"
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

