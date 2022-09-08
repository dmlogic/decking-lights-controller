#! /usr/bin/python3

from flask import Flask, request, jsonify, render_template
from os.path import exists
import json
import pigpio

app = Flask(__name__)
pi = pigpio.pi()

# Default light values
ONOFF = ''
RGB = '#000000'
WHITE = '128'
DATAPATH = 'data.json'

if exists(DATAPATH):
    with open(DATAPATH, 'r') as f:
        try:
            savedData = json.load(f);
            WHITE = savedData["white"]
            RGB =savedData["rgb"]
            ONOFF = savedData["onoff"]
        except:
            print("could not load valid data")


def setLightValues(red, green, blue, white):
    # Commented for non-pi testing. Bring back to make it do stuff
    # pi.set_PWM_dutycycle(24, red)
    # pi.set_PWM_dutycycle(20, blue)
    # pi.set_PWM_dutycycle(25, green)
    # pi.set_PWM_dutycycle(18, white)
    print ("set lights")

@app.route('/')
def index():
    return render_template('index.html', on_off=ONOFF, rgb=RGB, white=WHITE)

@app.route('/update', methods=['POST'])
def update():
    # Turn it all off
    if request.form.get('onoff') == 'off':
        ONOFF=''
        setLightValues(0, 0, 0, 0)

    # Set on values as per data supplied
    else:
        ONOFF='checked'
        WHITE = int(request.form.get('white'))
        RGB = request.form.get('rgb')

        rgbValues = tuple(int(RGB.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        setLightValues(rgbValues[0], rgbValues[1], rgbValues[2], WHITE)

    # Store data for persistence
    updateData = {"onoff": ONOFF, "rgb": RGB, "white": WHITE}
    with open(DATAPATH, 'w') as f:
        json.dump(updateData, f)

    return jsonify(updateData);

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
