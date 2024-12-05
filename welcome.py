import os
from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

# Correctly formatted paths to batch files using double backslashes or forward slashes
powersave_script = r'cmd.exe /c "power_saver_mode.bat"'
normal_mode_script = r'cmd.exe /c "normal_mode.bat"'
jupyter_command = r'jupyter lab'
jupyter_shutdown = r'pkill -f jupyter'

@app.route('/')
def home():
    # Serve the HTML page when accessing the root URL
    return render_template('index.html')  # This assumes 'index.html' is in the 'templates' folder

@app.route('/command/<action>', methods=['GET'])
def execute_command(action):
    if action == 'powersave':
        result = subprocess.run([powersave_script], shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify(message="Power Saver Mode Activated!")
        else:
            return jsonify(message="Error: " + result.stderr)
    
    elif action == 'normal':
        result = subprocess.run([normal_mode_script], shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify(message="Normal Power Mode Activated!")
        else:
            return jsonify(message="Error: " + result.stderr)
    
    elif action == 'jupyter':
        # Start Jupyter Server and then switch to normal mode
        subprocess.Popen([jupyter_command], shell=True)
        result = subprocess.run([normal_mode_script], shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify(message="Jupyter Server Started and Normal Mode Activated!")
        else:
            return jsonify(message="Error: " + result.stderr)
        
    elif action == 'shutdown':
        # Shutdown jupyter lab and revert it back to Power saver mode
        subprocess.Popen([jupyter_shutdown], shell=True)
        result = subprocess.run([powersave_script], shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify(message="Jupyter Server Shutdown and Power saver Mode Activated!")
        else:
            return jsonify(message="Error: " + result.stderr)
    
    else:
        return jsonify(message="Invalid Command!")

if __name__ == '__main__':
    subprocess.run([powersave_script], shell=True, capture_output=True, text=True)
    app.run() #debug=True)  # Run Flask app in debug mode for easier troubleshooting
