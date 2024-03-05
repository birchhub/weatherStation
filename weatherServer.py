#!/usr/bin/python3

import random
import socket
import json
import sqlite3
import math
from datetime import datetime

class Node:
	def __init__(self, ip, module=None):
		self.ip = ip
		self.module = module

class Measurement:
	def __init__(self, jsonObject):
		print(jsonObject)
		if "temperature" in jsonObject:
			self.temp = jsonObject["temperature"]
		else:
			self.temp = None
		if "humidity" in jsonObject:
			self.humidity = jsonObject["humidity"]
		else:
			self.humidity = None
		self.timestamp = datetime.now()

class PersistenceLayer:
	def __init__(self):
		self.connection = sqlite3.connect('weather.db')

	def writeEntry(self, node, message):
		print(self.connection.total_changes)
		nodeId = self.getNodeId(node)

		sqlCmd = 'insert into measurements(node, timestamp, epoch, temperature, humidity) values(?,?,?,?,?)';
		cursor = self.connection.cursor()
		cursor.execute(sqlCmd, (nodeId, message.timestamp, math.floor(message.timestamp.timestamp()), message.temp, message.humidity))
		self.connection.commit()


	def getNodeId(self, node):
		print(f'get node for {node.ip}')

		# search ID for node
		sqlCmd = "select id from nodes where ip = ?"

		cursor = self.connection.cursor()
		rows = cursor.execute(sqlCmd, (node.ip,)).fetchall()

		if len(rows) == 0:
			# no entry yet, create
			sqlCmd = "insert into nodes(ip,module) values(?,?)"
			cursor.execute(sqlCmd, (node.ip, node.module))
			self.connection.commit()
			return cursor.lastrowid

		return (rows[0][0])

class WeatherServer:
    def processMeasurement(self, msg, ip):
        node = Node(ip)
        measurement = Measurement(json.loads(msg))
        pl.writeEntry(node, measurement)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('', 3141))

        while True:
            message, address = self.server_socket.recvfrom(1024)
            try:
            	self.processMeasurement(message, address[0])
            except Exception as e:
                print(e)

pl = PersistenceLayer()
WeatherServer().start()
