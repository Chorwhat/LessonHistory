from flask import Flask, request, jsonify
import os
import json
import numpy as np
from werkzeug.utils import secure_filename
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

def read_csv_and_convert_to_json(file_path):
    try:
        df = pd.read_csv(file_path)

        # Handle null or NaN values for Score and Notes
        df['Score'].fillna(0, inplace=True)
        df['Notes'].fillna('No Notes', inplace=True)

        # Group activities for each lesson
        grouped_data = df.groupby(['FirstName', 'LastName', 'LessonNumber'])

        json_data = []
        for (first_name, last_name, lesson_number), group in grouped_data:
            activities = []
            for _, row in group.iterrows():
                activity_data = [
                    row['Info_Name'],
                    float(row['Score']),  # Convert Score to float
                    row['Status'],
                    row['Notes']
                ]
                activities.append(activity_data)

            lesson_object = {
                'FirstName': first_name,
                'LastName': last_name,
                'LessonNumber': int(lesson_number),  # Convert LessonNumber to integer
                'Activities': activities
            }
            json_data.append(lesson_object)

        return json_data

    except Exception as e:
        print("Error reading CSV file:", e)
        return None

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
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            json_data = read_csv_and_convert_to_json(file_path)

            if json_data:
                with open('output.json', "w") as output_file:
                    json.dump(json_data, output_file, indent=4)
                return jsonify({'message': 'Render completed successfully'}), 200
            else:
                return jsonify({'error': 'Error processing CSV file'}), 500
        else:
            return jsonify({'error': 'Invalid file type'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/output.json', methods=['GET'])
def serve_json_data():
    try:
        json_data = None

        # Load the JSON data from the generated filename (filename + ".json")
        with open(f"output.json", "r") as json_file:
            json_data = json.load(json_file)

        return jsonify(json_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
