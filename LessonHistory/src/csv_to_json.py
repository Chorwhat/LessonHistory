import pandas as pd
import json

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
                    float(row['Score']),
                    row['Status'],
                    row['Notes']
                ]
                activities.append(activity_data)

            lesson_object = {
                'FirstName': first_name,
                'LastName': last_name,
                'LessonNumber': int(lesson_number),
                'Activities': activities
            }
            json_data.append(lesson_object)

        return json_data

    except Exception as e:
        print("Error reading CSV file:", e)
        return None

if __name__ == "__main__":
    file_path = "/Users/shing/Downloads/LessonHistory.csv"  # Replace this with the actual path to your CSV file
    json_data = read_csv_and_convert_to_json(file_path)

    if json_data:
        with open("output.json", "w") as output_file:
            json.dump(json_data, output_file, indent=4)
        print("CSV data converted to JSON and saved to output.json")
