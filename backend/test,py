import requests
import json

# Define the base URL for the Flask application
base_url = 'http://localhost:5000'

def test_get_temps():
    url = f'{base_url}/get_temps'
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert 'temperature' in data
    assert 'humidity' in data
    assert 'wind_speed' in data
    assert 'percipitation' in data
    assert 'sunchine' in data

def test_generate_report():
    url = f'{base_url}/generate_report'
    payload = {
        'user_id': 'user123',
        'report_name': 'tomato_report',
        'crop_type': 'tomato',
        'temperature': '25',
        'humidity': '60',
        'wind_speed': '5',
        'percipitation': '10',
        'sunchine': '8',
        'growth_stage': 'flowering',
        'irregation_method': 'drip',
        'start_date': '2023-10-01'
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 'report_name' in data
    assert 'report_id' in data
    assert 'start_date' in data
    assert 'report' in data
    return data['report_id']

def test_get_report(report_id):
    url = f'{base_url}/get_report/{report_id}'
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert 'report_id' in data
    assert 'report_name' in data
    assert 'start_date' in data
    assert 'report' in data

def test_get_report_list():
    url = f'{base_url}/get_report_list'
    payload = {'user_id': 'user123'}
    response = requests.get(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 'reports' in data
    for report in data['reports']:
        assert 'report_id' in report
        assert 'report_name' in report
        assert 'start_date' in report
        assert 'report' in report

if __name__ == '__main__':
    test_get_temps()
    report_id = test_generate_report()
    test_get_report(report_id)
    test_get_report_list()
    print("All tests passed!")