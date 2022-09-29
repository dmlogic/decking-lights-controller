# Decking lights controller

A Python Flask App for controlling RGBW strip lights via a Raspberry PI GPIO interface.

Inspired by the [project by naztronaut](https://github.com/naztronaut/RaspberryPi-RGBW-Control).

The hardware requirements are identical so please follow that guide for all the GPIO and Mosfet work.

This software is intentionally lean. The only dependency is Boostrap from a CDN, and that could easily go away with a little CSS work.

For a private home environment, run `nohup ./app.py > /dev/null &` on startup. For higher usage or less trusted environments, see options for [deploying Flask to production](https://flask.palletsprojects.com/en/2.2.x/deploying/). Gunicorn looks like a nice, low-resource option

