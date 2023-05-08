from flask import Flask, render_template, jsonify, request
import requests
from gpiozero import DistanceSensor
import time
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

distance = 0.3 # 기본 값
# 초음파 센서로 설정한 거리 안에 들어오면 이를 감지
def ultrasonic(distance):
	sonic = DistanceSensor(echo=14, trigger=4)
	sonic.threshold_distance = distance

	if(sonic.wait_for_in_range()):
		return userIn(sonic)
	else:
		print("그외")
		return userOut(sonic)

def userIn(sonic):
	print("in ", sonic.distance*100," cm")
	return True
def userOut(sonic):
	print("out ", sonic.distance*100," cm")
	return False

app.route("/")
def home():
	return 'ok'

# 유저 거리 감지
@app.route("/move")
def sonic():
	global distance
	move = ultrasonic(distance)
	print(move)
	if move:
		data = {'result':'user In'}
		return  jsonify(data)
	else:
		data = {'result':'user Out'}
		return jsonify(data)

# 거리 셋팅
@app.route("/set_distance")
def set_distance():
	global distance
	arg = request.args.get('value')
	if arg!=None:
		distance = float(arg)
	print(distance)
	return str(distance)

@app.route("/test")
def test():
	return "flask ok"

if __name__=='__main__':
	app.run(host='0.0.0.0')

