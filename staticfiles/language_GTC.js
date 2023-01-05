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
    document.querySelector('.heading').innerHTML = 'General Terms and Conditions (GTC)'
    document.querySelector('.li-1').innerHTML = 'We do not aim for any financial benefits.'
    document.querySelector('.li-2').innerHTML = 'By agreeing these terms you agree that we put the address of your restaurant on our website.'
    document.querySelector('.li-3').innerHTML = 'It will result in an immediate as well as irreversible exclusion from our online service if your restaurant offers non-vegan dishes, as this is of fundamental importance to us. Every dish you offer, prepare and sell must be 100% vegan without exception.'
    document.querySelector('.li-4').innerHTML = 'We maintain the right to delete your restaurant as well as your data from our database in situations we think it is approriate.'
    document.querySelector('.li-5').innerHTML = 'As you are providing information and specific details about the particular business you take responsibility for its truth.'
    document.querySelector('.li-6').innerHTML = 'By agreeing these terms you confirm that the restaurant belongs to you or you officially act with permission in the name of the particular business. As the purpose of this website, we need the exact location of your restaurant as well as some additional information for being able to confirm whether you are the real owner of this business or not. If you are trying to register a non existing restaurant or a restaurant without its permission you may face legal actions as we do not take responsibility for any illegal activities done by our users. Arbitrarily registering restaurants from which you do not explicitly have the permission to share its data is not allowed and will face consequences.'
    document.querySelector('.li-7').innerHTML = 'You are able to delete your data and your restaurant from our database anytime you want. Therefore send us an email with the specific request and we will make sure your wish will be fulfilled.'
}

function german(){
    document.getElementById('header-item-div').style.backgroundImage = 'url("/static/pics/english.png")'
    document.querySelector('.heading').innerHTML = 'Allgemeine Geschäftsbedingungen (AGB)'
    document.querySelector('.li-1').innerHTML = 'Wir verfolgen keine gewerblichen sowie finanziellen Ziele.'
    document.querySelector('.li-2').innerHTML = 'Mit der Zustimmung zu diesen Bedingungen erklären Sie sich damit einverstanden, dass wir die Adresse Ihres Restaurants auf unserer Website veröffentlichen.'
    document.querySelector('.li-3').innerHTML = 'Wenn Ihr Restaurant auch nicht-vegane Gerichte anbietet, führt dies zu einem sofortigen und unwiderruflichen Ausschluss von unserem Online-Dienst, da dies für uns von grundlegender Bedeutung ist. Jedes Gericht, das Sie anbieten, zubereiten und verkaufen, muss ausnahmslos 100% vegan sein.'
    document.querySelector('.li-4').innerHTML = 'Wir behalten uns das Recht vor, sowohl Ihr Restaurant als auch Ihre Daten aus unserer Datenbank zu löschen, wenn wir dies für angemessen halten.'
    document.querySelector('.li-5').innerHTML = 'Da Sie Informationen und spezifische Details über das jeweilige Unternehmen bereitstellen, übernehmen Sie die Verantwortung für deren Richtigkeit.'
    document.querySelector('.li-6').innerHTML = 'Mit der Zustimmung zu diesen Bedingungen bestätigen Sie, dass das Restaurant Ihnen gehört oder Sie offiziell mit Genehmigung im Namen des jeweiligen Unternehmens handeln. Für den Zweck dieser Website benötigen wir den genauen Standort Ihres Restaurants sowie einige zusätzliche Informationen, um bestätigen zu können, ob Sie der tatsächliche Eigentümer dieses Unternehmens sind oder nicht. Wenn Sie versuchen, ein nicht existierendes Restaurant oder ein Restaurant ohne dessen Erlaubnis anzumelden, können Sie mit rechtlichen Schritten rechnen, da wir keine Verantwortung für illegale Aktivitäten unserer Nutzer übernehmen. Die willkürliche Registrierung von Restaurants, von denen Sie nicht ausdrücklich die Erlaubnis haben, ihre Daten zu teilen, ist nicht erlaubt und wird Konsequenzen nach sich ziehen.'
    document.querySelector('.li-7').innerHTML = 'Sie haben jederzeit die Möglichkeit, Ihre Daten und Ihr Restaurant aus unserer Datenbank zu löschen. Schicken Sie uns dazu eine E-Mail mit Ihrer konkreten Anfrage und wir werden dafür sorgen, dass Ihr Wunsch erfüllt wird.'
}