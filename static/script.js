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
    resultado.innerHTML = ""; 
    
    fetch('/procesar_placas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
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

        if (data.error) {
            // 🔹 Corregido: Mostrar el mensaje de error del servidor
            resultado.textContent = data.error;
            resultado.style.color = "red";
        } else {
            const resultados = data.resultados;

            if (resultados.length === 0) {
                resultado.textContent = 'No se encontraron bonificaciones para las placas ingresadas.';
            } else {
                // Crear una lista segura sin manipular directamente `innerHTML`
                const lista = document.createElement("ul");
                resultados.forEach(res => {
                    const li = document.createElement("li");
                    
                    // Resaltamos la palabra "página" de manera segura
                    const contenidoSeguro = res.replace(/página (\d+)/g, "<span class='resaltado'>página $1</span>");
                    li.innerHTML = DOMPurify.sanitize(contenidoSeguro); // Sanitizar la entrada antes de insertar en HTML
                    lista.appendChild(li);
                });

                resultado.innerHTML = ""; // Limpiar antes de insertar
                resultado.appendChild(lista);
            }
        }
    })
    .catch(error => {
        loader.style.display = "none"; // Asegurarse de ocultar el indicador de carga en caso de error
        console.error('Error:', error);
        alert('Hubo un problema al procesar las placas. Por favor, intente nuevamente.');
        resultado.textContent = 'Error en la solicitud. Intente más tarde.'; // 🔹 Mensaje más claro
        resultado.style.color = "red";
    });
}
