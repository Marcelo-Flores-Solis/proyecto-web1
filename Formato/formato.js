class MiHeader extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <header>
                <div class="cabecera">
                    <div class="logo"><h1>ZEBRALibra</h1></div>
                    <nav>
                        <ul>
                            <li><a href="index.html">Inicio</a></li>
                            <li><a href="Account/login.html">Iniciar Sesión</a></li>
                            <li><a href="public_html/user.html">Perfil</a></li>
                            <li><a href="public_html/element.html">LibroExpandido</a></li>
                        </ul>
                    </nav>
                </div> <br>
            </header>
        `;
    }
}
customElements.define('header-custom', MiHeader);
class MiFooter extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <footer>
                © 2025 ZEBRALibra — Biblioteca Virtual creada con pasión por la lectura.
            </footer>
        `;
    }
}
customElements.define('footer-custom', MiFooter);