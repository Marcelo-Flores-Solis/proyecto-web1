class Cuenta {
    constructor(nombreCompleto, edad, sexo, gmail, contrasena) {
        this.nombreCompleto = nombreCompleto;
        this.edad = edad;
        this.sexo = sexo;
        this.gmail = gmail; 
        this.contrasena = contrasena; 
    }
}
const credencialesMap = new Map();

const cuenta1 = new Cuenta('Jhovi', 17, 'Masculino', 'cusijose35@gmail.com', 'clave456');
const cuenta2 = new Cuenta('Marcelo', 17, 'Masculino', 'marcelosolis10@gmail.com', 'mi_pass');
const cuenta3 = new Cuenta('Saulo', 19, 'Masculino', 'saulo12@gmail.com', 'secreta123');

credencialesMap.set(cuenta1.gmail, cuenta1.contrasena);
credencialesMap.set(cuenta2.gmail, cuenta2.contrasena);
credencialesMap.set(cuenta3.gmail, cuenta3.contrasena);


const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username'); 
const passwordInput = document.getElementById('password');ñ