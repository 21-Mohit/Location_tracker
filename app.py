from flask import Flask, render_template, request, jsonify  
from db import  update_coordinates 

app = Flask(__name__)  
app.secret_key = "my_secret_key" 

@app.route('/')  
def index():  
    return render_template('index.html')  

@app.route('/track')  
def track():  
    return render_template('tracking.html')  

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

if __name__ == '__main__':  
    app.run(debug=True)