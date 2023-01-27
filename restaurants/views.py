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

from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext

API_KEY = 'AIzaSyDU6RdLpMKVZuKX4d8IyfIW5l83TveSz4g'
lat_speicher = ''
lon_speicher = ''

# Create your views here.
def home(request):
    trans = translate(language='de')
    return render(request, 'restaurants/nearby.html', {
        'trans': trans,
    })
def restaurant_add(request):
    return render(request, 'restaurants/add.html', {
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY
    })
def contact2(request):
    return render(request, 'restaurants/contact2.html')
def privacy(request):
    return render(request, 'restaurants/privacy.html')


def translate(language):
    curl_language = get_language()
    try:
        activate(language)
        text = gettext('hello')
    finally:
        activate(curl_language)
    return text

def gps_berechnen(request):
    if request.method == 'POST':
        restaurant = standort_restaurant()
        restaurant.first_name = request.POST.get('first_name')
        restaurant.last_name = request.POST.get('last_name')
        restaurant.restaurant_name = request.POST.get('restaurant_name')
        restaurant.address = request.POST.get('address')
        restaurant.email = request.POST.get('email')
        vorwahl = request.POST.get('countryCode')
        phone = request.POST.get('phone_number')
        gtc_check = request.POST.get('gtc_check')
        restaurant.verified = False
        restaurant.menu = False

        address = request.POST.get('address') #um es als extra variable zu haben
        if restaurant.address == '' or restaurant.restaurant_name == '' or restaurant.email == '' or phone == '' or restaurant.first_name == '' or restaurant.last_name == '' or vorwahl == '':
            return render(request, 'restaurants/error.html', {
                'error_message_not_enough_information': _('Unfortunately something went wrong. It looks like you forgot to fill out a field.')
            })
        #überprüfen ob die gtc akzeptiert wurden
        if gtc_check != 'true':
            return render(request, 'restaurants/error.html', {
                'error_message_gtc': _('Unfortunately something went wrong. You can only register your restaurant by accepting our general terms and conditions!')
            })
        vorwahl = str(vorwahl)
        phone = str(phone)
        phone = vorwahl + phone
        if name_check(restaurant.first_name) == False or name_check(restaurant.last_name) == False:
            return render(request, 'restaurants/error.html', {
                'error_message_name_wrong': _('Unfortunately something went wrong! Please check whether you only entered letters and not numbers for your first and last name')
            })
        if email_check(restaurant.email) == False:
            return render(request, 'restaurants/error.html', {
                'error_message_email_false': _('It looks like you entered an invalid email')
            })
        if phonenumber_validate(phone) == False:
            return render(request, 'restaurants/error.html', {
                'error_message_phone_number': _('Unfortunately something went wrong! Please check whether you entered a valid phone number!'),
                'error_message_e164': _('Please use the international phone number format e164 following your country code!')
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
                    'error_message_couldnt_locate_restaurant': _("Unfortunately something went wrong! Please check if you entered a correct address.")
                })
            restaurant.lat = lat
            restaurant.lon = lon

            restaurant.country = land_user_berechnen(lat, lon)  

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
                        'error_message_restaurant_already_exists': _('Something went wrong! It looks like there is already a restaurant registered with the same credentials.')
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
                'error_message_fehlende_informationen': _('Unfortunately something went wrong! It looks like you forgot to enter your code.')
            })
        
        code = int(code)
        code = hash_code(code)
        if code == code_hashed:
            try: 
                restaurant_richtig = standort_restaurant.objects.get(restaurant_name=restaurant_name, address=address, email=email)
            except ObjectDoesNotExist:
                return render(request, 'restaurants/error.html', {
                'error_message_restaurantdaten_verändert': _('Unfortunately something went wrong. Please try again!')
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
                'error_message_already_verified': _('Unfortunately something went wrong. It looks like this restaurant is already registered.')
            })
        else:
            return render(request, 'restaurants/error.html', {
                'error_message_falscher_code': _('Your code is incorrect.')
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
            'error_message_fehlende_informationen_again': _('Unfortunately something went wrong! Please try again')
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
                'error_message_fehlende_informationen_again': _('Unfortunately something went wrong! Please try again')
            }) 
        if email_check(email_again) == False:
            return render(request, 'restaurants/error.html', {
                'error_message_email_invalid': _('Unfortunately something went wrong! It looks like you entered an invalid email address! Due to our safety protocols you will need to register your restaurant again!')
            }) 
        if not email_again == email:
            return render(request, 'restaurants/error.html', {
                'error_message_email_not_same': _('Unfortunately something went wrong! It looks like you entered a different email address. Due to our safety protocols you will need to register your restaurant again!')
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
                'error_message_email_again_error': _('Unfortunately something went wrong! Please try again!')
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
                'error_message_range': _('Unfortunately something went wrong with your requested range. Please submit a number greater than 0 and smaller than 150. Thank you!')
            })
        for char in range_user:
            if ord(char) < 48 or ord(char) > 57:
                return render(request, 'restaurants/error.html', {
                'error_message_range': _('Unfortunately something went wrong with your requested range. Please submit a number greater than 0 and smaller than 150. Thank you!')
            })
        #honeyput search
        if safety != '':
            return render(request, 'restaurants/error.html', {
                'error_message_safety': _('Unfortunately something went wrong with your request. Please try again!')
            })
        range_user = float(range_user)
        if range_user <= 0 or range_user > 150:
            return render(request, 'restaurants/error.html', {
                'error_message_range': _('Unfortunately something went wrong with your requested range. Please submit a number greater than 0 and smaller than 150. Thank you!')
            })
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return render(request, 'restaurants/error.html', {
                'error_message_latlon_safety': _('Unfortunately something went wrong. Please try again!')
            })
        if lat < 0 or lat > 180 or lon < 0 or lon > 360:
            return render(request, 'restaurants/error.html', {
                'error_message_lon_lat': _('Unfortunately something went wrong with tracking your coordinates')
            })
        distanzen = []
        country_user = land_user_berechnen(lat, lon)
        #restaurants_nah = restaurants_nähe(lat, lon, country_user, range_user)

        city_restaurant = standort_restaurant.objects.filter(country=country_user, verified=True, menu=True) #menu=True
        restaurants_nähe = []
        for lokal in city_restaurant:
            distanz1 = distanz_berechnen(lat,lon, lokal)
            if distanz1 < range_user:
                restaurants_nähe.append(lokal)
                
        if restaurants_nähe == []:
            message = _('Unfortunately there are no vegan restaurants in your requested range.')
            return render(request, 'restaurants/nearby.html', {
                'no_restaurants': message
            })
            #create a map
        point = (lat, lon)
        m = folium.Map(width=800, height=500, location=point,
        zoom_start=15
        )
        folium.Marker([lat, lon], popup=_('Current Location'),
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
                'error_message_email_code_not_send': _('Unfortunately we were not able to send you an email. Please try again!')
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




"""
git add .
git commit -am "xyz"
git push
git push heroku main
heroku logs -t

heroku run python3 manage.py 
python3 manage.py collectstatic

python3 manage.py makemessages --all
python3 manage.py compilemessages
"""