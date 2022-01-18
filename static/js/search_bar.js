const productos = [
    {nombre: "Platanos"},
    {nombre: "Manzana"},
    {nombre: "Naranja"},
    {nombre: "Manzana"},
    {nombre: "Arandanos"},
    {nombre: "Palta"}
]


const formulario = document.querySelector('#formulario');
const boton = document.querySelector('#boton');
const resultado = document.querySelector('#resultado')



const filtrar = () => {
    resultado.innerHTML = '' ;
    //console.log(formulario.value);
    const texto = formulario.value.toLowerCase();

    for(let producto of productos){
        let nombre = producto.nombre.toLowerCase()
        if(nombre.indexOf(texto) !==-1){
            resultado.innerHTML += 
            ` <li>${producto.nombre} </li> ` 
        }
    }

    if(resultado.innerHTML === ''){
        resultado.innerHTML +=
        ` <li> Producto no encontrado.. </li> ` 
    }
}

boton.addEventListener('click',filtrar)
formulario.addEventListener('keyup',filtrar)

filtrar()