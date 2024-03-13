import requests
from requests.exceptions import RequestException


def get_user_location():
    url = 'http://ip-api.com/json/?fields=status,city,lat,lon'
    try:
        response = requests.get(url)

        if not response.status_code == 200:
            raise RequestException(f"Unable to get location data. Status code: {response.status_code}")
        
        data = response.json()
        if not data["status"] == "success":
            raise RequestException(f"Fetch result failed")
        data.pop("status", None)
        return data
    except RequestException as e:
        print(f"RequestException: {e}")
        return None


def get_weather_for_cords(lat, lon):
    # throwaway api key
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=f0ea9f2e8570e4182ef8e82a12096af1&units=metric"
    try:
        response = requests.get(url)

        if not response.status_code == 200:
            raise RequestException(f"Unable to get weather data. Status code: {response.status_code}")
        
        data = response.json()
        if not data.get("main", None):
            raise RequestException(f"Fetch result failed")
        
        res = {'temp': data['main']['temp'],
               'feels_like': data['main']['feels_like']}
        return res
    except RequestException as e:
        print(f"RequestException: {e}")
        return None


def print_output(weather_info, city=None):
    try:
        print('='*50)
        print(f'''\n\tIt`s currently {weather_info["temp"]}° {"in "+ str(city) if city else "in your location"},
        which feels like {weather_info["feels_like"]}°!
        ''')
        print('='*50)
    except KeyError as e:
        print(f'Key error in froming output. {e}')
    

def main():
    while True:
        try: 
            location = get_user_location()
            weather_info = get_weather_for_cords(lat=location['lat'], lon=location['lon'])
            print_output(weather_info, location.get('city', None))
            break
        except Exception as e:
            print(f"Unexpected error\n{e} \nAttempting again")


if __name__ == "__main__":
    main()
