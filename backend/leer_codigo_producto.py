import cv2
from pyzbar import pyzbar

def capturar_codigo():
    cap = cv2.VideoCapture(0)
    codigo_detectado = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        codigos = pyzbar.decode(frame)

        for codigo in codigos:
            codigo_detectado = codigo.data.decode('utf-8')
            # Dibujar el rectángulo
            (x, y, w, h) = codigo.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, codigo_detectado, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Guardar imagen
            nombre_archivo = f'data/productos/{codigo_detectado}/producto.jpg'
            cv2.imwrite(nombre_archivo, frame)

            print(f"Código detectado: {codigo_detectado}")
            cap.release()
            cv2.destroyAllWindows()
            return codigo_detectado

        cv2.imshow("Escanea el código", frame)
        if cv2.waitKey(1) == 27:  # ESC para salir
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
