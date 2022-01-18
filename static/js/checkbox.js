const formCheck = document.getElementById("flexCheckDefault")
const shippingInfo = document.getElementById("shipping-info")


var contador=0;


function cambio(){
    if(contador==1){
        shippingInfo.style.display = 'initial';    
        contador=0;
    }
    else{shippingInfo.style.display = 'none';
            contador=1;}
}


formCheck.addEventListener('click',cambio,true)
