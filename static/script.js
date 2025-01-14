function procesarPlacas() {
    const placas = document.getElementById('placas').value.trim();
    const loader = document.getElementById("loader");
    const resultado = document.getElementById("resultado");

    if (placas === '') {
        alert('Por favor, ingrese las placas.');
        return;
    }
      // Mostrar el círculo de carga
  console.log("Mostrando loader...");
  loader.style.display = "block";
  console.log("Loader mostrado.");
  resultado.innerHTML = "";
    
    fetch('/procesar_placas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ placas: placas })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error en la respuesta del servidor: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        loader.style.display = "none"; // Ocultar el círculo de carga

        const resultadoDiv = document.getElementById('resultado');

        if (data.error) {
            resultadoDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
        } else {
            const resultados = data.resultados;

            if (resultados.length === 0) {
                resultadoDiv.innerHTML = '<p>No se encontraron bonificaciones para las placas ingresadas.</p>';
            } else {
                const listaResultados = resultados
                .map(res => {
                     // Resaltar dinámicamente los números de página
                    return `<li>${res.replace(/página (\d+)/g, "<span class='resaltado'>página $1</span>")}</li>`;
                })
                .join('');
                resultadoDiv.innerHTML = `<ul>${listaResultados}</ul>`;
            }
        }
    })
    .catch(error => {
        loader.style.display = "none";// Asegurarse de ocultar el indicador de carga en caso de error
        console.error('Error:', error);
        alert('Hubo un problema al procesar las placas. Por favor, intente nuevamente.');
        resultadoDiv.innerHTML = '';
    });
}
