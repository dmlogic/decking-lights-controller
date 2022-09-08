from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)
ONOFF = 'checked'
RGB = '#32a852'
WHITE = '30'

def setLightValues(red, green, blue, white):
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
    updateData = {"onoff": ONOFF, "rgb": RGB, "white": WHITE, "rgb": rgbValues[0]}
    with open('data.json', 'w') as f:
        json.dump(updateData, f)

    return jsonify(updateData);

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
