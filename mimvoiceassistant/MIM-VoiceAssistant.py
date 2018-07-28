
import logging
import time
import os
from threading import Thread, Event
from respeaker import Microphone

import httplib, urllib, json 
import requests 
from xml.etree import ElementTree
from respeaker.bing_speech_api import BingSpeechAPI
from time import gmtime, strftime

# This key is used for the initial Speech to Text conversion only
BING_KEY = 'yourSpeechToTextAPIKey'
os.system('madplay HelloMIMVoiceServiceFemale.mp3')

# Azure IoT Hub Details for Auditing and Reporting 
IoTHubName = 'YourIoTHub'
deviceID = 'YourIoTDeviceID'
# IoT Hub RestAPI Version
iotHubAPIVer = '2018-04-01'
# SAS Token Generated via Azure CLI or Device Explorer
SASToken = 'SharedAccessSignature sr=YourIoTHub.azure-devices.net%2Fdevices%2FYourIoTDeviceID&sig=I%2BBFeaCFNiSnvQe%2FwbUeT4B%2Fg4UWvUzzVRV6NmOjnE1%3D&se=1564028530'
            
def task(quit_event):
    mic = Microphone(quit_event=quit_event)
    bing = BingSpeechAPI(key=BING_KEY)

    while not quit_event.is_set():
        if mic.wakeup('lithnet'):
            print('Wake up')
            os.system('madplay yes-female.mp3')
            data = mic.listen()
            try:
                text = bing.recognize(data)
                if text:
                    print('Converted query from speech: %s' % text)                    
                    os.system('madplay LetmehavealookFemale.mp3')

                    try:
                        # -----------------------------
                        # Search MIM for Object 
                        # -----------------------------
                        params = {}
                        params['query'] = str(text)
                        params['staging'] = "true"
                        headers = {"Content-Type" : "application/x-www-form-urlencoded"}

                        # Connect to server to get the Access Token
                        print ("Connect to Azure Function to get Object from MIM")
                        textresp = httplib.HTTPSConnection("yourAzureFunctionApp.azurewebsites.net")
                        code = {"code" : "yourAzureFunctionKey=="}
                        functioncode = urllib.urlencode(code)
                        textresp.request("POST", "/api/yourAzureFunction?" + functioncode, json.dumps(params), headers)
                        
                        response = textresp.getresponse()
                        data = response.read()
                        print(response.status, response.reason)
                        
                        # Remove CRLF and leading "
                        data = data[:-5]      
                        data = data[1:]                  
                        print('MIM Returned: ' + data)
                        returnedResults = json.loads(data)

                        # -----------------------------
                        # Convert Repsonse to Speech
                        # -----------------------------
                        if data:
                            mimResponse = returnedResults['MIMResponse']
                            tokenurl = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"
                            ttskey = 'yourAzureTextToSpeechAPIKey'
                            params = ""
                            ttstokenheaders = {"Ocp-Apim-Subscription-Key": ttskey}

                            print("Getting AccessToken from westus.tts.speech.microsoft.com for Text to Speech Conversion")

                            resp = requests.post(tokenurl, params=params, headers=ttstokenheaders)
                            token = resp.text
                            accesstoken = token.decode("UTF-8")

                            ttsurl = 'https://westus.tts.speech.microsoft.com/cognitiveservices/v1'

                            ttsheaders = {}
                            ttsheaders['Ocp-Apim-Subscription-Key'] = ttskey
                            ttsheaders['Content-Type'] = "application/ssml+xml"
                            ttsheaders['X-Microsoft-OutputFormat'] = "audio-16khz-32kbitrate-mono-mp3"
                            ttsheaders['User-Agent'] = "MIMText2Speech"
                            ttsheaders['Authorization'] = "Bearer " + accesstoken

                            #<speak version='1.0' xmlns="http://www.w3.org/2001/10/synthesis" xml:lang='en-US'><voice  name='Microsoft Server Speech Text to Speech Voice (en-AU, HayleyRUS)'><prosody volume="+20.00%">Welcome to use Microsoft Cognitive Services Text-to-Speech API.</prosody></voice> </speak>
                            body = ElementTree.Element('speak', version='1.0')
                            body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
                            voice = ElementTree.SubElement(body, 'voice')
                            voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-AU')
                            voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Female')
                            voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-AU, HayleyRUS)')
                            prosody = ElementTree.SubElement(body, 'prosody')
                            prosody.set('volume', '-50.00%')
                            prosody.set('rate', '-50.00%')
                            voice.text = data

                            print("Calling westus.tts.speech.microsoft.com to convert response to audio")
                            audioresp = httplib.HTTPSConnection("westus.tts.speech.microsoft.com")
                            audioresp.request("POST", "/cognitiveservices/v1", ElementTree.tostring(body), ttsheaders)
                        
                            response = audioresp.getresponse()
                            data = response.read()
                            print(response.status, response.reason)

                            file = open("audioout.mp3", "wb")
                            file.write(data)
                            file.close()

                            # Play Response
                            os.system('madplay audioout.mp3')
                                                       
                            # -----------------------------
							# Reporting and Auditing  
							# -----------------------------                            
                            datetimenow = strftime("%m-%d-%Y %H:%M:%S", gmtime())
                            logparams = {}
                            logparams['deviceId'] = "MIMVoice"
                            logparams['messageId'] = str(datetimenow)
                            logparams['messageString'] = "MIMVoice-to-Cloud-" +str(datetimenow)
                            logparams['MIMQuery'] = str(text)
                            logparams['MIMResponse'] = mimResponse
                            logparams['entity'] = returnedResults['fullname']
                            logparams['entitlement'] = returnedResults['entitlement']
                            logparams['date'] = strftime("%m-%d-%Y", gmtime())

                            logheaders = {}
                            logheaders['Authorization'] = SASToken
                            logheaders['Content-Type'] = "application/json"

                            # Send Event to IoT Hub 
                            print ("Sending Event Summary to IoT Hub - " + IoTHubName + ".azure-devices.net from deviceID " + deviceID)
                            logresp = httplib.HTTPSConnection(IoTHubName + ".azure-devices.net")
                            logresp.request("POST", "/devices/" + deviceID + "/messages/events?api-version=" + iotHubAPIVer, json.dumps(logparams), logheaders)
                            logresponse = logresp.getresponse()
                            logdata = logresponse.read()
                            
                            if logdata:
                                print(logresponse.status, logresponse.reason)
                                logdata = logdata[:-5]
                                print("DEBUG:Event Summary send to IoT Hub failed: " + logdata)
                            
                    except Exception as e:
                        print(e.message)
                        
            except Exception as e:
                print(e.message)


def main():
    logging.basicConfig(level=logging.DEBUG)

    quit_event = Event()
    thread = Thread(target=task, args=(quit_event,))
    thread.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('Quit')
            quit_event.set()
            break
    thread.join()

if __name__ == '__main__':
    main()

