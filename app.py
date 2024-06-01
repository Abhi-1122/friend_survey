from flask import Flask, render_template, request, redirect, url_for
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

questions = ["Pulls the most","Pulls the least","Most Delusional","Funniest","Most likely to go to jail","Mom of the group"
             ,"Red Flag","Green Flag","Most likely to get married first","Nicest","Who's dying first in a zombie apocalypse",
             "Most likely to be a parent first"]

# Your IPStack or IPinfo API key
API_KEY = 'a6be5f64e10740'

def get_geolocation(ip):
    url = f'https://ipinfo.io/{ip}?token={API_KEY}'
    print(url)
    response = requests.get(url)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return None

def check_location(user_ip,location_info):
    with open('static/survey_results.json', 'r') as file:
        for line in file:
            data = json.loads(line)
            if data['user_ip'] == user_ip:
                return False
            elif data['location']['city'] == location_info['city'] and data['location']['postal'] == location_info['postal']:
                return False
            elif data['location']['loc'] == location_info['loc']:
                return False
    return True

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        user_ip = request.remote_addr
        location_info = get_geolocation(user_ip)
        # if check_location(user_ip,location_info) is False:
        #     return "You are not allowed to take the survey."
        # Retrieve form data
        data = {}
        for i in range(1, 13):
            question_key = f'question{i}'
            selected_option = request.form.get(question_key)
            data[question_key] = selected_option

        # Get the user's IP address
        
        data['user_ip'] = user_ip

        # Get the user's geolocation
        if location_info:
            data['location'] = {
                'city': location_info.get('city'),
                'region': location_info.get('region'),
                'loc': location_info.get('loc'),
                'postal': location_info.get('postal')
            }

        # Convert data to JSON and store in a file
        with open('static/survey_results.json', 'a') as json_file:
            json_file.write(json.dumps(data) + "\n")

        return redirect(url_for('thank_you'))
    
    return render_template('index.html')

@app.route('/thank_you')
def thank_you():
    return "Thank you for your submission!"

@app.route('/admin',methods=['GET','POST'])
def admin_check():
    if request.method=='POST':
        password=request.form['password']
        username=request.form['username']
        if username=='sheky' and password=='sheky':
            return redirect(url_for('x8r2eGsuu09BLhOKKsZsW9XXyFW5HCdL'))

    return render_template('login.html')

@app.route('/x8r2eGsuu09BLhOKKsZsW9XXyFW5HCdL',methods=['GET','POST'])
def x8r2eGsuu09BLhOKKsZsW9XXyFW5HCdL():
    num=0
    with open('static/survey_results.json', 'r') as file:
        for line in file:
            num+=1
    if num==0:
        return render_template('admin.html',num=0)
    for i in range(1, 13):
        generate_pie_chart(i)
    return render_template('admin.html',num=num)

@app.route('/delete',methods=['GET'])
def delete():
    os.remove('static/survey_results.json')
    for i in range(1,13):
        os.remove(f'static/pie_chart{i}.png')
    f = open('static/survey_results.json', "x")
    return redirect(url_for('x8r2eGsuu09BLhOKKsZsW9XXyFW5HCdL'))

def generate_pie_chart(question_number):
    # Read data from survey_results.json
    with open('static/survey_results.json', 'r') as file:
        data = [json.loads(line) for line in file]

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Filter data for the specified question number
    question_key = f'question{question_number}'
    question_data = df[question_key].dropna()

    # Count occurrences of each option
    option_counts = question_data.value_counts()

    # Generate pie chart
    plt.figure(figsize=(6,5))
    plt.title(questions[question_number-1])
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Create legend with option labels and counts
    

    # Get lists of option names and counts
    explod=[0.1]
    option_names = option_counts.index.tolist()
    counts_list = option_counts.values.tolist()
    explod+=[0]*(len(option_names)-1)
    plt.pie(counts_list, autopct='%1.1f%%', startangle=140,explode=explod)
    legend_labels = [f'{option}: {count}' for option, count in zip(option_names, counts_list)]
    plt.legend(labels=legend_labels, loc='upper left', fontsize='small')
    plt.savefig(f'static/pie_chart{question_number}.png')

if __name__ == '__main__':
    app.run(debug=True)
