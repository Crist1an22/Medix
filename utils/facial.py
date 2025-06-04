import cv2
import os

def registrar_miembro(nombre):
    ruta = f"data/miembros/{nombre}"
    os.makedirs(ruta, exist_ok=True)

    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    contador = 0

    print("📸 Capturando rostro. Presiona 'q' para salir...")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostros = face_cascade.detectMultiScale(gris, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in rostros:
            rostro = frame[y:y+h, x:x+w]
            contador += 1
            nombre_archivo = f"{ruta}/rostro_{contador}.jpg"
            cv2.imwrite(nombre_archivo, rostro)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Detección de Rostro", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or contador >= 5:
            break

    cam.release()
    cv2.destroyAllWindows()
    print(f"🟢 Rostros capturados: {contador} en {ruta}")
