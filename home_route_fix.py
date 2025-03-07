@app.route("/")
def home():
    try:
        logger.info("Acceso a la ruta principal '/'")
        if "usuario" not in session:
