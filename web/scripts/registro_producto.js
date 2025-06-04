let html5QrCode;
let codigoDetectado = null;

function iniciarEscaneo() {
  const qrRegion = document.getElementById("lectorQR");
  qrRegion.innerHTML = "";

  html5QrCode = new Html5Qrcode("lectorQR");
  Html5Qrcode.getCameras().then(cameras => {
    if (cameras && cameras.length) {
      html5QrCode.start(
        cameras[0].id,
        {
          fps: 10,
          qrbox: { width: 250, height: 250 }
        },
        qrCodeMessage => {
          if (!codigoDetectado) {
            codigoDetectado = qrCodeMessage;
            html5QrCode.stop().then(() => {
              qrRegion.innerHTML = "<p>Código detectado: " + codigoDetectado + "</p>";
              capturarProducto();
            });
          }
        },
        errorMessage => {
        }
      );
    }
  }).catch(err => {
    alert("No se pudo acceder a la cámara: " + err);
  });
}

function capturarProducto() {
  const video = document.getElementById("videoProducto");
  video.style.display = "block";

  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;

      setTimeout(() => {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0);

        const imagenBase64 = canvas.toDataURL("image/jpeg");

        video.srcObject.getTracks().forEach(track => track.stop());

        const nombre = document.getElementById("nombreProducto").value.trim();
        if (!nombre || !codigoDetectado) {
          alert("Debes escribir el nombre del producto y escanear un código.");
          return;
        }

        fetch("http://localhost:5000/registrar_producto", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            codigo: codigoDetectado,
            nombre: nombre,
            imagen: imagenBase64
          })
        })
        .then(response => response.json())
        .then(data => {
          alert(data.mensaje || "Producto registrado.");
          codigoDetectado = null;
          video.style.display = "none";
        })
        .catch(error => {
          console.error("Error:", error);
          alert("Error al registrar producto.");
        });
      }, 2000);
    })
    .catch(err => {
      alert("No se pudo acceder a la cámara: " + err);
    });
}
