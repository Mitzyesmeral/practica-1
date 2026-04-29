from flask import Flask, render_template, request, redirect, url_for, flash, session
from gestor_tarea import GestorTareas
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esto-en-produccion")
gestor = GestorTareas(uri=os.environ.get("MONGO_URL", "mongodb://localhost:27017/"))
@app.route("/")
def index():
    """Página de inicio de sesión."""
    return render_template("index.html")


@app.route("/registro")
def registro():
    """Página de registro."""
    return render_template("registro.html")


@app.route("/pagina1")
def pagina1():
    """Página principal después de iniciar sesión / registrarse."""
    if "usuario_id" not in session:
        flash("Primero inicia sesión.", "warning")
        return redirect(url_for("index"))
    tareas = gestor.obtener_tareas_usuario(session["usuario_id"])
    return render_template("pagina1.html", tareas=tareas, nombre=session.get("nombre"))


@app.route("/datos")
def datos_usuario():
    """Tabla con los datos del usuario y sus tareas."""
    if "usuario_id" not in session:
        flash("Primero inicia sesión.", "warning")
        return redirect(url_for("index"))
    tareas = gestor.obtener_tareas_usuario(session["usuario_id"])
    return render_template(
        "datos_usuario.html",
        tareas=tareas,
        nombre=session.get("nombre"),
        email=session.get("email"),
    )

@app.route("/login", methods=["POST"])
def login():
    """Login simple por email (sin contraseña en esta práctica)."""
    email = (request.form.get("email") or "").strip().lower()
    if not email:
        flash("Ingresa tu email.", "danger")
        return redirect(url_for("index"))

    usuario = gestor.usuarios.find_one({"email": email}, {"_id": 1, "nombre": 1, "email": 1})
    if not usuario:
        flash("No existe una cuenta con ese email. Regístrate primero.", "warning")
        return redirect(url_for("registro"))

    session["usuario_id"] = str(usuario["_id"])
    session["nombre"] = usuario.get("nombre", "")
    session["email"] = usuario["email"]
    return redirect(url_for("pagina1"))


@app.route("/registrar", methods=["POST"])
def registrar():
    """Crea el usuario en MongoDB y redirige a /pagina1."""
    nombre = (request.form.get("nombre") or "Usuario").strip()
    email = (request.form.get("email") or "").strip().lower()
    if not email:
        flash("Ingresa tu email.", "danger")
        return redirect(url_for("registro"))

    usuario_id = gestor.crear_usuario(nombre, email)
    if not usuario_id:
        existente = gestor.usuarios.find_one({"email": email}, {"_id": 1, "nombre": 1, "email": 1})
        if not existente:
            flash("No se pudo registrar. Intenta de nuevo.", "danger")
            return redirect(url_for("registro"))
        usuario_id = str(existente["_id"])
        nombre = existente.get("nombre", nombre)

    session["usuario_id"] = usuario_id
    session["nombre"] = nombre
    session["email"] = email
    return redirect(url_for("pagina1"))


@app.route("/tareas/crear", methods=["POST"])
def crear_tarea():
    if "usuario_id" not in session:
        return redirect(url_for("index"))
    titulo = (request.form.get("titulo") or "").strip()
    materia = (request.form.get("materia") or "").strip()
    apuntes = (request.form.get("apuntes") or "").strip()
    if titulo:
        descripcion = " | ".join(p for p in [materia and f"Materia: {materia}", apuntes] if p)
        gestor.crear_tarea(session["usuario_id"], titulo, descripcion)
    return redirect(url_for("pagina1"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)