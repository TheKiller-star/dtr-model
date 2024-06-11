from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Memuat model yang telah dilatih
with open('DTRModel.pkl', 'rb') as f:
    model = pickle.load(f)

def format_rupiah(value):
    return f"Rp {value:,.2f}".replace(',', '.').replace('.', ',', 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    features = [
        float(data['lebar_bangunan']), 
        float(data['lebar_tanah']), 
        float(data['jumlah_kamar_tidur']), 
        float(data['jumlah_kamar_mandi']), 
        float(data['jumlah_kapasitas_mobil_dan_garasi'])
    ]
    prediction = model.predict([features])[0]
    formatted_prediction = format_rupiah(prediction)
    
    result = {
        'Lebar Bangunan': data['lebar_bangunan'],
        'Lebar Tanah': data['lebar_tanah'],
        'Jumlah Kamar Tidur': data['jumlah_kamar_tidur'],
        'Jumlah Kamar Mandi': data['jumlah_kamar_mandi'],
        'Jumlah Kapasitas Mobil dan Garasi': data['jumlah_kapasitas_mobil_dan_garasi'],
        'Prediction': formatted_prediction
    }
    
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
