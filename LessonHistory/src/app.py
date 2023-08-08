from flask import Flask, request, jsonify, send_file, current_app
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from csv_to_json import read_csv_and_convert_to_json

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

@app.route('/api/render', methods=['POST'])
def render():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            json_data = read_csv_and_convert_to_json(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if json_data:
                # Save output.json one level higher than the 'uploads' folder
                output_file_path = os.path.join(current_app.root_path, 'output.json')
                with open(output_file_path, "w") as output_file:
                    json.dump(json_data, output_file, indent=4)

                return jsonify({'message': 'Render completed successfully'})
            else:
                return jsonify({'error': 'Error processing CSV file'}), 500
        else:
            return jsonify({'error': 'Invalid file type'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/output.json')
def get_output_json():
    try:
        output_file_path = os.path.join(current_app.root_path, 'output.json')
        return send_file(output_file_path, mimetype='application/json')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
