import cv2
import os

def registrar_producto(nombre_producto):
    ruta = f"data/productos/{nombre_producto}"
    os.makedirs(ruta, exist_ok=True)

    cam = cv2.VideoCapture(0)
    print("📦 Capturando imagen del producto. Presiona 'q' para guardar...")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        cv2.imshow("Captura de Producto", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            nombre_archivo = f"{ruta}/producto.jpg"
            cv2.imwrite(nombre_archivo, frame)
            print(f"🟢 Imagen del producto '{nombre_producto}' guardada en {nombre_archivo}")
            break

    cam.release()
    cv2.destroyAllWindows()
