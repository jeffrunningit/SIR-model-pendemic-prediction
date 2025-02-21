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
    print("Initializing simulation...")  # Debugging log
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
    #sim1.step(stepsPerDay)
    data = {
        "day" : sim1.day,
        "boxsize" : sim1.box_size,
        "state_count": sim1.statescount.tolist(),
        "states": sim1.states.tolist(),
        "positions": sim1.positions.tolist()
    }
    return jsonify(data)

@app.route('/step')
def step():
    stepsPerDay = int(request.args.get('stepsPerDay'))
    sim1.step(stepsPerDay)
    return jsonify({"message": "Stepped"}), 200

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
