from flask import Flask, request, jsonify, render_template  # 1. imports

app = Flask(__name__)  # 2. crear app

import logging
logging.basicConfig(level=logging.DEBUG)

gastos = []  # 3. variables

# 4. funciones
def agregar_gasto(descripcion, monto):
    dicc = {'descripcion': descripcion, 'monto': monto}
    gastos.append(dicc)

def calcular_total():
    total = 0
    for dicc in gastos:
        total = total + dicc['monto']
    return total

# 5. rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gastos', methods=['GET'])
def ver_gastos():
    total = calcular_total()
    return jsonify({'gastos': gastos, 'total': total})

@app.route('/gastos', methods=['POST'])
def nuevo_gasto():
    datos = request.get_json()
    descripcion = datos.get('descripcion')
    monto = datos.get('monto')
    if not descripcion or monto is None:
        return jsonify({'error': 'Faltan campos: descripcion y monto'}), 400
    agregar_gasto(descripcion, float(monto))
    return jsonify({'mensaje': 'Gasto agregado correctamente.'}), 201

if __name__ == '__main__':
    app.run(debug=True)
