import argparse

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

def main():
    # Parsear argumentos de línea de comandos
    args = parse_arguments()

    # Mostrar la ubicación y formato ingresado por el usuario
    print(f"Consultando el clima para: {args.ubicacion}")
    print(f"Formato de salida: {args.formato}")

    # Aquí es donde se implementará la lógica para consultar la API de clima
    # Por ahora, solo mostramos un mensaje de prueba.
    print("Esta es una aplicación CLI de ejemplo.")

if __name__ == "__main__":
    main()

