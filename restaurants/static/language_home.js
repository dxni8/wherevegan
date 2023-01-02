document.addEventListener('DOMContentLoaded', function(){
    let language_counter = 0
    let counter_map = 0
    document.getElementById('header-item-div').onclick = function(){
        language_counter += 1
        if(language_counter % 2 == 0){
            // english
            english()
        } else {
            // german
            german()
        }
    }
    document.getElementById('mapButton').onclick = function(){
        counter_map = counter_map + 1;
        if(counter_map % 2 == 0){
            document.getElementById('map').style.display = 'none';
            document.getElementById('fill').style.display = 'none';
            if(language_counter % 2 == 0){
                document.getElementById('mapButton').innerHTML = 'map';
            } else{
                document.getElementById('mapButton').innerHTML = 'Karte';
            }
        } else{
            document.getElementById('map').style.display = 'block';
            document.getElementById('fill').style.display = 'block';
            document.getElementById('mapButton').innerHTML = 'close';
        } 
    }
})


function english(){
    document.getElementById('header-item-div').style.backgroundImage = 'url("/static/pics/german.png")'
    document.querySelector('.heading').innerHTML = ' Find vegan<br/>restaurants in <br/>your area'
    document.querySelector('.navbar-item-contact').innerHTML = 'contact'
    document.querySelector('#navbar-item-last').innerHTML = 'recipes'
    document.querySelector('#mybutton').value = 'search'

    if(document.getElementById('mapButton').innerHTML == 'Karte'){
        document.getElementById('mapButton').innerHTML = 'map'
    }

}
function german(){
    document.getElementById('header-item-div').style.backgroundImage = 'url("/static/pics/english.png")'
    document.querySelector('.heading').innerHTML = 'Finde vegane<br/>Restaurants in <br/>deiner Nähe'

    document.querySelector('.navbar-item-contact').innerHTML = 'Kontakt'
    document.querySelector('#navbar-item-last').innerHTML = 'Rezepte'
    document.querySelector('#mybutton').value = 'suchen'  
    if(document.getElementById('mapButton').innerHTML == 'map'){
        document.getElementById('mapButton').innerHTML = 'Karte'
    }
} 




