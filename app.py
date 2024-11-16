from flask import Flask, render_template, request, jsonify, redirect,url_for ,session
from db import fetch_all_coordinates, update_coordinates,find_user_by_name, create_user  
from dotenv import load_dotenv

import os

app = Flask(__name__)  
app.secret_key = "my_secret_key" 

load_dotenv()


@app.route('/')  
def index():  
    
    return render_template('index.html')  

@app.route('/track')  
def track():
   # app.logger.info(type(session)) 
    #app.logger.info(session)
    #flag = 'user_id' not in session
    #app.logger.info(flag)
    #if 'user_id' not in session:  
       # return redirect(url_for('login')) 
    api_key = os.getenv('API')

    return render_template('tracking.html',API_KEY = api_key)  

@app.route('/register', methods=['GET', 'POST'])  
def register():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password']
        #bcrypt.generate_password_hash(request.form['password']).decode('utf-8')  
        create_user(username, password)  # insert user into the database  
        return redirect(url_for('login'))  
    return render_template('register.html') 

@app.route('/login', methods=['GET', 'POST'])  
def login():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password']  
        user = find_user_by_name(username)  
        app.logger.info(user)
        #app.logger.info(f'username and password is {username },{password}')
        if user and user.get('password')==password:  
            session['user_id'] = str(user['_id'])   # Storing user ID in session  
            #app.logger.info(f'user_id while storing in session {username}')
            return redirect(url_for('track'))  
        else:  
            return "Invalid username or password", 401  
    return render_template('login.html')  

@app.route('/update-location', methods=['POST'])  
def update_location():  
    try:
        data = request.get_json()  # Parse the incoming JSON data  
        device_id = data.get('id')  # Get the device ID from the request  
        latitude = data.get('latitude')  
        longitude = data.get('longitude')  
        app.logger.info(f'data is {data}')
        if not device_id or latitude is None or longitude is None:
            return jsonify({'error':'Missing device ID or location Data'}), 400
        update_coordinates(device_id,latitude,longitude)
        return jsonify({"status": "success"}), 200  
    except:
        app.log_exception(f'getting exception in updating location, data is {data}')

@app.route('/get-all-locations',methods = ['GET'])
def get_locations():
    locations = fetch_all_coordinates()
    return locations
if __name__ == '__main__':  
    port = int(os.environ.get('PORT', 5003))
    app.run(debug=True, host = '0.0.0.0', port = port)