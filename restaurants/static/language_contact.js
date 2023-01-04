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
    document.querySelector('.heading').innerHTML = 'contact'
    document.querySelector('#navbar-item-contact-home').innerHTML = 'home'
    document.querySelector('.text1').innerHTML = 'We are a free online service based in Austria. With our service we do not seek any financial gain. As we aim for a more vegan oriented future for countries all over the world, we try to help fully vegan restaurants to attract more attention and as a result more customers. While we do our best, we cannot guarantee that every information on our website is true or current. If you have any questions, please contact us and we will respond as soon as possible.'
    document.querySelector('.text2').innerHTML = 'If you want to add your restaurant to our database and furthermore list it on our website, take a look at'
    document.querySelector('.text3').innerHTML = 'If you notice that certain data (addresses, ...) are no longer up to date or even incorrect, or restaurants listed on this website also offer non-vegan food, we ask you to report this to us immediately.'
    const link = document.getElementById('link_add');
    link.textContent = 'add my Restaurant';
}

function german(){
    document.getElementById('header-item-div').style.backgroundImage = 'url("/static/pics/english.png")'
    document.querySelector('.heading').innerHTML = 'Kontakt'
    document.querySelector('#navbar-item-contact-home').innerHTML = 'zurück'
    document.querySelector('.text1').innerHTML = 'Wir sind ein kostenloser Online-Dienst mit Sitz in Österreich. Mit unserem Service verfolgen wir keine finanziellen sowie gewerblichen Ziele und Vorteile. Da wir eine stärker vegan-orientierte Zukunft für Länder auf der ganzen Welt anstreben, versuchen wir rein veganen Restaurants zu helfen, indem wir mehr Aufmerksamkeit für diese erregen und diese in Folge mehr Kunden gewinnen können. Obwohl wir unser Bestes geben können wir nicht garantieren, dass alle Informationen auf unserer Website wahr oder aktuell sind. Wenn Sie Fragen haben, kontaktieren Sie uns bitte und wir werden Ihnen so schnell wie möglich antworten.'
    document.querySelector('.text2').innerHTML = 'Falls Sie in Besitz eines Restaurants sind und interessiert sind es in unsere Datenbank aufzunehmen, sollten Sie bei bei folgendem Link vorbeischauen.'
    document.querySelector('.text3').innerHTML = 'Sollten Sie feststellen, dass bestimmte Daten (Adressen, ...) nicht mehr aktuell oder gar falsch sind, oder dass auf dieser Website gelistete Restaurants auch nicht-vegane Speisen anbieten, bitten wir Sie, uns dies umgehend zu melden.'
    const link = document.getElementById('link_add');
    link.textContent = 'mein Restaurant';
}