import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def rehome():
    return render_template('home.html')

@app.route('/Crop_recommender')
def crop():
    return render_template('Crop_recommender.html')

@app.route('/fertiliser')
def fertiliser():
    return render_template('fertiliser.html')

@app.route('/health')
def health():
    return render_template('health.html')

@app.route('/Recommend',methods=['POST'])
def recommend():
    model = pickle.load(open('model.pkl', 'rb'))
    if request.method == 'POST':
        N = int(request.form['N'])
        P = int(request.form['P'])
        K = int(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        final_features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = model.predict(final_features)
        output = prediction[0]
        return render_template('Crop_recommender.html', prediction_text=' {}'.format(output))
    model.close()

@app.route('/Suggest',methods=['POST'])
def suggest():
    if request.method == 'POST':
        Crop = str(request.form['Crop'])
        N = int(request.form['N'])
        P = int(request.form['P'])
        K = int(request.form['K'])
        
        df = pd.read_csv('Data/fertilizer.csv')
        
        nr = df[df['Crop'] == Crop]['N'].iloc[0]
        pr = df[df['Crop'] == Crop]['P'].iloc[0]
        kr = df[df['Crop'] == Crop]['K'].iloc[0]

        n = nr - N
        p = pr - P
        k = kr - K

        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]
        if max_value == "N":
            if n < 0:
                output = 'High in Nitrogen'
            else:
                output = "Low in Nitrogen"
        elif max_value == "P":
            if p < 0:
                output = 'High in Phosphorus'
            else:
                output = "Low in Phosphorus"
        else:
            if k < 0:
                output = 'High in Potassium'
            else:
                output = "Low in Potassium"
                
        return render_template('fertiliser.html', prediction_text=' {}'.format(output))


@app.route('/Predict',methods=['POST'])
def predict():
    model1 = pickle.load(open('model1.pkl', 'rb'))
    if request.method == 'POST':
       Estimated_Insects_Count = int(request.form['Estimated_Insects_Count'])
       Crop_Type = int(request.form['Crop_Type'])
       Soil_Type = int(request.form['Soil_Type'])
       Pesticide_Use_Category = int(request.form['Pesticide_Use_Category'])
       Number_Doses_Week = int(request.form['Number_Doses_Week'])
       Number_Weeks_Used = int(request.form['Number_Weeks_Used'])
       Number_Weeks_Quit = int(request.form['Number_Weeks_Quit'])
       Season = int(request.form['Season'])
       
       final_features = np.array([[Estimated_Insects_Count,Crop_Type,Soil_Type,Pesticide_Use_Category,
       Number_Doses_Week,Number_Weeks_Used,Number_Weeks_Quit,Season]])
       prediction = model1.predict(final_features)
       output = prediction[0]

       if output== 0:
           output = "None"
       elif output == 1:
           output = "Damage due to other Cause"
       else:
           output = "Damage due to Pesticides"
         
       return render_template('health.html', prediction_text=' {}'.format(output))
    model1.close()


# def predict_api():
#     '''
#     For direct API calls through request
#     '''
#     data = request.get_json(force =True)
#     prediction = model.predict([np.array(list(data.values()))])

#     output = prediction[0]
#     return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True) 