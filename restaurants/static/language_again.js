document.addEventListener('DOMContentLoaded', function(){

    let language_counter = 0
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
})
function english(){
    document.getElementById('header-item-div').style.backgroundImage = 'url("/static/pics/german.png")'
    document.querySelector('.text').innerHTML = 'Please enter the same email address as before!'
}

function german(){
    document.getElementById('header-item-div').style.backgroundImage = 'url("/static/pics/english.png")'
    document.querySelector('.text').innerHTML = 'Bitte geben Sie die gleiche E-Mail-Adresse wie vorher ein!'
}