import typing

import numpy as np
from flask import Flask, request, Blueprint, jsonify
import logging
from flask_cors import CORS
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QEventLoop
from PyQt5.QtWidgets import QApplication

# blueprint for socket comms parts of app
from .blockly_routes import bly as blockly_blueprint
from .blockly_routes import setBlocklyPath, setShowStatusSignal, setP
from werkzeug.serving import make_server, WSGIRequestHandler
import threading, webbrowser



from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


print('starting the compile server...')

flask_thread = None
server_ip = ''
device = None


def create_server(showStatusSignal, serverSignal, path, local_ip, dev):
	global flask_thread, server_ip, device
	server_ip = local_ip
	setShowStatusSignal(showStatusSignal)
	setBlocklyPath(path, local_ip)
	device = dev
	setP(dev)
	flask_thread = FlaskThread()
	flask_thread.setShowStatusSignal(showStatusSignal)
	flask_thread.setServerSignal(serverSignal)
	# flask_thread.finished.connect(QApplication.quit)

	# Start the thread
	flask_thread.start()
	return flask_thread



class FlaskThread(QThread):
	finished = pyqtSignal()
	serverSignal = None
	MPSlots = None


	def __init__(self, parent=None):
		super().__init__(parent)
		self.cameraReadySignal = None
		self.coords = None
		self.server = None
		self._stop_flag = False  # Add stop flag


	def setServerSignal(self, sig):
		self.serverSignal = sig
		self.QuietRequestHandler.serverSignal = self.serverSignal

	def setShowStatusSignal(self, sig):
		self.showStatusSignal = sig
		self.QuietRequestHandler.showStatusSignal = self.showStatusSignal


	class QuietRequestHandler(WSGIRequestHandler):
		serverSignal = None
		showStatusSignal = None
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

		def log(self, type, message, *args):
			# Emit the log message using the serverSignal
			if self.showStatusSignal:
				self.showStatusSignal.emit(type+':'+message%args,False)


	def stop(self):
		"""Signal the thread to stop and shutdown the server."""
		self._stop_flag = True
		self.stop_flask_app()
		
	def stop_flask_app(self):
		"""Safely shutdown the Flask server."""
		if hasattr(self, 'server') and self.server:
			if self.server and self.server.is_alive():
				self.server.stop()
				self.server.join()  # Wait for the thread to finish
				print("Flask server stopped.")
			else:
				print("Flask server was not running.")


	def run(self):
		# Run the Flask app in a separate thread
		print('starting the flask app...')
		self.app = Flask(__name__, template_folder='flask_templates', 
						static_folder='static', static_url_path='/')
		
		# Add shutdown route
		@self.app.route('/shutdown')
		def shutdown():
			func = request.environ.get('werkzeug.server.shutdown')
			if func is None:
				raise RuntimeError('Not running with the Werkzeug Server')
			func()
			return 'Server shutting down...'

		try:
			from flasgger import Swagger
			# Define custom names/paths

			swagger_config = {
				"headers": [],
				"specs": [
					{
						"title": 'SEELab Server API',
						"description": 'API docs for the SEELab Server. Many functions are not yet documented.',
						"version": '1.0.0',
						"termsOfService": 'https://csparkresearch.in/seelab3',
						"contact": {
							"name": 'CSPARK Research',
							"url": 'https://csparkresearch.in',
							"email": 'info@csparkresearch.in'
						},                      
						"endpoint": 'seelab_spec',
						"route": '/apidef.json',
						"rule_filter": lambda rule: True,
						"model_filter": lambda tag: True,
						"supportedSubmitMethods": [],  # Disable "Try it out" using this option
					}
				],
				"swagger_ui": True,
				"specs_route": "/apidocs/",
				"tryItOutEnable": False,
				"supportedSubmitMethods": [],
				"swagger_ui_config": {
					"tryItOutEnable": False,
					"supportedSubmitMethods": []
				}
			}

			self.swagger = Swagger(self.app, config=swagger_config)
		except:
			print('flasgger not installed')
		self.app.logger.setLevel(logging.WARNING)
		CORS(self.app)
		
		from .blockly_routes import bly as blockly_blueprint
		self.app.register_blueprint(blockly_blueprint)
		
		try:
			self.server = make_server('0.0.0.0', 8888, self.app, 
									request_handler=self.QuietRequestHandler)
			while not self._stop_flag:
				self.server.handle_request()
		except Exception as e:
			import traceback
			self.serverSignal.emit(traceback.format_exc())
		finally:
			if hasattr(self, 'server') and self.server:
				try:
					self.server.server_close()
				except:
					pass

	def updateCoords(self,c):
		self.coords = c
		#print(c)

