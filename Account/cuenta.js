class Cuenta {
    constructor(nombreCompleto, edad, sexo, gmail, contraseña) {
        this.nombreCompleto = nombreCompleto;
        this.edad = edad;
        this.sexo = sexo;
        this.gmail = gmail; 
        this.contrasena = contraseña; 
    }
}
const credencialesMap = new Map();

const cuenta1 = new Cuenta('Jhovi', 17, 'Masculino', 'cusijose35@gmail.com', 'clave456');
const cuenta2 = new Cuenta('Marcelo', 17, 'Masculino', 'marcelo.flores@gmail.com', '28tujv10');
const cuenta3 = new Cuenta('Saulo', 19, 'Masculino', 'saulo12@gmail.com', 'secreta123');

credencialesMap.set(cuenta1.gmail, cuenta1.contraseña);
credencialesMap.set(cuenta2.gmail, cuenta2.contraseña);
credencialesMap.set(cuenta3.gmail, cuenta3.contraseña);

const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username'); 
const passwordInput = document.getElementById('password');