from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def fetch_nav_data():
    url = "https://www.amfiindia.com/spages/NAVAll.txt"
    response = requests.get(url)
    return response.text

def parse_nav_data(data):
    nav_dict = {}
    lines = data.splitlines()
    for line in lines[1:]:  # Skip header line
        parts = line.split(';')  # Change from '|' to ';' based on the input format
        if len(parts) > 4:  # Ensure there are enough parts
            fund_name = parts[3].strip()
            nav_value = parts[4].strip()
            nav_dict[fund_name] = nav_value
    return nav_dict


@app.route('/', methods=['GET', 'POST'])
def home():
    nav_value = None
    if request.method == 'POST':
        fund_name = request.form['fund_name']
        data = fetch_nav_data()
        nav_data = parse_nav_data(data)
        nav_value = nav_data.get(fund_name)

    return render_template('index.html', nav_value=nav_value)


if __name__ == '__main__':
    app.run(debug=True, port=5001)

