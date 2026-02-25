from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

API_URL = "http://localhost:5000/v1/usuarios/"

@app.route("/")
def index():
    response = requests.get(API_URL)
    data = response.json()
    usuarios = data["Usuarios"]
    return render_template("index.html", usuarios=usuarios)

@app.route("/agregar", methods=["POST"])
def agregar():
    nuevo_usuario = {
        "id": int(request.form["id"]),
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
    }
    requests.post(API_URL, json=nuevo_usuario)
    return redirect("/")

@app.route("/eliminar/<int:id>")
def eliminar(id):
    requests.delete(f"http://localhost:5000/v1/usuarios/{id}")
    return redirect("/")

@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    datos_actualizados = {
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
    }
    requests.put(f"http://localhost:5000/v1/usuarios/{id}", json=datos_actualizados)
    return redirect("/")

if __name__ == "__main__":
    app.run(port=3000, debug=True)
