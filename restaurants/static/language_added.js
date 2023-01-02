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
    document.querySelector('.text2').innerHTML = 'However, before we will show your restaurant to our users, we need to make sure that you only offer vegan meals.'
    document.querySelector('.important').innerHTML = 'Therefore, as a last step, please send photos of your current menu to our email address contact@wherevegan.de with your registered email address. Please do not forget to include the name of your restaurant and the address, otherwise we will not know to which restaurant the respective menu belongs.'
    document.querySelector('.text4').innerHTML = 'You will receive an email from us as soon as we have checked your restaurant and menu and approved them for our website.'
}

function german(){
    document.getElementById('header-item-div').style.backgroundImage = 'url("/static/pics/english.png")'
    document.querySelector('.text2').innerHTML = 'Jedoch bevor wir Ihr Restaurant endgültig unseren Nutzern anzeigen können, müssen wir sicherstellen, dass Sie nur vegane Gerichte zubereiten.'
    document.querySelector('.important').innerHTML = 'Schicken Sie daher bitte als letzten Schritt Fotos Ihrer aktuellen Speisekarte an unsere E-Mail-Adresse contact@wherevegan.de, mit Ihrer bereits registrierten E-Mail-Adresse. Bitte vergessen Sie nicht den Namen sowie die Adresse Ihres Restaurants anzugeben, da wir sonst Ihre Speisekarte nicht Ihrem Restaurant zuordnen könnten.'
    document.querySelector('.text4').innerHTML = 'Sie erhalten eine Benachrichtigung via email von uns, sobald wir ihr Restaurant sowie ihre Speisekarte überprüft und für unsere Website freigeschalten haben.'
}
