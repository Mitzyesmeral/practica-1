from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key='Mi_llave_segura_super_secreta'

usuarios_registrados = {
    "usuario1@example.com": {"nombre": "Usuario 1", "password": "contraseña1"},
    "usuario2@example.com": {"nombre": "Usuario 2", "password": "contraseña2"},
}
@app.route("/")
def home():
    returnrender_template('index.html')

@app.route('/login', metods=["POST"])
def login():
    if reques.method =="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        
    if emailin usuarios_registrados and usuaros_registrados[email] == password:
        sesssion['usuario']=email
        flash('Inicio de sesion revisado y ¡exitoso!','sucess')
        return redirect(url_for('dashboard'))
    else:
        flassh('Correo o contraseña incorrectas, intentalo nuevamente.','danger')
        return redirect(url_for("login"))
    
    return render_template(url_for('login.html'))

@app.route(/dashboard)
def dashboard():
    if 'usuario' in session:
        return f"<h1>Hola{session['usuario']}! Bienvenido a base.</h1>"
    return redirect(url_for('login'))

@app.route(/registro)
def registro():
    return"<h1>Pagina de registro </h1>"

{% with messages = get_flasehes(with_categories=true) %}
    {% if messages %}6
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}

if __name__ == "__main__":
    app.run(debug=True)