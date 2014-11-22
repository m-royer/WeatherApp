# -*- coding: utf-8 -*-
import urllib.parse
import urllib.request
import json

endprogram = "y"
#global returned
returned = False

print('{:^80}'.format("WEATHER APP"))

class WeatherApp:
    def __init__(self):
        self.data = {}
        self.url = 'http://api.openweathermap.org/data/2.5/weather/'
        self.weather_object = {}

    def urlopen(self, cityname):
        global returned
        returned = False
        self.cityname = cityname
        self.data = {}
        self.data['q'] = self.cityname
        self.url_data = urllib.parse.urlencode(self.data)
        full_url = self.url + '?' + self.url_data
        try:
            self.response = urllib.request.urlopen(full_url)
            self.json_data = self.response.read().decode('utf-8')
            # decode the JSON
            self.weather_object = json.loads(self.json_data)
        except urllib.error.HTTPError as e:
            returned = True
            return "Error " + e.code() + ": " + e.read()
        else:
            returned = True

    def gettemp(self):
        # Temperature in kelvin:
        self.temp = self.weather_object['main']['temp']
        self.temp = self.temp - 273.15 # 0 celsius = 273.15 kelvin
        # Convert to F
        self.temp = (9/5) * self.temp + 32
        return "{0:.1f}".format(self.temp)
    
    def getdesc(self):
        return self.weather_object['weather'][0]['description']

    def getname(self):
        return self.weather_object['name']

    def dump(self):
        print(self.weather_object)

    def getmsg(self):
        try:
            self.weather_object['message']
        except KeyError:
            msg = {'flag': True, 'msg': 'a-okay!'}
        else:
            msg = {'flag': False, 'msg': self.weather_object['message']}
            
        return msg
    
####################################################################
########################### THE PROGRAM: ###########################
####################################################################

while endprogram == "y":
    cityname = input("City Name, State/Country: ")
    CurrentWeather = WeatherApp()
    CurrentWeather.urlopen(cityname)

    # wait for our promised flag
    while returned == False:
        print("returned: " + str(returned))
        
    successmsg = CurrentWeather.getmsg()
    if successmsg['flag'] == True:
        temp = CurrentWeather.gettemp()
        desc = CurrentWeather.getdesc()
        name = CurrentWeather.getname()
        print("City Name: " + name)
        print("Current temperature: " + str(temp) + u'\N{DEGREE SIGN}' + "F")
        print("Current weather: " + desc)
    else:
        print(successmsg['msg'])
    

    # end program
    endprogram = input("Enter a new city? (y/n) ")


'''

The return object:

{
    'main': {
        'temp': 286.12,
        'temp_max': 287.15,
        'humidity': 87,
        'temp_min': 285.15,
        'pressure': 1001
    },
    'wind': {
        'deg': 320,
        'gust': 10.8,
         'speed': 8.2
    }, 'id': 5710756,
    'name': 'Albany',
    'cod': 200, 'base':
    'cmc stations',
    'sys': {
        'id': 2285,
        'sunset': 1416703099,
        'type': 1,
        'message': 0.0532,
        'sunrise': 1416669553,
        'country': 'United States of America'
    },
    'dt': 1416631380,
    'coord': {
        'lat': 44.64,
        'lon': -123.11
    },
    'weather': [
        {
            'main': 'Rain',
            'id': 501,
            'icon': '10n',
            'description': 'moderate rain'
        },
        {
            'main': 'Mist',
            'id': 701,
            'icon': '50n',
            'description': 'mist'
        }
    ],
    'clouds': {
        'all': 90
    }
}

'''
