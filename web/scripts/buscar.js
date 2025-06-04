function buscarMiembro() {
  const nombre = document.getElementById("nombreBusqueda").value.trim();
  if (!nombre) {
    alert("Escribe un nombre válido.");
    return;
  }

  fetch(`http://127.0.0.1:5000/buscar_miembro/${nombre}`)
    .then(res => res.json())
    .then(data => {
      const div = document.getElementById("resultadoMiembro");
      console.log("Respuesta del servidor:", data);

      if (data.existe) {
        const imagenURL = `http://127.0.0.1:5000${data.imagen}`;
        console.log("Imagen URL:", imagenURL);

        div.innerHTML = `
          <img src="${imagenURL}"
               alt="Rostro de ${nombre}"
               style="max-width: 100%; border-radius: 12px; margin-top: 10px;" />
        `;
      } else {
        div.innerHTML = "<p>❌ Miembro no encontrado.</p>";
      }
    })
    .catch(err => {
      console.error("❌ Error buscando miembro:", err);
      alert("Error al buscar miembro.");
    });
}

function buscarProducto() {
  const codigo = document.getElementById("codigoBusqueda").value.trim();
  if (!codigo) {
    alert("Escribe un código válido.");
    return;
  }

  fetch(`http://127.0.0.1:5000/buscar_producto/${codigo}`)
    .then(res => res.json())
    .then(data => {
      const div = document.getElementById("resultadoProducto");
      console.log("📦 Respuesta del servidor:", data);

      if (data.existe) {
        const imagenURL = `http://127.0.0.1:5000${data.imagen}`;
        console.log("📷 Imagen producto URL:", imagenURL);

        div.innerHTML = `
          <img src="${imagenURL}"
               alt="Producto ${codigo}"
               style="max-width: 100%; border-radius: 12px; margin-top: 10px;" />
        `;
      } else {
        div.innerHTML = "<p>Producto no encontrado.</p>";
      }
    })
    .catch(err => {
      console.error("Error buscando producto:", err);
      alert("Error al buscar producto.");
    });
}
