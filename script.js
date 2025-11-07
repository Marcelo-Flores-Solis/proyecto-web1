// Se identifica el formulario de registro por su ID
const formulario = document.getElementById("form-register");

// Evento para manejar el envío del formulario
formulario.addEventListener("submit", function(event) {
    event.preventDefault();
    
    const nombre = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const pwd = document.getElementById("password").value;
    const pwdConfirm = document.getElementById("password2").value;

    // Se imprime las variables en la consola para verificar su captura
    console.log("Nombre:", nombre);
    console.log("Email:", email);
    console.log("Contraseña:", pwd);
    console.log("Confirmar Contraseña:", pwdConfirm);
});

// Se almacenará en una base de datos en el futuro