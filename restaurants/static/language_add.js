document.addEventListener('DOMContentLoaded', function(){
    window.onscroll = function(){
        if(window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            document.querySelector('body').style.backgroundColor = '#344648'
        } else{
            document.querySelector('body').style.backgroundColor = '#657779'
        }
    }

    var checkboxes = $("input[type='checkbox']"),
    submitButt = $("input[type='submit']");

    checkboxes.click(function() {
    submitButt.attr("disabled", !checkboxes.is(":checked"));
    });
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
    
    document.querySelector('.heading').innerHTML = 'Add Your Restaurant'
    document.querySelector('#Name').placeholder = 'restaurant name'
    document.querySelector('#address').placeholder = 'address'
    document.querySelector('.text').innerHTML = 'I hereby agree that I am acting with the official permission of the restaurant in question and that I have read our GTCs' 
    const link = document.getElementById('privacy_link1');
    link.textContent = 'General terms and conditions';
    const link2 = document.getElementById('header-link1')
    link2.textContent = 'home'
}

function german(){
    document.getElementById('header-item-div').style.backgroundImage = 'url("/static/pics/english.png")'

    document.querySelector('.heading').innerHTML = 'Dein Restaurant Hinzufügen'
    document.querySelector('#Name').placeholder = 'Name des Restaurants'
    document.querySelector('#address').placeholder = 'Adresse'
    document.querySelector('.text').innerHTML = 'Hiermit stimme ich zu, dass ich mit offizieller Genehmigung des jeweiligen Restaurants handle und dass ich unsere AGB gelesen habe'
    const link = document.getElementById('privacy_link1');
    link.textContent = 'Allgemeine Geschätsbedingungen';
    const link2 = document.getElementById('header-link1');
    link2.textContent = 'zurück';
}