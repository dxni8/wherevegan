document.addEventListener('DOMContentLoaded', function(){
    window.onscroll = function(){
        if(window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            if(window.innerWidth < 900){
                document.querySelector('body').style.backgroundColor = '#344648'
            }
        } else{
            if(window.innerWidth < 900){
                document.querySelector('body').style.backgroundColor = '#657779'
            }
        }
    }

    let lat_test = sessionStorage.getItem("lat_permanent");
    if (lat_test == null){
        if ("geolocation" in navigator) {
            // check if geolocation is supported/enabled on current browser
            navigator.geolocation.getCurrentPosition(
            function success(position) {
                // for when getting location is a success
                lat2 = position.coords.latitude;
                lon2 = position.coords.longitude;
                document.getElementById('hidden1').value = lat2
                document.getElementById('hidden2').value = lon2
                sessionStorage.setItem("lat_permanent", lat2);
                sessionStorage.setItem("lon_permanent", lon2);
                },
            function error(error_message) {
                // for when getting location results in an error
                console.log('An error has occured while retrieving location', error_message)
                }  
                );     
            }else {
                // geolocation is not supported
                // get your location some other way
                alert('geolocation is not enabled on this browser')
                }
    }  

let lat2 = sessionStorage.getItem("lat_permanent");
let lon2 = sessionStorage.getItem("lon_permanent");
document.getElementById('hidden1').value = lat2
document.getElementById('hidden2').value = lon2

document.getElementById('navbar-item-last').onclick = function(){
    sessionStorage.setItem("flex", 'none');
}
document.getElementById('navbar-item').onclick = function(){
    sessionStorage.setItem("flex", 'none');
}
document.getElementById('mybutton').onclick = function(){
    sessionStorage.setItem("flex", 'flex');
}

// nach dem neuladen wird der Wert von der Session "flex", abhängig on den obigen
// conditions, dem display property von content gegeben
let flex_wert = sessionStorage.getItem("flex");
document.getElementById('content').style.display = flex_wert;
if(flex_wert == 'flex'){
    var section = $('#content');
    event.preventDefault();
         $('html, body').animate({
             scrollTop: $(section).offset().top
         }, 1500);
}
$(function(){

    var trigger = $('#mapButton'); // your trigger for click event
    var section = $('#map'); // your class goes here to scroll to
 
    trigger.click(function(event){
         event.preventDefault();
         $('html, body').animate({
             scrollTop: $(section).offset().top
         }, 1500);
     });
 });
})


    