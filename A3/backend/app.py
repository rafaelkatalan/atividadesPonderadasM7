from flask import Flask, request, jsonify
import pandas as pd
from pycaret.classification import load_model, predict_model

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def submit():
    try:
        data = request.get_data()
        data = data.decode('utf-8')
        data = jsonify(data)
        print(data)
        
        data = pd.read_json(data, orient='columns')
        print(data)

        # Load the pre-trained model
        model = load_model('./lgbmregressor.pkl')

        # Make predictions
        predictions = predict_model(model, data)

        # Return predictions as JSON response
        return jsonify({'predictions': predictions.tolist()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
