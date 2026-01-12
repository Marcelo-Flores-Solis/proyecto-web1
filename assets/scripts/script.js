document.addEventListener('DOMContentLoaded', () => {
	// Sesión
	const usuarioGuardado = localStorage.getItem('usuario_zebra');
	let usuario = null;

	if (usuarioGuardado) {
		try {
			usuario = JSON.parse(usuarioGuardado);
			console.log("Usuario activo:", usuario.nombre, "| Admin:", usuario.es_admin);
			
			// Menú
			const linkLogin = document.querySelector('a[href="/login"]');
			if (linkLogin) {
				// Admin
				if (usuario.es_admin == 1) {
					linkLogin.innerHTML = `Admin: ${usuario.nombre}`;
					linkLogin.style.color = "#ffd700";
					
					// Opcional
				} else {
					linkLogin.innerText = `Hola, ${usuario.nombre}`;
				}
				linkLogin.href = "/usuario";
			}
		} catch (e) {
			console.error(e);
			localStorage.removeItem('usuario_zebra');
		}
	}

	// Perfil
	const perfilNombre = document.getElementById('perfil-nombre');
	
	if (perfilNombre) {
		if (!usuario) {
			window.location.href = '/login';
		} else {
			// Datos
			document.getElementById('perfil-nombre').innerText = usuario.nombre;
			document.getElementById('perfil-email').innerText = usuario.email;

			// Préstamos
			const listaPrestamos = document.getElementById('lista-prestamos');
			
			if (listaPrestamos) {
				// Fetch
				fetch(`/api/mis_prestamos?id_usuario=${usuario.id}`)
					.then(r => r.json())
					.then(libros => {
						if (libros.length === 0) {
							listaPrestamos.innerHTML = "<p style='padding:10px; color:#666;'>No tienes libros prestados actualmente.</p>";
						} else {
							listaPrestamos.innerHTML = "";
							
							libros.forEach(libro => {
								const div = document.createElement('div');
								div.className = 'item-prestamo';
								// Estilos
								div.style = "display:flex; justify-content:space-between; align-items:center; border:1px solid #ddd; padding:10px; margin-bottom:10px; background:white; border-radius:5px;";
								
								div.innerHTML = `
									<div style="display:flex; align-items:center; gap:10px;">
										<img src="${libro.img}" style="width:40px; height:60px; object-fit:cover;">
										<div>
											<strong style="display:block;">${libro.titulo}</strong>
											<span style="font-size:0.8em; color:#555;">${libro.autor}</span>
										</div>
									</div>
									<button class="btn-devolver" data-id="${libro.id}" style="background:#d9534f; color:white; border:none; padding:5px 10px; border-radius:3px; cursor:pointer;">Devolver</button>
								`;
								listaPrestamos.appendChild(div);
							});

							// Devolver
							document.querySelectorAll('.btn-devolver').forEach(btn => {
								btn.addEventListener('click', (e) => {
									const idLibro = e.target.getAttribute('data-id');
									if(confirm("¿Quieres devolver este libro?")) {
										fetch('/api/devolver', {
											method: 'POST',
											headers: {'Content-Type': 'application/json'},
											body: JSON.stringify({ id_libro: idLibro, id_usuario: usuario.id })
										})
										.then(res => res.json())
										.then(() => {
											alert("Libro devuelto correctamente.");
											location.reload();
										});
									}
								});
							});
						}
					})
					.catch(err => console.error("Error cargando préstamos:", err));
			}
		}

		// Logout
		const btnsLogout = [document.getElementById('btn-logout-nav'), document.getElementById('btn-logout-main')];
		btnsLogout.forEach(btn => {
			if(btn) {
				btn.addEventListener('click', (e) => {
					e.preventDefault();
					if(confirm("¿Cerrar sesión?")) {
						localStorage.removeItem('usuario_zebra');
						window.location.href = '/login';
					}
				});
			}
		});
	}
	// Registro
	const formRegistro = document.getElementById('form-registro');
	if (formRegistro) {
		formRegistro.addEventListener('submit', (e) => {
			e.preventDefault();
			const nombre = document.getElementById('nombre').value;
			const email = document.getElementById('email').value;
			const password = document.getElementById('password').value;

			fetch('/api/registro', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ nombre, email, password })
			})
			.then(res => {
				if (res.ok) return res.json();
				throw new Error('Error en registro.');
			})
			.then(() => {
				alert('¡Cuenta creada! Inicia sesión.');
				window.location.href = '/login';
			})
			.catch(err => alert(err.message));
		});
	}

	// Login
	const formLogin = document.getElementById('form-login');
	if (formLogin) {
		formLogin.addEventListener('submit', (e) => {
			e.preventDefault();
			const email = document.getElementById('email').value;
			const password = document.getElementById('password').value;

			fetch('/api/login', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password })
			})
			.then(res => {
				if (res.ok) return res.json();
				throw new Error('Credenciales incorrectas');
			})
			.then(dataUsuario => {
				localStorage.setItem('usuario_zebra', JSON.stringify(dataUsuario));
				window.location.href = '/catalogo';
			})
			.catch(err => alert(err.message));
		});
	}

	// Catálogo
	// ==========================================
    
    // --- LÓGICA DE ADMIN: MOSTRAR PANEL ---
    const panelAdmin = document.getElementById('panel-admin');
    const formAgregarLibro = document.getElementById('form-agregar-libro');

    // Solo mostramos el panel si hay usuario Y es admin (1)
    if (panelAdmin && usuario && usuario.es_admin == 1) {
		// Admin
		panelAdmin.style.display = 'block';
		
		// Enviar libro
		formAgregarLibro.addEventListener('submit', (e) => {
			e.preventDefault();
			const titulo = document.getElementById('nuevo-titulo').value;
			const autor = document.getElementById('nuevo-autor').value;
			const categoria = document.getElementById('nuevo-categoria').value; // <--- NUEVO
			const img = document.getElementById('nuevo-img').value;
			const sinopsis = document.getElementById('nuevo-sinopsis').value; // Con 'n'

			fetch('/api/admin/agregar_libro', {
				method: 'POST',
				headers: {'Content-Type': 'application/json'},
				body: JSON.stringify({ titulo, autor, categoria, img, sinopsis })
			}).then(res => {
				if(res.ok) {
					alert("Libro agregado correctamente");
					location.reload();
				} else {
					alert("Error al guardar (Revisa consola del servidor)");
				}
			});
		});
	}

	// Mostrar libros
	const contenedorLibros = document.getElementById('contenedor-libros');
    const inputBuscador = document.getElementById('buscador');
    let librosMemoria = []; 

    const mostrarLibros = (libros) => {
        contenedorLibros.innerHTML = ""; 
        if (libros.length === 0) {
            contenedorLibros.innerHTML = "<h3 style='text-align:center; width:100%; color:#666;'>Sin resultados.</h3>";
            return;
        }
        libros.forEach(libro => {
            const disponible = (libro.disponible == 1);
            const tarjeta = document.createElement('div');
            tarjeta.className = 'tarjeta-libro';
            tarjeta.innerHTML = `
                <a href="/detalle?id=${libro.id}" style="text-decoration: none; color: inherit;">
                    <img src="${libro.img}" onerror="this.src='https://via.placeholder.com/150'">
                    <h4>${libro.titulo}</h4>
                    <p>${libro.autor}</p>
                    <span class="etiqueta ${disponible ? 'disponible' : 'agotado'}" 
                          style="display:inline-block; padding:3px 8px; border-radius:4px; background:${disponible ? '#d4edda' : '#f8d7da'}; color:${disponible ? '#155724' : '#721c24'}; font-size:0.8em;">
                        ${disponible ? 'Disponible' : 'Prestado'}
                    </span>
                </a>
            `;
            contenedorLibros.appendChild(tarjeta);
        });
    };

    if (contenedorLibros) { 
        fetch('/api/libros')
            .then(r => r.json())
            .then(data => { librosMemoria = data; mostrarLibros(data); });

        if (inputBuscador) {
            inputBuscador.addEventListener('input', (e) => {
                const txt = e.target.value.toLowerCase();
                mostrarLibros(librosMemoria.filter(l => l.titulo.toLowerCase().includes(txt) || l.autor.toLowerCase().includes(txt)));
            });
        }
    }

    // Detalle
    const tituloDetalle = document.getElementById('detalle-titulo');

    if (tituloDetalle) {
        const params = new URLSearchParams(window.location.search);
        const idLibro = params.get('id');

        if (idLibro) {
            fetch(`/api/libro?id=${idLibro}`)
                .then(r => r.json())
                .then(libro => {
                    document.getElementById('detalle-titulo').innerText = libro.titulo;
                    document.getElementById('detalle-autor').innerText = libro.autor;
                    document.getElementById('detalle-sinopsis').innerText = libro.sinopsis || "Sin descripción.";
                    document.getElementById('detalle-img').src = libro.img;
                    
                    const btnPrestar = document.getElementById('btn-prestar');
                    if(btnPrestar) {
                        if(libro.disponible == 0) {
                            btnPrestar.innerText = "No Disponible";
                            btnPrestar.style.backgroundColor = "#ccc";
                            btnPrestar.disabled = true;
                        } else {
                            btnPrestar.addEventListener('click', () => {
                                if(!usuario) {
                                    alert("Inicia sesión para pedir libros.");
                                    window.location.href = '/login';
                                    return;
                                }
                                if(confirm(`¿Pedir prestado "${libro.titulo}"?`)) {
                                    // AQUI ENVIAMOS EL ID DE USUARIO TAMBIÉN
                                    fetch('/api/prestar', {
                                        method: 'POST',
                                        headers: {'Content-Type': 'application/json'},
                                        body: JSON.stringify({ 
                                            id_libro: idLibro,
                                            id_usuario: usuario.id 
                                        })
                                    }).then(() => {
                                        alert("¡Libro Prestado!");
                                        window.location.href = '/usuario'; // Ir al perfil a verlo
                                    });
                                }
                            });
                        }
                    }
                });
        }
    }
});
 
// Errores
if (contenedorLibros) { 
        fetch('/api/libros')
            .then(r => {
                // VERIFICACIÓN DE ERRORES DEL SERVIDOR
                if (!r.ok) throw new Error(`Error del servidor: ${r.status}`);
                return r.json();
            })
            .then(data => { 
                librosMemoria = data; 
                mostrarLibros(data); 
            })
            .catch(err => {
                console.error(err);
                // Error UI
                contenedorLibros.innerHTML = `<div style="text-align:center; padding:20px;">
            <h3 style="color:red;">Error cargando libros</h3>
            <p>${err.message}</p>
            <small>Revisa la consola (F12) para más detalles.</small>
        </div>`;
            });

        if (inputBuscador) {
            inputBuscador.addEventListener('input', (e) => {
                const txt = e.target.value.toLowerCase();
                mostrarLibros(librosMemoria.filter(l => l.titulo.toLowerCase().includes(txt) || l.autor.toLowerCase().includes(txt)));
            });
        }
    }