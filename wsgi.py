import sys
import os
from dotenv import load_dotenv

# Añadir la ruta de la aplicación al path de Python
sys.path.insert(0, '/var/www/vhosts/edefrutos2025.xyz/httpdocs')

# Cargar variables de entorno desde .env
dotenv_path = os.path.join('/var/www/vhosts/edefrutos2025.xyz/httpdocs', '.env')
load_dotenv(dotenv_path)

# Configurar el entorno virtual
python_home = '/var/www/vhosts/edefrutos2025.xyz/httpdocs/.venv'
python_bin = os.path.join(python_home, 'bin')

# Establecer variables de entorno para el entorno virtual
os.environ['VIRTUAL_ENV'] = python_home
os.environ['PATH'] = python_bin + os.pathsep + os.environ.get('PATH', '')

# Importar la aplicación
from app import app as application
