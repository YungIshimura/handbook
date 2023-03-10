function Vanish(){
    document.getElementById("message").style.cssText = 'opacity: 0; transition: 0.3s';
}


function changeRegion() {
    document.getElementById('city').innerHTML = 'Тула'
    document.getElementById('region').value = 'Тула'
}