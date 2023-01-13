document.addEventListener('DOMContentLoaded', function(){
    let language_counter = 0
    let counter_map = 0
    document.getElementById('mapButton').onclick = function(){
        counter_map = counter_map + 1;
        if(counter_map % 2 == 0){
            document.getElementById('map').style.display = 'none';
            document.getElementById('fill').style.display = 'none';
            document.getElementById('mapButton').innerHTML = 'map';
        } else{
            document.getElementById('map').style.display = 'block';
            document.getElementById('fill').style.display = 'block';
            document.getElementById('mapButton').innerHTML = 'close';
        } 
    }
})






