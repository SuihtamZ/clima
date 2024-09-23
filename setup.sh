# Salir inmediatamente si un comando falla
set -e

echo "Configurando el entorno para Weather CLI..."

# Verificar si Python está instalado
if ! command -v python &> /dev/null
then
    echo "Error: Python no está instalado. Por favor, instala Python antes de continuar."
    exit 1
fi

# Crear un entorno virtual llamado '.venv' si no existe
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python -m venv .venv
else
    echo "Entorno virtual '.venv' ya existe."
fi

# Activar el entorno virtual
echo "Activando entorno virtual..."
source .venv/Scripts/activate

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias desde requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt
else
    echo "Error: No se encontró 'requirements.txt'. Asegúrate de que exista en el directorio raíz."
    deactivate
    exit 1
fi

echo "Entorno configurado exitosamente."

echo "Ejecutar la aplicación Weather con parámetros predeterminados..."
python weather.py "Asuncion, PY" --formato texto

#Desactivando entorno virtual
deactivate
