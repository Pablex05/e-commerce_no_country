var cuerpoweb = document.body;
var modocolor = localStorage.getItem("modo");
var btnpresionado = false;

function cargarModo() {
    if (modocolor === "oscuro") {
        cuerpoweb.classList.add("oscuro");
    } else {
        cuerpoweb.classList.add("claro");
    }
}
function cambiarModo() {
    if (btnpresionado) { // Si No es presionado el botón
        cuerpoweb.classList.remove("oscuro");
        localStorage.setItem("modo", "claro");
        cuerpoweb.classList.add("claro");
        btnpresionado = false;
    } else { // Si es presionado el botón
        if (modocolor === "oscuro") {
            resetear();
            btnpresionado = true;
        } else {
            cuerpoweb.classList.remove("claro");
            localStorage.setItem("modo", "oscuro");
            cuerpoweb.classList.add("oscuro");
            btnpresionado = true;

        }
    }
}
function resetear() {
    localStorage.removeItem('modo');
    location.reload();
}
