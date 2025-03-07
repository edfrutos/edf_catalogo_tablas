# Añadir importaciones necesarias
import traceback
from functools import wraps
from flask import jsonify, current_app, request

# Configurar el manejador de errores global
@app.errorhandler(500)
def handle_500(e):
    logger.error(f"Error 500: {str(e)}")
    return render_template("error.html", error=str(e)), 500
    
@app.errorhandler(404)
def handle_404(e):
    return render_template("not_found.html"), 404

# Función decoradora para manejar excepciones en rutas
def route_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Registrar el error en logs
            error_msg = f"Error en {func.__name__}: {str(e)}"
            stack_trace = traceback.format_exc()
            logger.error(f"{error_msg}\n{stack_trace}")
            
            # Si estamos en una ruta que maneja JSON, devolver JSON
            if request.path.startswith('/api/'):
                return jsonify({"error": str(e)}), 500
            
            # Mostrar una página de error amigable con detalles técnicos
            return render_template("error.html", error=str(e), 
                                 traceback=stack_trace), 500
    
    return wrapper

# Mejorar el manejo de la conexión con MongoDB
def get_db_connection():
    try:
        client = MongoClient(os.environ.get("MONGO_URI"))
        db = client.catalogo
        logger.info("Conexión a MongoDB establecida correctamente")
        return db
    except Exception as e:
        logger.error(f"Error al conectar con MongoDB: {str(e)}")
        raise

