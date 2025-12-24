/* assets/scripts/script.js */

document.addEventListener('DOMContentLoaded', () => {
    
    // --- ESCENARIO 1: ESTAMOS EN EL CATÁLOGO (catalogo.html) ---
    const contenedorLibros = document.getElementById('contenedor-libros');
    
    if (contenedorLibros) {
        console.log("📚 Cargando catálogo desde la Base de Datos...");
        
        // Pedimos los datos al servidor Python (que a su vez los pide a MySQL)
        fetch('/api/libros')
            .then(response => {
                if (!response.ok) throw new Error("Error en la red");
                return response.json();
            })
            .then(libros => {
                // Limpiamos el mensaje de "Cargando..."
                contenedorLibros.innerHTML = ""; 

                if (libros.length === 0) {
                    contenedorLibros.innerHTML = "<h3>No hay libros disponibles aún.</h3>";
                    return;
                }

                // Creamos una tarjeta por cada libro que llegó de la base de datos
                libros.forEach(libro => {
                    const tarjeta = document.createElement('div');
                    tarjeta.className = 'tarjeta-libro'; // Asegúrate de tener CSS para esta clase
                    
                    // OJO: Usamos libro.id para el enlace
                    tarjeta.innerHTML = `
                        <a href="/detalle?id=${libro.id}" style="text-decoration: none; color: inherit;">
                            <img src="${libro.img}" alt="${libro.titulo}" onerror="this.src='https://via.placeholder.com/150'">
                            <h4>${libro.titulo}</h4>
                            <p>${libro.autor}</p>
                            <span class="etiqueta ${libro.disponible ? 'disponible' : 'agotado'}">
                                ${libro.disponible ? 'Disponible' : 'Agotado'}
                            </span>
                        </a>
                    `;
                    contenedorLibros.appendChild(tarjeta);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                contenedorLibros.innerHTML = "<p>Hubo un error al cargar los libros. Revisa la consola (F12).</p>";
            });
    }

    // --- ESCENARIO 2: ESTAMOS EN EL DETALLE (element.html) ---
    const tituloDetalle = document.getElementById('detalle-titulo');

    if (tituloDetalle) {
        // Obtenemos el ID de la URL (ej: /detalle?id=5)
        const params = new URLSearchParams(window.location.search);
        const idLibro = params.get('id');

        if (idLibro) {
            console.log(`🔍 Buscando libro ID: ${idLibro}`);
            
            // Pedimos SÓLO ese libro a la API
            fetch(`/api/libro?id=${idLibro}`)
                .then(response => response.json())
                .then(libro => {
                    if (!libro) {
                        document.querySelector('.librodatos').innerHTML = "<h2>Libro no encontrado</h2>";
                        return;
                    }

                    // Rellenamos el HTML con los datos reales
                    document.getElementById('detalle-titulo').innerText = libro.titulo;
                    document.getElementById('detalle-autor').innerText = libro.autor;
                    // document.getElementById('detalle-categoria').innerText = libro.categoria; // Descomenta si tienes este ID en el HTML
                    document.getElementById('detalle-sinopsis').innerText = libro.sinopsis || "Sin descripción disponible.";
                    
                    const img = document.getElementById('detalle-img');
                    if(img) img.src = libro.img;
                })
                .catch(error => console.error('Error cargando libro:', error));
        }
    }
});