function Vanish(){
    document.getElementById("message").style.cssText = 'opacity: 0; transition: 0.3s';
}


function OpenSelectCityForm() {
    document.getElementById("city__search--container").style.cssText = 'opacity:1; display:block; z-index:55; box-shadow: rgba(0,0,0,.5) 0 0 0 1000px; height:200px; background-color: white;' 
    document.getElementsByName('html').style.cssText = 'bacground-color: lightgray;'

}

function CloseSelectCityForm(){
    document.getElementById('city__search--container').style.cssText = 'display:none;'
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