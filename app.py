from flask import Flask, render_template, request
import pandas as pd
import json
import os
from datetime import datetime

app = Flask(__name__)

# Load CSV data
DATA_FILE = 'disease_data.csv'
df = pd.read_csv(DATA_FILE)

# Create history file if it doesn't exist
HISTORY_FILE = 'history.json'
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'w') as f:
        json.dump([], f)

# Diagnosis function
def diagnose(symptoms_input):
    symptoms = [s.strip().lower() for s in symptoms_input.split(',')]
    for index, row in df.iterrows():
        row_symptoms = [str(row['symptom1']).lower(), str(row['symptom2']).lower(), str(row['symptom3']).lower()]
        match_count = sum([s in row_symptoms for s in symptoms])
        if match_count >= 2:
            return f"{row['disease']} - {row.get('diagnosis_info', 'No additional info available.')}"
    return "No matching disease found. Please check your symptoms."

# Save to history
def save_history(symptoms, result):
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symptoms": symptoms,
        "result": result
    }
    history.append(entry)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        symptoms = request.form['symptoms']
        result = diagnose(symptoms)
        save_history(symptoms, result)
    
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
        
    return render_template('project.html', result=result, history=history)


# History route (optional standalone page)
@app.route('/history')
def view_history():
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
