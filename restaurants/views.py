from ipaddress import ip_address
from math import radians
import math
#from turtle import distance, home 
from unicodedata import decimal
from django.shortcuts import redirect, render
from urllib import response
import requests
from math import radians, cos, sin, asin, sqrt
from .models import standort_restaurant
from django.http import HttpResponse
from django.views.generic import View 
import folium #map
from geopy.geocoders import Nominatim
from email_validator import validate_email, EmailNotValidError 
import random
from django.core.exceptions import ObjectDoesNotExist
import phonenumbers
from phonenumbers import NumberParseException
from django.conf import settings


API_KEY = 'AIzaSyDU6RdLpMKVZuKX4d8IyfIW5l83TveSz4g'
lat_speicher = ''
lon_speicher = ''

# Create your views here.
def home(request):
    return render(request, 'restaurants/nearby.html')
def restaurant_add(request):
    return render(request, 'restaurants/add.html', {
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY
    })
def recipes(request):
    return render(request, 'restaurants/recipes.html')
def contact(request):
    return render(request, 'restaurants/contact.html')
def privacy(request):
    return render(request, 'restaurants/privacy.html')


def gps_berechnen(request):
    if request.method == 'POST':
        restaurant = standort_restaurant()
        restaurant.first_name = request.POST.get('first_name')
        restaurant.last_name = request.POST.get('last_name')
        restaurant.address = request.POST.get('address')
        restaurant.restaurant_name = request.POST.get('restaurant_name')
        restaurant.email = request.POST.get('email')
        vorwahl = request.POST.get('countryCode')
        phone = request.POST.get('phone_number')
        gtc_check = request.POST.get('gtc_check')
        restaurant.verified = False

        address = request.POST.get('address') #um es als extra variable zu haben
        if restaurant.address == '' or restaurant.restaurant_name == '' or restaurant.email == '' or phone == '' or restaurant.first_name == '' or restaurant.last_name == '' or vorwahl == '':
            return render(request, 'restaurants/error.html', {
                'error_message_not_enough_information': 'Unfortunately something went wrong. It looks like you forgot to fill out a field.'
            })
        #überprüfen ob die gtc akzeptiert wurden
        if gtc_check != 'true':
            return render(request, 'restaurants/error.html', {
                'error_message_gtc': 'Unfortunately something went wrong. You can only register your restaurant by accepting our general terms and conditions!'
            })
        vorwahl = str(vorwahl)
        phone = str(phone)
        phone = vorwahl + phone
        if name_check(restaurant.first_name) == False or name_check(restaurant.last_name) == False:
            return render(request, 'restaurants/error.html', {
                'error_message_name_wrong': 'Unfortunately something went wrong! Please check whether you only entered letters and not numbers for your first and last name'
            })
        if email_check(restaurant.email) == False:
            return render(request, 'restaurants/error.html', {
                'error_message_email_false': 'It looks like you entered an invalid email'
            })
        if phonenumber_validate(phone) == False:
            return render(request, 'restaurants/error.html', {
                'error_message_phone_number': 'Unfortunately something went wrong! Please check whether you entered a valid phone number!',
                'error_message_e164': 'Please use the international phone number format e164 following your country code!'
            })

        ##########
        ''' reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        print(result)
        if result['success']:
            ################
            
            params = {
            'key': API_KEY,
            'address': address
            }

            base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
            response = requests.get(base_url, params=params).json()
            response.keys()

            if response['status'] == 'OK':
                geometry = response['results'][0]['geometry']
                lat = geometry['location']['lat']
                lon = geometry['location']['lng']
            else:
                return render(request, 'restaurants/error.html',{
                    'error_message_couldnt_locate_restaurant': "Unfortunately something went wrong! Please check if you entered a correct address."
                })
            restaurant.lat = lat
            restaurant.lon = lon

            restaurant.country = land_user_berechnen(lat, lon)  
            country_phone_number = phone_number_country(vorwahl)
            
            #vorwahl 1
            if country_phone_number == 'United States':
                if restaurant.country != 'United States' and restaurant.country != 'Canada':
                    return render(request, 'restaurants/error.html', {
                    'error_message_country_different': "Unfortunately something went wrong! You can only enter a phone number located in the same country as your restaurant. If you are located near to a country border and are dealing with this problem please contact our support (contact@wherevegan.de) and we will manage this specific situation."
                })
            #vorwahl 7
            if country_phone_number == 'Қазақстан':
                if restaurant.country != 'Қазақстан' and restaurant.country != 'Россия':
                    return render(request, 'restaurants/error.html', {
                    'error_message_country_different': "Unfortunately something went wrong! You can only enter a phone number located in the same country as your restaurant. If you are located near to a country border and are dealing with this problem please contact our support (contact@wherevegan.de) and we will manage this specific situation."
                })
                
            if country_phone_number == 'Dominica':
                if restaurant.country != 'Dominica' and restaurant.country != 'República Dominicana':
                    return render(request, 'restaurants/error.html', {
                    'error_message_country_different': "Unfortunately something went wrong! You can only enter a phone number located in the same country as your restaurant. If you are located near to a country border and are dealing with this problem please contact our support (contact@wherevegan.de) and we will manage this specific situation."
                })
            if country_phone_number == 'Việt Nam':
                if restaurant.country != 'Việt Nam' and restaurant.country != 'British Virgin Islands' and restaurant.country != 'United States':
                    return render(request, 'restaurants/error.html', {
                    'error_message_country_different': "Unfortunately something went wrong! You can only enter a phone number located in the same country as your restaurant. If you are located near to a country border and are dealing with this problem please contact our support (contact@wherevegan.de) and we will manage this specific situation."
                })
            if country_phone_number != 'United States' and country_phone_number != 'Қазақстан' and country_phone_number != 'Dominica' and country_phone_number != 'Việt Nam':
                if not restaurant.country == country_phone_number:
                    return render(request, 'restaurants/error.html', {
                        'error_message_country_different': "Unfortunately something went wrong! You can only enter a phone number located in the same country as your restaurant. If you are located near to a country border and are dealing with this problem please contact our support (contact@wherevegan.de) and we will manage this specific situation."
                    })

            #überprüfen ob es das restaurant schon gibt
            city_restaurant = standort_restaurant.objects.filter(country=restaurant.country)
            for pub in city_restaurant:
                address1 = pub.address.lower()
                address2 = restaurant.address.lower()
                name1 = pub.restaurant_name.lower()
                name2 = restaurant.restaurant_name.lower()
                if address1 == address2 and name1 == name2:
                    if pub.verified == False:
                        pub.delete()
                        continue
                    return render(request, 'restaurants/error.html', {
                        'error_message_restaurant_already_exists': 'Something went wrong! It looks like there is already a restaurant registered with the same credentials.'
                    })
            restaurant.save()
            phone_code = create_code()
            code_senden(restaurant.email, phone_code, request)
            code_hashed = hash_code(phone_code)
            code_hashed = str(code_hashed)
            
            return render(request, 'restaurants/code.html', {
                'ch': code_hashed,
                'r': restaurant.restaurant_name,
                'a': restaurant.address,
                'p': phone,
                'e': restaurant.email,
            })
        return render(request, 'restaurants/error.html', {
                        'error_message_recaptcha': 'reCAPTCHA error'
                    })
    else:
        return render(request, 'restaurants/add.html')

#required 
def phone_code_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        code_hashed = request.POST.get('ch')
        code_hashed = int(code_hashed)
        restaurant_name = request.POST.get('r')
        address = request.POST.get('a')
        phone = request.POST.get('p')
        email = request.POST.get('e')
        if code == '' or code_hashed == '' or restaurant_name == '' or address == '' or phone == '' or email == '':
            return render(request, 'restaurants/error.html', {
                'error_message_fehlende_informationen': 'Unfortunately something went wrong! It looks like you forgot to enter your code.'
            })
        
        code = int(code)
        code = hash_code(code)
        if code == code_hashed:
            try: 
                restaurant_richtig = standort_restaurant.objects.get(restaurant_name=restaurant_name, address=address, email=email)
            except ObjectDoesNotExist:
                return render(request, 'restaurants/error.html', {
                'error_message_restaurantdaten_verändert': 'Unfortunately something went wrong. Please try again!'
                })
            if restaurant_richtig.verified == False:
                restaurant_richtig.verified = True
                restaurant_richtig.save()
                return render(request, 'restaurants/added.html', {
                    'restaurant_name': restaurant_richtig.restaurant_name,
                    'address': restaurant_richtig.address
                })
            else:
                return render(request, 'restaurants/error.html', {
                'error_message_already_verified': 'Unfortunately something went wrong. It looks like this restaurant is already registered.'
            })
        else:
            return render(request, 'restaurants/error.html', {
                'error_message_falscher_code': 'Your code is incorrect.'
            })
    else:
        return render(request, 'restaurants/error.html')

def email_again_view(request):
    #kann sein das ich ein seperates form machen muss um, da dies nicht als post verschickt wurde
    restaurant_name = request.POST.get('r')
    address = request.POST.get('a')
    phone = request.POST.get('p')
    email = request.POST.get('e')
    if restaurant_name == '' or address == '' or phone == '' or email == '':
        return render(request, 'restaurants/error.html', {
            'error_message_fehlende_informationen_again': 'Unfortunately something went wrong! Please try again'
        })
    return render(request, 'restaurants/again.html', {
        'r': restaurant_name,
        'a': address,
        'p': phone,
        'e': email,
    })

def email_again(request):
    if request.method == 'POST':
        restaurant_name = request.POST.get('r')
        address = request.POST.get('a')
        phone = request.POST.get('p')
        email = request.POST.get('e')
        email_again = request.POST.get('email2')
        if restaurant_name == '' or address == '' or phone == '' or email == '' or email_again == '':
            return render(request, 'restaurants/error.html', {
                'error_message_fehlende_informationen_again': 'Unfortunately something went wrong! Please try again'
            }) 
        if email_check(email_again) == False:
            return render(request, 'restaurants/error.html', {
                'error_message_email_invalid': 'Unfortunately something went wrong! It looks like you entered an invalid email address! Due to our safety protocols you will need to register your restaurant again!'
            }) 
        if not email_again == email:
            return render(request, 'restaurants/error.html', {
                'error_message_email_not_same': 'Unfortunately something went wrong! It looks like you entered a different email address. Due to our safety protocols you will need to register your restaurant again!'
            }) 
        code = create_code()
        code_senden(email_again, code, request)
        code_hashed = hash_code(code)
        code_hashed = str(code_hashed)
        return render(request, 'restaurants/code.html', {
            'ch': code_hashed,
            'r': restaurant_name,
            'a': address,
            'p': phone,
            'e': email,
        })
    else:
        return render(request, 'restaurants/error.html', {
                'error_message_email_again_error': 'Unfortunately something went wrong! Please try again!'
            }) 
        
def einzel_standort_berechnen(request):
    if request.method == 'POST':
        lat = request.POST.get('lat1')
        lon = request.POST.get('lon1')
        safety = request.POST.get('s1')

        range_user = request.POST.get('range')
        for letter in range_user:
            if ord(letter) == 75 or ord(letter) == 77 or ord(letter) == 107 or ord(letter) == 109:
                letter = ''
                print(letter)
        if range_user == '':
            return render(request, 'restaurants/error.html', {
                'error_message_range': 'Unfortunately something went wrong with your requested range. Please submit a number greater than 0 and smaller than 150. Thank you!'
            })
        for char in range_user:
            if ord(char) < 48 or ord(char) > 57:
                return render(request, 'restaurants/error.html', {
                'error_message_range': 'Unfortunately something went wrong with your requested range. Please submit a number greater than 0 and smaller than 150. Thank you!'
            })
        #honeyput search
        if safety != '':
            return render(request, 'restaurants/error.html', {
                'error_message_safety': 'Unfortunately something went wrong with your request. Please try again!'
            })
        range_user = float(range_user)
        if range_user <= 0 or range_user > 150:
            return render(request, 'restaurants/error.html', {
                'error_message_range': 'Unfortunately something went wrong with your requested range. Please submit a number greater than 0 and smaller than 150. Thank you!'
            })
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return render(request, 'restaurants/error.html', {
                'error_message_latlon_safety': 'Unfortunately something went wrong. Please try again!'
            })
        if lat < 0 or lat > 180 or lon < 0 or lon > 360:
            return render(request, 'restaurants/error.html', {
                'error_message_lon_lat': 'Unfortunately something went wrong with tracking your coordinates'
            })
        distanzen = []
        country_user = land_user_berechnen(lat, lon)
        #restaurants_nah = restaurants_nähe(lat, lon, country_user, range_user)

        city_restaurant = standort_restaurant.objects.filter(country=country_user, verified=True, menu=True)
    
        restaurants_nähe = []
        for lokal in city_restaurant:
            distanz1 = distanz_berechnen(lat,lon, lokal)
            if distanz1 < range_user:
                restaurants_nähe.append(lokal)
                
       
            #create a map
        point = (lat, lon)
        m = folium.Map(width=800, height=500, location=point,
        zoom_start=15
        )
        folium.Marker([lat, lon], popup='Current Location',
        icon=folium.Icon(color='black')).add_to(m)
            
            
            #distanz der einzelnen Restaurants zum User berechnen
        for restaurant in restaurants_nähe:
            distanz = distanz_berechnen(lat, lon, restaurant)
            distanz = math.ceil(distanz * 10) / 10
            distanzen.append(distanz)
            folium.Marker([restaurant.lat, restaurant.lon], popup='<b>{}</b>, {}'.format(restaurant, restaurant.address),
            icon=folium.Icon(color='green')).add_to(m)
        m = m._repr_html_() #map in html schreibweise repräsentieren
        return render(request, 'restaurants/nearby.html', {
            'restaurants': restaurants_nähe,
            'distanzen': distanzen,
            'map': m
        })
    else:
        return render(request, 'restaurants/nearby.html')


def distanz_berechnen(lat, lon, name2):
    place2 = standort_restaurant.objects.get(restaurant_name=name2, address=name2.address, verified=True, menu=True)

    lon1 = radians(lon)
    lat1 = radians(lat)

    lon2 = radians(place2.lon)
    lat2 = radians(place2.lat)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    
    c = 2 * asin(sqrt(a))
        
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
        
    # calculate the result
    distance = (c * r)
    return distance

def restaurants_nähe(lat, lon, country, range_user):
    city_restaurant = standort_restaurant.objects.filter(country=country, verified=True)
    
    restaurants_nähe = []
    for lokal in city_restaurant:
        distanz1 = distanz_berechnen(lat,lon, lokal)
        if distanz1 < range_user:
            restaurants_nähe.append(lokal.restaurant_name)
            
    return restaurants_nähe

def land_user_berechnen(lat, lon):
    geolocator = Nominatim(user_agent="geoapiExercises")
    
    coord = '{}, {}'.format(lat, lon)
    land = city_state_country(coord, geolocator)
    return land
def city_state_country(coord, geolocator):
        location = geolocator.reverse(coord, exactly_one=True)
        address = location.raw['address']
        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')
        return country

def name_check(name):
    for char in name:
        if ord(char) > 39 and ord(char) < 65 or ord(char) > 32 and ord(char) < 39 or ord(char) > 90 and ord(char) < 97 or ord(char) == 123 or ord(char) == 124 or ord(char) == 125 or ord(char) == 126:
            return False
    return True

def email_check(email):
    try:
        validation = validate_email(email, check_deliverability=True)
    except EmailNotValidError as e:
        return False
    return True

def phonenumber_validate(number):
	try:
		phone_number = phonenumbers.parse(number)
		valid = phonenumbers.is_valid_number(phone_number)

		possible = phonenumbers.is_possible_number(phone_number)

		if possible == True and valid == True:
			return True
		return False
	except NumberParseException:
		return False

def code_senden(email, code, request):
    import requests

    """
    * Send an email message by using Infobip API.
    *
    * This example is already pre-populated with your account data:
    * 1. Your account Base URL
    * 2. Your account API key
    * 3. Your recipient email
    *
    * THIS CODE EXAMPLE IS READY BY DEFAULT. HIT RUN TO SEND THE MESSAGE!
    *
    * Send email API reference: https://www.infobip.com/docs/api#channels/email/send-email
    * See Readme file for details.
    """

    BASE_URL = "https://yren59.api.infobip.com"
    API_KEY = "App fef126cbee854003dca50539819919c9-0154e71d-cd21-4429-879e-aab138fffdf1"

    SENDER_EMAIL = "wherevegan@selfserviceib.com"
    RECIPIENT_EMAIL = email
    EMAIL_SUBJECT = "Authentication code"
    EMAIL_TEXT = code

    formData = {
        "from": SENDER_EMAIL,
        "to": RECIPIENT_EMAIL,
        "subject": EMAIL_SUBJECT,
        "text": EMAIL_TEXT,
        "replyTo": "contact@wherevegan.de",
    }

    all_headers = {
        "Authorization": API_KEY
    }

    response = requests.post(BASE_URL + "/email/2/send", files=formData, headers=all_headers)
    print("Status Code: " + str(response.status_code))
    print(response.json())
    status_code = int(response.status_code)
    if not status_code == 200:
        return render(request, 'restaurants/error.html', {
                'error_message_email_code_not_send': 'Unfortunately we were not able to send you an email. Please try again!'
            })
    
def create_code():
    #random 6-stelligen Code erstellen
    number1 = str(random.randint(0,9))
    number2 = str(random.randint(0,9))
    number3 = str(random.randint(0,9))
    number4 = str(random.randint(0,9))
    number5 = str(random.randint(0,9))
    number6 = str(random.randint(0,9))
    code = number1 + number2 + number3 + number4 + number5 + number6
    return code
def hash_code(phone_code):
    #code hashen z.B. ord() an 2. stelle + 3 und an 4. + 17
    code = int(phone_code)
    code = code / 13.245
    code = int(code)
    code = code - 36
    return code
def phone_number_country(number):
    if number == '+1':
        return 'United States'
    if number == '+44':
        return 'United Kingdom'
    if number == '+213':
        return 'Algérie / ⵍⵣⵣⴰⵢⴻⵔ / الجزائر'
    if number == '+376':
        return 'Andorra'
    if number == '+244':
        return 'Angola'
    if number == '+1264':
        return 'Anguilla'
    if number == '+1268':
        return 'Antigua and Barbuda'
    if number == '+54':
        return 'Argentina'
    if number == '+374':
        return 'Հայաստան'
    if number == '+297':
        return 'Nederland'
    if number == '+61':
        return 'Australia'
    if number == '+43':
        return 'Österreich'
    if number == '+994':
        return 'Azərbaycan'
    if number == '+1242':
        return 'The Bahamas'
    if number == '+973':
        return 'البحرين'
    if number == '+880':
        return 'বাংলাদেশ'
    if number == '+1246':
        return 'Barbados'
    if number == '+375':
        return 'Беларусь'
    if number == '+32':
        return 'België / Belgique / Belgien'
    if number == '501':
        return 'Belize'
    if number == '+229':
        return 'Bénin'
    if number == '+1441':
        return 'Bermuda'
    if number == '+975':
        return 'འབྲུགཡུལ་'
    if number == '+591':
        return 'Bolivia'
    if number == '+387':
        return 'Bosna i Hercegovina / Босна и Херцеговина'
    if number == '+267':
        return 'Botswana'
    if number == '+55':
        return 'Brasil'
    if number == '+673':
        return 'Brunei'
    if number == '+359':
        return 'България'
    if number == '+226':
        return 'Burkina Faso'
    if number == '+257':
        return 'Burundi'
    if number == '+855':
        return 'ព្រះរាជាណាចក្រ​កម្ពុជា'
    if number == '+237':
        return 'Cameroun'
    if number == '+238':
        return 'Cabo Verde'
    if number == '+1345':
        return 'Cayman Islands'
    if number == '+236':
        return 'Ködörösêse tî Bêafrîka - République Centrafricaine'
    if number == '+56':
        return 'Chile'
    if number == '+86':
        return '中国'
    if number == '+57':
        return 'Colombia'
    if number == '+269':
        return 'Comores Komori جزر القمر'
    if number == '+242':
        return 'République démocratique du Congo'
    if number == '+682':
        return "Kūki 'Āirani"
    if number == '+506':
        return 'Costa Rica'
    if number == '+385':
        return 'Hrvatska'
    if number == '+53':
        return 'Cuba'
    if number == '+90392':
        return 'Κύπρος - Kıbrıs'
    if number == '+357':
        return 'Κύπρος - Kıbrıs'
    if number == '+42':
        return 'Česko'
    if number == '+45':
        return 'Danmark'
    if number == '+253':
        return 'Djibouti جيبوتي'
    if number == '+1809':
        return 'Dominica'
    if number == '+593':
        return 'Ecuador'
    if number == '+20':
        return 'مصر'
    if number == '+503':
        return 'El Salvador'
    if number == '+240':
        return 'Guinea Ecuatorial'
    if number == '+291':
        return 'ኤርትራ Eritrea إرتريا'
    if number == '+372':
        return 'Eesti'
    if number == '+251':
        return 'ኢትዮጵያ'
    if number == '+500':
        return 'Falkland Islands'
    if number == '+298':
        return 'Føroyar'
    if number == '+679':
        return 'Viti'
    if number == '+358':
        return 'Suomi / Finland'
    if number == '+33':
        return 'France'
    if number == '+594':
        return 'France'
    if number == '+689':
        return 'France'
    if number == '+241':
        return 'Gabon'
    if number == '+220':
        return 'Gambia'
    if number == '+7880':
        return 'საქართველო'
    if number == '+233':
        return 'Ghana'
    if number == '+350':
        return 'Gibraltar'
    if number == '+30':
        return 'Ελλάς'
    if number == '+299':
        return 'Kalaallit Nunaat'
    if number == '+1473':
        return 'Grenada'
    if number == '+590':
        return 'France'
    if number == '+671':
        return 'United States'
    if number == '+502':
        return 'Guatemala'
    if number == '+224':
        return 'Guinée'
    if number == '+245':
        return 'Guiné-Bissau'
    if number == '+592':
        return 'Guyana'
    if number == '+509':
        return 'Ayiti'
    if number == '+504':
        return 'Honduras'
    if number == '+852':
        return '中国'
    if number == '+36':
        return 'Magyarország'
    if number == '+354':
        return 'Ísland'
    if number == '+91':
        return 'India'
    if number == '+62':
        return 'Indonesia'
    if number == '+98':
        return 'ایران'
    if number == '+964':
        return 'العراق'
    if number == '+353':
        return 'Éire / Ireland'
    if number == '+972':
        return 'ישראל'
    if number == '+39':
        return 'Italia'
    if number == '+1876':
        return 'Jamaica'
    if number == '+81':
        return '日本'
    if number == '+962':
        return 'الأردن'
    if number == '+7':
        return 'Қазақстан'
    if number == '+254':
        return 'Kenya'
    if number == '+686':
        return 'Kiribati'
    if number == '+850':
        return '조선민주주의인민공화국'
    if number == '+82':
        return '대한민국'
    if number == '+965':
        return 'الكويت'
    if number == '+996':
        return 'Кыргызстан'
    if number == '+856':
        return 'ປະເທດລາວ'
    if number == '+371':
        return 'Latvija'
    if number == '+961':
        return 'لبنان'
    if number == '+266':
        return 'Lesotho'
    if number == '+231':
        return 'Liberia'
    if number == '+218':
        return 'ليبيا'
    if number == '+417':
        return 'Liechtenstein'
    if number == '+370':
        return 'Lietuva'
    if number == '+352':
        return 'Lëtzebuerg'
    if number == '+853':
        return '中国'
    if number == '+389':
        return 'Северна Македонија'
    if number == '+261':
        return 'Madagasikara / Madagascar'
    if number == '+265':
        return 'Malawi'
    if number == '+60':
        return 'Malaysia'
    if number == '+960':
        return 'ދިވެހިރާއްޖެ'
    if number == '+223':
        return 'Mali'
    if number == '+356':
        return 'Malta'
    if number == '+692':
        return 'Ṃajeḷ'
    if number == '+596':
        return 'France'
    if number == '+222':
        return 'موريتانيا'
    if number == '+269':
        return 'France'
    if number == '+52':
        return 'México'
    if number == '+691':
        return 'Micronesia'
    if number == '+373':
        return 'Moldova'
    if number == '+377':
        return 'Monaco'
    if number == '+976':
        return 'Монгол улс ᠮᠤᠩᠭᠤᠯ ᠤᠯᠤᠰ'
    if number == '+1664':
        return 'Montserrat'
    if number == '+212':
        return 'Maroc / ⵍⵎⵖⵔⵉⴱ / المغرب'
    if number == '+258':
        return 'Moçambique'
    if number == '+95':
        return 'မြန်မာ'
    if number == '+264':
        return 'Namibia'
    if number == '+674':
        return 'Naoero'
    if number == '+977':
        return 'नेपाल'
    if number == '+31':
        return 'Nederland'
    if number == '+687':
        return 'France'
    if number == '+64':
        return 'New Zealand / Aotearoa'
    if number == '+505':
        return 'Nicaragua'
    if number == '+227':
        return 'Niger'
    if number == '+234':
        return 'Nigeria'
    if number == '+683':
        return 'Niuē'
    if number == '+672':
        return 'Australia'
    if number == '+670':
        return 'United States'
    if number == '+47':
        return 'Norge'
    if number == '+968':
        return 'عمان'
    if number == '+680':
        return 'Belau'
    if number == '+507':
        return 'Panamá'
    if number == '+675':
        return 'Papua Niugini'
    if number == '+595':
        return 'Paraguay / Paraguái'
    if number == '+51':
        return 'Perú'
    if number == '+63':
        return 'Philippines'
    if number == '+48':
        return 'Polska'
    if number == '+351':
        return 'Portugal'
    if number == '+1787':
        return 'United States'
    if number == '+974':
        return 'قطر'
    if number == '+262':
        return 'France'
    if number == '+40':
        return 'România'
    if number == '+250':
        return 'Tanzania'
    if number == '+378':
        return 'San Marino'
    if number == '+239':
        return 'São Tomé e Príncipe'
    if number == '+966':
        return 'السعودية'
    if number == '+221':
        return 'Sénégal'
    if number == '+381':
        return 'Србија'
    if number == '+248':
        return 'Sesel'
    if number == '+232':
        return 'Sierra Leone'
    if number == '+65':
        return 'Singapore'
    if number == '+421':
        return 'Slovensko'
    if number == '+386':
        return 'Slovenija'
    if number == '+677':
        return 'Solomon Islands'
    if number == '+252':
        return 'Soomaaliya الصومال'
    if number == '+27':
        return 'South Africa'
    if number == '+34':
        return 'España'
    if number == '+94':
        return 'ශ්‍රී ලංකාව இலங்கை'
    if number == '+290':
        return 'Saint Helena, Ascension and Tristan da Cunha'
    if number == '+1869':
        return 'Saint Kitts and Nevis'
    if number == '+1758':
        return 'Saint Lucia'
    if number == '+249':
        return 'السودان'
    if number == '+597':
        return 'Suriname'
    if number == '+268':
        return 'eSwatini'
    if number == '+46':
        return 'Sverige'
    if number == '+41':
        return 'Schweiz/Suisse/Svizzera/Svizra'
    if number == '+963':
        return 'سوريا'
    if number == '+886':
        return '臺灣'
    if number == '+66':
        return 'ประเทศไทย'
    if number == '+228':
        return 'Togo'
    if number == '+676':
        return 'Tonga'
    if number == '+1868':
        return 'Trinidad and Tobago'
    if number == '+216':
        return 'تونس'
    if number == '+90':
        return 'Türkiye'
    if number == '+993':
        return 'Türkmenistan'
    if number == '+1649':
        return 'Turks and Caicos Islands'
    if number == '+688':
        return 'Tuvalu'
    if number == '+256':
        return 'Uganda'
    if number == '+380':
        return 'Україна'
    if number == '+971':
        return 'الإمارات العربية المتحدة'
    if number == '+598':
        return 'Uruguay'
    if number == '+678':
        return 'Vanuatu'
    if number == '+379':
        return 'Civitas Vaticana - Città del Vaticano'
    if number == '+58':
        return 'Venezuela'
    if number == '+84':
        return 'Việt Nam' 
    if number == '+681':
        return 'France'
    if number == '+969':
        return 'اليمن'
    if number == '+967':
        return 'اليمن'
    if number == '+260':
        return 'Zambia'
    if number == '+263':
        return 'Zimbabwe'
    if number == '+992':
        return 'Тоҷикистон'
    if number == '+998':
        return 'Oʻzbekiston'
    return 'none'

#superuser:
#   dxni
#   DanielWlach1!040405

"""
virtuel environment
installation of:
    captcha 

git add .
git commit -am "xyz"
git push
git push heroku main
"""