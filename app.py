from flask import Flask, request, jsonify, render_template
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

gastos = []


def calcular_total(lista):
    total = 0
    for dicc in lista:
        total = total + dicc['monto']
    return total


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gastos', methods=['GET'])
def ver_gastos():
    categoria = request.args.get('categoria')  # Filtro opcional por categoría
    if categoria and categoria != 'todas':
        filtrados = [g for g in gastos if g['categoria'] == categoria]
    else:
        filtrados = gastos
    total = calcular_total(filtrados)
    return jsonify({'gastos': filtrados, 'total': total})


@app.route('/gastos', methods=['POST'])
def nuevo_gasto():
    datos = request.get_json()
    descripcion = datos.get('descripcion')
    monto = datos.get('monto')
    categoria = datos.get('categoria', 'Sin categoría')

    if not descripcion or monto is None:
        return jsonify({'error': 'Faltan campos: descripcion y monto'}), 400

    gasto = {
        'id': len(gastos),
        'descripcion': descripcion,
        'monto': float(monto),
        'categoria': categoria
    }
    gastos.append(gasto)
    return jsonify({'mensaje': 'Gasto agregado correctamente.'}), 201


@app.route('/gastos/<int:id>', methods=['DELETE'])
def borrar_gasto(id):
    global gastos
    gastos = [g for g in gastos if g['id'] != id]  # Borra el gasto con ese ID
    return jsonify({'mensaje': 'Gasto eliminado correctamente.'}), 200


@app.route('/categorias', methods=['GET'])
def ver_categorias():
    categorias = list(set(g['categoria'] for g in gastos))  # Lista sin repetidos
    return jsonify({'categorias': categorias})


if __name__ == '__main__':
    app.run(debug=True)
