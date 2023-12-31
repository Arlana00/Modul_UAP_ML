import time
from unittest import result
from flask import Flask, render_template, request
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

app = Flask(__name__)

dic = {0: 'paper', 1: 'rock', 2: 'scissors'}

model = load_model('model.h5')

model.make_predict_function()

def predict_label(img_path):
	start_time = time.time()
	i = load_img(img_path, target_size=(224,224))
	i = img_to_array(i)/255.0
	i = i.reshape(1, 224,224,3)
	p = model.predict(i)
	finish_time = time.time()
	prediction_time = finish_time - start_time
	index = np.argmax(p, axis=-1)
	return dic[index[0]], prediction_time

# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		prediction, prediction_time  = predict_label(img_path)
		
		
	return render_template("index.html", prediction = prediction, prediction_time=prediction_time,img_path = img_path)


if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)
