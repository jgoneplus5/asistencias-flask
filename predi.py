from flask import Flask, render_template, request

app = Flask(__name__)

# Simulamos una base de datos en memoria
registros = []

LUGARES = [
    "Luis Cabrera y San Bernabé",
    "Luis Cabrera y Orquídea",
    "Luis Cabrera y Las Torres",
    "Parque La Malinche"
]

DIAS = ["Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

@app.route("/", methods=["GET", "POST"])
def formulario():
    mensaje = ""
    if request.method == "POST":
        nombre = request.form.get("nombre")
        dia = request.form.get("dia")
        lugar = request.form.get("lugar")

        # Validación de campos
        if not nombre or not dia or not lugar:
            mensaje = "Todos los campos son obligatorios."
        else:
            # Contar registros existentes para ese lugar/día
            count = sum(1 for r in registros if r["dia"] == dia and r["lugar"] == lugar)
            if count >= 3:
                mensaje = f"Cupo lleno para {lugar} el día {dia}."
            else:
                registros.append({"nombre": nombre, "dia": dia, "lugar": lugar})
                mensaje = f"{nombre} registrado correctamente en {lugar} el día {dia}."

    # Crear diccionario para la tabla de disponibilidad
    disponibilidad = {l: {d: [] for d in DIAS} for l in LUGARES}
    for r in registros:
        disponibilidad[r["lugar"]][r["dia"]].append(r["nombre"])

    return render_template(
        "formulario.html",
        registros=registros,
        lugares=LUGARES,
        dias=DIAS,
        mensaje=mensaje,
        disponibilidad=disponibilidad
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
