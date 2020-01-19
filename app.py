import sumTwoNumbers
import os
from flask import Flask, request, redirect, jsonify
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
#for split image
import cv2
import numpy as np
import sys
import shutil


app = Flask(__name__)
api = Api(app)


ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = "uploads"
FILE_NAME = ""
VALUE=""

##file upload started
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		FILE_NAME = filename
		file.save(os.path.join(UPLOAD_FOLDER, filename))
		#resp = jsonify({'message' : 'File successfully uploaded'})
		#resp.status_code = 201
		os.system("python splitit.py uploads/"+FILE_NAME)
		extractDigit("outs")
		global VALUE
		VALUE = VALUE.replace("<< ","")
		VALUE = VALUE.replace("\n","")
		resp = jsonify({'message' : 'File successfully uploaded:'+VALUE})
		resp.status_code = 201
		cleanFolder(UPLOAD_FOLDER)
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp
##file upload ended


def cleanFolder(folder):
    shutil.rmtree(folder)
    shutil.rmtree('outs', ignore_errors=True)
    os.mkdir(UPLOAD_FOLDER)
    os.mkdir('outs')
    global VALUE
    VALUE=""

    
def extractDigit(folderPath):
    global VALUE
    for filename in os.listdir(folderPath):
        if(filename.endswith(".jpg")):
            filename="outs/"+filename
            #VALUE = os.system("python classify.py "+filename)
            VALUE = VALUE + os.popen("python classify.py "+filename).read()
            #print('val:'+VALUE)
        else:
           continue

class sumNumbers(Resource):
    def get(self, first_number, second_number):
        return {'data': sumTwoNumbers.sumTwo(first_number,second_number)}

api.add_resource(sumNumbers, '/sumtwonumbers/<first_number>/<second_number>')





if __name__ == '__main__':
     app.run()
