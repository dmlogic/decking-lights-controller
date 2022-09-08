from flask import Flask, render_template

app = Flask(__name__)
ONOFF = 'checked'
RGB = '#32a852'
WHITE = '30'

@app.route('/')
def index():
    return render_template('index.html', on_off=ONOFF, rgb=RGB, white=WHITE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
