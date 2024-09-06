from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_cors import CORS
import json
import os
import random
import string
import sqlite3
import requests
from llm_utlils import get_llm_response, get_dataset
from weather import get_weather_data

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})



@app.route('/get_temps/<city>', methods=['GET'])
def get_temps(city):

    weather_data = get_weather_data(city)
    print(weather_data)
    return jsonify(weather_data)
    # return jsonify({'temperature': 25, 
    #                 'humidity': 50,
    #                 'wind_speed': 10,
    #                 'percipitation': 0.1,
    #                 'sunchine': 'sunny'
    #                 })


@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json

    user_id = data['user_id']
    report_name = data['report_name']

    crop_type = data['crop_type']
    temperature = str(data['temperature']) + '°C'
    humidity = str(data['humidity']) + '%'
    wind_speed = str(data['wind_speed']) + 'km/h'
    percipitation = str(data['percipitation']) + 'mm'

    growth_stage = data['growth_stage']
    irregation_method = data['irregation_method']

    start_date = data['start_date']

    user_weather_data = json.dumps({
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'percipitation': percipitation,
    })

    report_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    dataset = get_dataset()

    prompt = f"""Generate a report for {crop_type} crop based on the DOCUMENT with the following conditions: \n"
Temperature: {temperature}
Humidity: {humidity}
Wind Speed: {wind_speed}
Percipitation: {percipitation}
Growth Stage: {growth_stage}
Irregation Method: {irregation_method}


The output should be a json object with the following fields:
- Explanation: a thourough explanation (300 words) of how the values were calculated (str)
- irregation_frequency: how often the crop should be irregated in days (int)
- irregation_amount: how much water should be used for irregation in every square meter (mm) (float)

Rules:
- Only output the json object, nothing else.
- No need for an introduction or any other text including "```".
- Only respond based on the DOCUMENT, do not use any other information.
- If the crop type is not in the DOCUMENT, just return "None". Nothing else.
- Don't output anything else, just the json object. No explanations needed.
- Always start with the `explanation` key in the json object.
- Make sure not to write more 300 words in the explanation.

DOCUMENT:
{dataset}
"""
    print(prompt)
    
    text_response = get_llm_response(prompt, max_tokens=3000)
    # text_response = '{"explanation": "The irregation frequency is 2 days and the irregation amount is 10mm", "irregation_frequency": 2, "irregation_amount": 10.0}'
    print(text_response)

    response = json.loads(text_response)

    conn = sqlite3.connect('reports.db')
    conn.execute(f"INSERT INTO reports (report_id, user_id, report_name, start_date, report, weather_data) VALUES (?, ?, ?, ?, ?, ?)", (report_id, user_id, report_name, start_date, text_response, user_weather_data))
    conn.commit()
    conn.close()

    return jsonify({
        'report_name': report_name,
        'report_id': report_id,
        'start_date': start_date,
        'report': response
    })
  

@app.route('/get_report/<report_id>', methods=['GET'])
def get_report(report_id):
    print(report_id)
    conn = sqlite3.connect('reports.db')
    report = conn.execute(f"SELECT report_id, report_name, start_date, report, weather_data FROM reports WHERE report_id = '{report_id}'").fetchone()

    print(report[0], report[1], report[2], report[3])
    return jsonify({
        'report_id': report[0],
        'report_name': report[1],
        'start_date': report[2],
        'report': json.loads(report[3]),
        'weather_data': json.loads(report[4])
    })

@app.route('/get_report_list', methods=['POST'])
def get_report_list():
    data = request.json
    user_id = data['user_id']

    conn = sqlite3.connect('reports.db')

    # Use parameterized query to prevent SQL injection
    cursor = conn.execute("SELECT report_id, report_name, start_date, report FROM reports WHERE user_id = ?", (user_id,))
    reports = cursor.fetchall()
    
    return jsonify({
        'reports': [{'report_id': report[0], 'report_name': report[1], 'start_date': report[2], 'report': json.loads(report[3])} for report in reports]
    })



def create_table():
    if os.path.exists('reports.db'):
        return
    
    conn = sqlite3.connect('reports.db')
    conn.execute('''CREATE TABLE reports
             (report_id TEXT PRIMARY KEY,
             user_id TEXT NOT NULL,
             report_name TEXT NOT NULL,
             start_date TEXT NOT NULL,
             report TEXT NOT NULL,
             weather_data TEXT NOT NULL);''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
    app.run(debug=True)