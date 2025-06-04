let video = null;
let stream = null;
let qrInterval = null;

function mostrarFormulario(tipo) {
  document.getElementById("form-miembro").style.display = "none";
  document.getElementById("form-producto").style.display = "none";

  if (tipo === "miembro") {
    document.getElementById("form-miembro").style.display = "block";
  } else if (tipo === "producto") {
    document.getElementById("form-producto").style.display = "block";
  }
}

function iniciarCamara() {
  document.getElementById("videoContainer").style.display = "block";
  video = document.getElementById("video");

  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(mediaStream) {
      stream = mediaStream;
      video.srcObject = stream;

      if (document.getElementById("codigoProducto")) {
        iniciarLectorQR();
      }
    })
    .catch(function(err) {
      alert("Error al acceder a la cámara: " + err);
    });
}

function cerrarCamara() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
  if (qrInterval) {
    clearInterval(qrInterval);
    qrInterval = null;
  }
  document.getElementById("videoContainer").style.display = "none";
}

function capturarImagenBase64() {
  const canvas = document.getElementById("canvas");
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL("image/jpeg");
}

// Capturar rostro y enviar para registro de miembro
function capturarYEnviarMiembro() {
  const nombre = document.getElementById("nombreMiembro").value.trim();
  if (!nombre) {
    alert("Por favor escribe un nombre válido.");
    return;
  }

  const imagenBase64 = capturarImagenBase64();

  fetch('http://127.0.0.1:5000/registrar_miembro', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      nombre: nombre,
      imagen: imagenBase64
    })
  })
    .then(res => res.json())
    .then(data => alert(data.mensaje || "Rostro guardado."))
    .catch(err => alert("Error al guardar el rostro: " + err));
}

// Capturar imagen y registrar producto
function capturarYEnviarProducto() {
  const codigo = document.getElementById("codigoProducto").value.trim();
  if (!codigo) {
    alert("Por favor ingresa un código de producto válido.");
    return;
  }

  const imagenBase64 = capturarImagenBase64();

  fetch('http://127.0.0.1:5000/registrar_producto', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      codigo: codigo,
      imagen: imagenBase64
    })
  })
    .then(res => res.json())
    .then(data => alert(data.mensaje || "Producto registrado."))
    .catch(err => alert("Error al guardar producto: " + err));
}

// Iniciar lector QR/barra para productos
function iniciarLectorQR() {
  const canvas = document.getElementById("canvas");
  const context = canvas.getContext("2d");

  qrInterval = setInterval(() => {
    if (!video || video.readyState !== 4) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(imageData.data, imageData.width, imageData.height);

    if (code) {
      document.getElementById("codigoProducto").value = code.data;
      clearInterval(qrInterval);
      qrInterval = null;
      alert("Código detectado automáticamente.");
    }
  }, 500);
}
