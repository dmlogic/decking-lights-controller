#! /usr/bin/python3

from flask import Flask, request, jsonify, render_template
from os.path import exists
import json
import pigpio

app = Flask(__name__)
pi = pigpio.pi()

# Default light values
ONOFF = ''
POSTS = 0
RGB = '#000000'
DATAPATH = 'data.json'

def isGrey(string):
    chars = list(string.lstrip('#'))
    return (chars[0]+chars[1]) == (chars[2]+chars[3])  == (chars[4]+chars[5])

def setLedValues(red, green, blue, white):
    # Commented for non-pi testing. Bring back to make it do stuff
    if(white):
        print ("set white to ", white)
        # pi.set_PWM_dutycycle(24, 0)
        # pi.set_PWM_dutycycle(20, 0)
        # pi.set_PWM_dutycycle(25, 0)
        # pi.set_PWM_dutycycle(18, white)
    else:
        print ("set rgb ", red, green, blue)
        # pi.set_PWM_dutycycle(24, red)
        # pi.set_PWM_dutycycle(20, blue)
        # pi.set_PWM_dutycycle(25, green)
        # pi.set_PWM_dutycycle(18, 0)

def controlPosts(updateValue):
    GPIOVALUE = 0 if updateValue == 'checked' else 1
    print ("set posts GPIO to ", GPIOVALUE)
    # pi.write(16, GPIOVALUE)

def persistStatus(updateData):
    with open(DATAPATH, 'w') as f:
        json.dump(updateData, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    global RGB, ONOFF, POSTS

    # Deal with posts circuit first
    POSTS = request.form.get('onoffPosts')
    controlPosts(POSTS)

    # Turn LED circuit off
    if request.form.get('onoff') == 'off':
        ONOFF=''
        setLedValues(0, 0, 0, 0)

    # Set LED values as per data supplied
    else:
        ONOFF='checked'
        RGB = request.form.get('rgb')
        rgbValues = tuple(int(RGB.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        if(isGrey(RGB)):
            setLedValues(0, 0, 0, rgbValues[0])
        else:
            setLedValues(rgbValues[0], rgbValues[1], rgbValues[2], 0)

    # Store data for persistence
    updateData = {"onoff": ONOFF, "rgb": RGB, "posts": POSTS}
    persistStatus(updateData)
    return updateData

@app.route('/status', methods=['GET'])
def status():
    fallbackData = {"onoff": ONOFF, "rgb": RGB, "posts": POSTS, "error": "no data"}
    if exists(DATAPATH):
        with open(DATAPATH, 'r') as f:
            try:
                return json.load(f);
            except:
                return fallbackData

    return fallbackData

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
