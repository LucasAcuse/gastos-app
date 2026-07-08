from flask import Flask, request, jsonify


app = Flask(__name__)  # Crea el servidor


gastos = [] 
#Arma el gasto como diccionario
def agregar_gasto(descripcion, monto):
    dicc = {'descripcion': descripcion, 'monto': monto} 
    gastos.append(dicc)  # Lo agrega a la lista


#Suma cada monto
def calcular_total():
    total = 0
    for dicc in gastos:
        total = total + dicc['monto']
    return total




#Ruta GET: devuelve todos los gastos y el total (reemplaza el print del menú opción 2)
@app.route('/gastos', methods=['GET'])
def ver_gastos():
    total = calcular_total()
    return jsonify({'gastos': gastos, 'total': total})




#Ruta POST: recibe un gasto nuevo y lo guarda (reemplaza el input del menú opción 1)
@app.route('/gastos', methods=['POST'])
def nuevo_gasto():
    datos = request.get_json()  # Lee los datos enviados por el usuario


    descripcion = datos.get('descripcion')
    monto = datos.get('monto')


    if not descripcion or monto is None:
        return jsonify({'error': 'Faltan campos: descripcion y monto'}), 400  # Error si faltan datos


    agregar_gasto(descripcion, float(monto))
    return jsonify({'mensaje': 'Gasto agregado correctamente.'}), 201  # Confirma que se guardó




if __name__ == 'main':
    app.run(debug=True)  # Inicia el servidor (debug=True muestra errores detallados)
