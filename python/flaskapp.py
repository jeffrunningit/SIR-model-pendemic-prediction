from flask import Flask, render_template, jsonify, request
import numpy as np
import sim_latest

stepsPerDay = 10
sim1 = sim_latest.Population(
    infection_radius_m=1,
    infection_probability=0.5,
    infectious_period_day=3,
    N=600,
    max_speed_mpday=1
)

position_history = np.array([])
states_history = np.array([])

# Flask part

app = Flask(__name__)
app.json.sort_keys = False

@app.route('/')
def index():
    return render_template("siminterface.html")
    #return render_template("gptinterface.html")

@app.route('/start', methods=['POST'])
def start():
    """Initialize the simulation"""
    print("Initializing simulation...") # Debugging Log
    params = request.get_json()
    
    global sim1
    sim1 = sim_latest.Population(
        infection_radius_m=params.get('infectionRadius'),
        infection_probability=params.get('infectionProb'),
        infectious_period_day=params.get('infectiousPeriodDay')
    )
    return jsonify({"message": "Simulation initialized"})

@app.route('/data')
def get_data():
    try:
        data = {
            "day": sim1.day,
            "boxsize": sim1.box_size,
            "state_count": sim1.statescount.tolist(),
            "states": sim1.states.tolist(),
            "positions": sim1.positions.tolist(),
        }
        print(f"Sending Data: {data}")  # Debugging Log
        return jsonify(data), 200
    except Exception as e:
        print(f"Error in /data: {str(e)}")  # Print exact error
        return jsonify({"error": str(e)}), 500

@app.route('/step')
def step():
    try:
        stepsPerDay = int(request.args.get('stepsPerDay'))
        sim1.step(stepsPerDay)
        return jsonify({"message": "Stepped"}), 200
    except Exception as e:
        print(f"Error in /step: {str(e)}")  # Print exact error
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=False)
