#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyowm
from flask import Flask, render_template, request, send_file
from texttospeech import tts
from tts import _TTS
import os
import sys, json
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

app = Flask(__name__)


CLIENT_ACCESS_TOKEN = '' # Token de acceso al cliente del agente de Weather-chatbot' # Token de acceso al cliente del agente de Weather-chatbot
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN) #Conexion con el agente de Weather-Chatbot


app = Flask(__name__)
PATH = "C:\asistente_web_clima"


@app.route('/')
def init_recorder():
    return render_template('VoiceRecorder.html')


@app.route('/uploads', methods=['POST'])
def save_audio():
    rawAudio = request.get_data()
    audioFile = open('RecordedFile.wav', 'wb')
    audioFile.write(rawAudio)
    audioFile.close()
    return speech_to_text()
    

def speech_to_text():
    my_tts = _TTS()
    result = my_tts.start()
    result_query = parse_user_message(result)
    return result_query


def parse_user_message(user_text):
    '''
    Envia el mensaje a API AI que invoca una intención
    y retorna la respuesta en consecuencia
    A la respuesta del bot se agrega con los datos del clima obtenidos desde la consulta via API a OpenWeatherMap
    '''
    request = ai.text_request()
    request.query = user_text

    response = json.loads(request.getresponse().read().decode('utf-8'))
    responseStatus = response['status']['code']
    if (responseStatus == 200):
        print("API AI response", response['result']['fulfillment']['speech'])
        try:
            # Using open weather map client to fetch the weather report
            weather_report = ''

            input_city = response['result']['parameters']['geo-city']
            print("City ", input_city)

            owm = pyowm.OWM('')  # Api Key de OpenWeather
            observation = owm.weather_at_place(input_city)
            w = observation.get_weather()
            max_temp = str(w.get_temperature('celsius')['temp_max'])
            min_temp = str(w.get_temperature('celsius')['temp_min'])
            current_temp = str(w.get_temperature('celsius')['temp'])
            wind_speed = str(w.get_wind()['speed'])
            humidity = str(w.get_humidity())

            weather_report = ' Temperatura Máx: ' + max_temp + ' Temperatura Min: ' + min_temp + ' Temperatura Actual: '\
                             + current_temp + ' Velocidad del Viento :' + wind_speed + ' Humedad ' + humidity + '%'
            print("Weather report ", weather_report)
            text_res = (response['result']['fulfillment']['speech'] + weather_report)
            print(text_res)
            tts(text_res, "ES", "response.mp3")
            file = open('response.mp3', 'rb')
            return send_file(file, mimetype='audio/mpeg')
        except:
            text_res = (response['result']['fulfillment']['speech'])
            print(text_res)
            tts(text_res, "ES", "response.mp3")
            file = open('response.mp3', 'rb')
            return send_file(file, mimetype='audio/mpeg')
    else:
        return "Disculpa, No entiendo la consulta"


if __name__ == '__main__':
    app.run(debug=True, port=8100)
