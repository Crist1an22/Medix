# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
import base64
import os
from datetime import datetime
import face_recognition

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

@app.route('/registrar_miembro', methods=['POST'])
def registrar_miembro():
    data = request.json
    nombre = data.get('nombre')
    imagen_base64 = data.get('imagen')

    if not nombre or not imagen_base64:
        return jsonify({'error': 'Faltan datos'}), 400

    carpeta = os.path.join(BASE_DIR, f'data/miembros/{nombre}')
    os.makedirs(carpeta, exist_ok=True)

    try:
        img_data = base64.b64decode(imagen_base64.split(',')[1])
        np_img = np.frombuffer(img_data, np.uint8)
        imagen = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        filename = f'rostro_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        ruta_imagen = os.path.join(carpeta, filename)
        cv2.imwrite(ruta_imagen, imagen)

        return jsonify({'mensaje': 'Rostro guardado'}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Error al procesar el rostro'}), 500


@app.route('/registrar_producto', methods=['POST'])
def registrar_producto():
    data = request.json
    codigo = data.get('codigo')
    imagen_base64 = data.get('imagen')

    if not codigo or not imagen_base64:
        return jsonify({'error': 'Faltan datos'}), 400

    carpeta = os.path.join(BASE_DIR, f'data/productos/{codigo}')
    os.makedirs(carpeta, exist_ok=True)

    try:
        img_data = base64.b64decode(imagen_base64.split(',')[1])
        np_img = np.frombuffer(img_data, np.uint8)
        imagen = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        path = os.path.join(carpeta, 'producto.jpg')
        cv2.imwrite(path, imagen)

        return jsonify({'mensaje': 'Producto registrado correctamente.'}), 200
    except Exception as e:
        print("❌ Error procesando imagen de producto:", e)
        return jsonify({'error': 'Error procesando imagen'}), 500


@app.route('/verificar_miembro', methods=['POST'])
def verificar_miembro():
    data = request.json
    imagen_base64 = data.get('imagen')

    if not imagen_base64:
        return jsonify({'error': 'No se recibió imagen'}), 400

    try:
        img_data = base64.b64decode(imagen_base64.split(',')[1])
        np_img = np.frombuffer(img_data, np.uint8)
        imagen = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        ubicaciones = face_recognition.face_locations(rgb)
        if not ubicaciones:
            return jsonify({'existe': False, 'mensaje': 'No se detectó rostro'})

        encoding_actual = face_recognition.face_encodings(rgb, ubicaciones)[0]
        base_miembros = os.path.join(BASE_DIR, "data", "miembros")

        for nombre in os.listdir(base_miembros):
            carpeta = os.path.join(base_miembros, nombre)
            if not os.path.isdir(carpeta):
                continue

            for archivo in os.listdir(carpeta):
                if archivo.endswith(".jpg") or archivo.endswith(".png"):
                    img_path = os.path.join(carpeta, archivo)
                    img_known = face_recognition.load_image_file(img_path)
                    encodings_known = face_recognition.face_encodings(img_known)

                    if encodings_known:
                        match = face_recognition.compare_faces([encodings_known[0]], encoding_actual, tolerance=0.5)
                        if match[0]:
                            return jsonify({'existe': True, 'nombre': nombre})

        return jsonify({'existe': False, 'mensaje': 'No se encontró coincidencia'})
    except Exception as e:
        print("Error verificando rostro:", e)
        return jsonify({'error': 'Error al procesar verificación'}), 500


@app.route('/buscar_miembro/<nombre>', methods=['GET'])
def buscar_miembro(nombre):
    carpeta = os.path.join(BASE_DIR, f'data/miembros/{nombre}')
    if not os.path.exists(carpeta):
        return jsonify({'existe': False})

    archivos = os.listdir(carpeta)
    if not archivos:
        return jsonify({'existe': False})

    archivos.sort()
    imagen = archivos[-1]
    ruta = f'/static/miembros/{nombre}/{imagen}'
    return jsonify({'existe': True, 'imagen': ruta})


@app.route('/buscar_producto/<codigo>', methods=['GET'])
def buscar_producto(codigo):
    carpeta = os.path.join(BASE_DIR, f'data/productos/{codigo}')
    if not os.path.exists(carpeta):
        return jsonify({'existe': False})

    archivos = os.listdir(carpeta)
    if not archivos:
        return jsonify({'existe': False})

    ruta = f'/static/productos/{codigo}/producto.jpg'
    return jsonify({'existe': True, 'imagen': ruta})


@app.route('/static/<tipo>/<id>/<filename>')
def servir_imagen(tipo, id, filename):
    carpeta = os.path.join(BASE_DIR, f'data/{tipo}/{id}')
    return send_from_directory(carpeta, filename)


if __name__ == '__main__':
    os.makedirs(os.path.join(BASE_DIR, 'data/miembros'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'data/productos'), exist_ok=True)
    print("Servidor corriendo con verificación facial (sin .npy).")
    app.run(debug=True)
