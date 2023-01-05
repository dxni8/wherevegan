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
    document.querySelector('.text').innerHTML = 'We have sent you a confirmation email.'
    document.querySelector('#text-bottom').innerHTML = 'Please check your spam folder as well!'
    document.getElementById('header-link1').innerHTML = 'home'
}

function german(){
    document.getElementById('header-item-div').style.backgroundImage = 'url("/static/pics/english.png")'
    document.querySelector('.text').innerHTML = 'Wir haben Ihnen eine Bestätigungsemail gesendet.'
    document.querySelector('#text-bottom').innerHTML = 'Bitte schauen Sie auch in Ihrem Spamordner nach'
    document.getElementById('header-link1').innerHTML = 'zurück'
}