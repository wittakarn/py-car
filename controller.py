import os, os.path
import cherrypy
import RPi.GPIO as gpio
import time

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(16, gpio.OUT)
        gpio.setup(11, gpio.OUT)
        gpio.setup(13, gpio.OUT)
        gpio.setup(15, gpio.OUT)
        return open('index.html')

@cherrypy.expose
class ControllerWebService(object):
    def POST(self, command):
        if command == 'forward':
            gpio.output(16, True)
            gpio.output(11, False)
            gpio.output(13, True)
            gpio.output(15, False)
        elif command == 'backward':
            gpio.output(16, False)
            gpio.output(11, True)
            gpio.output(13, False)
            gpio.output(15, True)
        elif command == 'stop':
            gpio.output(16, False)
            gpio.output(11, False)
            gpio.output(13, False)
            gpio.output(15, False)
        elif command == 'left':
            gpio.output(16, False)
            gpio.output(11, False)
            gpio.output(13, True)
            gpio.output(15, False)
        elif command == 'right':
            gpio.output(16, True)
            gpio.output(11, False)
            gpio.output(13, False)
            gpio.output(15, False)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/controller': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    webapp = StringGenerator()
    webapp.controller = ControllerWebService()
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 3000})
    cherrypy.quickstart(webapp, '/', conf)