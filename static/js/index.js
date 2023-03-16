function Vanish(){
    document.getElementById("message").style.cssText = 'opacity: 0; transition: 0.3s';
}


function SelectCity() {
    document.getElementById("city__search--container").style.cssText = 'opacity:1;'

}

$(document).ready ( function(){
        fetch('http://ip-api.com/json/?lang=ru')
            .then(function(response) {
                return response.json();
            })
            .then(function(jsonResponse) {
                document.getElementById('city').textContent=jsonResponse.city
                document.getElementById('region').value=jsonResponse.city
            });
   });