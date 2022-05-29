from cgitb import text
from flask import Flask,request, render_template, url_for, jsonify
from flask_wtf import Form 
from wtforms import StringField
import random
import model
app = Flask(__name__)

# placeholder = ['masukkan atau tempelkan pesan disini']   
@app.route('/')
def home():
    # cplace = str(random.choice(placeholder))
    return render_template('index.html', prediction_text="")


@app.route('/predict', methods=['GET','POST'])
def predict():
    # get the description submitted on the web page
    text = request.form.get('description')
    correct_text = ' '.join('<<'+i+'>>'+' %s'%model.correction(i) if model.correction(i) != i else i for i in text.split())
    return render_template('index.html', prediction_text=correct_text)

if __name__ == "__main__":
    app.run(debug=True)