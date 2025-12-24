// Se identifica el formulario de registro por su ID
const formulario = document.getElementById("form-register");

// Evento para manejar el envío del formulario
formulario.addEventListener("submit", function(event) {
    event.preventDefault();
    
    const nombre = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    let pwd = document.getElementById("password").value;
    let pwdConfirm = document.getElementById("password2").value;

    if (pwd !== pwdConfirm) { // Verificación de que las contraseñas coincidan
        alert("Las contraseñas no coinciden.");
        document.getElementById("password").value = "";
        document.getElementById("password2").value = "";
        pwd = "";
        pwdConfirm = "";
        return;
    }

    // Se imprime las variables en la consola para verificar su captura
    console.log("Nombre:", nombre);
    console.log("Email:", email);
    console.log("Contraseña:", pwd);
    console.log("Confirmar Contraseña:", pwdConfirm);
});

// Se almacenará en una base de datos en el futuro