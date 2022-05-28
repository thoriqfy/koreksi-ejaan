from cgitb import text
from flask import Flask,request, render_template, url_for, jsonify
import model
app = Flask(__name__)

# @app.route('/')
# def my_form():
#     return render_template('index.html')

# def get_correction():
#     text = request.args.get("word", default=None)
#     correct_text = model.correction(text)
#     return f"{text} => {correct_text}"
# @app.route('/', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     correct_text = model.correction(text)
#     return correct_text

# if __name__ == "__main__":
#     app.run(debug=True)
    


# what html should be loaded as the home page when the app loads?
@app.route('/')
def home():
    return render_template('index.html', prediction_text="")

# define the logic for reading the inputs from the WEB PAGE, 
# running the model, and displaying the prediction
@app.route('/predict', methods=['GET','POST'])
def predict():
    # get the description submitted on the web page
    text = request.form.get('description')
    correct_text = ' '.join('<<'+i+'>>'+' %s'%model.correction(i) if model.correction(i) != i else i for i in text.split())
    return render_template('index.html', prediction_text=correct_text)
    #return 'Description entered: {}'.format(a_description)

#@app.route('/prediction', methods=['GET', 'POST'])
#def prediction():
#    if request.method == 'POST':
#        prediction_data = request.json
#        print(prediction_data)
#    return jsonify({'result': prediction_data})

# boilerplate flask app code
if __name__ == "__main__":
    app.run(debug=True)