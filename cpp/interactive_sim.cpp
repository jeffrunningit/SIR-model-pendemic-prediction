#include <iostream>
#include <iomanip>
#include <vector>
#include <limits>

using namespace std;

struct SimulationParams {
    double population;
    double initialInfected;
    double initialRecovered;
    double beta;    // Transmission rate
    double gamma;   // Recovery rate
    double dt;      // Time step (in days)
    int days;       // Total simulation duration (in days)
};

struct SIRResult {
    std::vector<double> time;
    std::vector<double> susceptible;
    std::vector<double> infected;
    std::vector<double> recovered;
};

/// Runs the SIR simulation using Euler integration
SIRResult runSimulation(const SimulationParams& params) {
    int steps = static_cast<int>(params.days / params.dt);
    SIRResult result;
    result.time.resize(steps + 1);
    result.susceptible.resize(steps + 1);
    result.infected.resize(steps + 1);
    result.recovered.resize(steps + 1);

    // Initial conditions
    double S0 = params.population - params.initialInfected - params.initialRecovered;
    result.time[0] = 0;
    result.susceptible[0] = S0;
    result.infected[0] = params.initialInfected;
    result.recovered[0] = params.initialRecovered;

    // Euler integration loop
    for (int i = 0; i < steps; i++) {
        double currentS = result.susceptible[i];
        double currentI = result.infected[i];
        double currentR = result.recovered[i];

        // SIR model equations
        double dS = -params.beta * currentS * currentI / params.population;
        double dI = params.beta * currentS * currentI / params.population - params.gamma * currentI;
        double dR = params.gamma * currentI;

        result.susceptible[i + 1] = currentS + dS * params.dt;
        result.infected[i + 1]    = currentI + dI * params.dt;
        result.recovered[i + 1]   = currentR + dR * params.dt;
        result.time[i + 1] = result.time[i] + params.dt;
    }

    return result;
}

/// Displays simulation results in a table format
void displayResults(const SIRResult& result) {
    cout << "\nTime\tSusceptible\tInfected\tRecovered\n";
    cout << "-------------------------------------------------------\n";
    cout << fixed << setprecision(2);
    for (size_t i = 0; i < result.time.size(); i++) {
        cout << result.time[i] << "\t" 
             << result.susceptible[i] << "\t\t" 
             << result.infected[i] << "\t\t" 
             << result.recovered[i] << "\n";
    }
}

/// Clears any invalid input from the stream
void clearInput() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

int main() {
    SimulationParams params = {0};
    char choice;
    bool exit = false;

    while (!exit) {
        cout << "\n--- SIR Model Simulation ---\n";
        cout << "1. Set simulation parameters\n";
        cout << "2. Run simulation\n";
        cout << "3. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;
        if (!cin) {
            clearInput();
            continue;
        }

        switch (choice) {
            case '1': {
                cout << "\nEnter total population (N): ";
                cin >> params.population;
                cout << "Enter initial number of infected individuals (I0): ";
                cin >> params.initialInfected;
                cout << "Enter initial number of recovered individuals (R0): ";
                cin >> params.initialRecovered;
                cout << "Enter transmission rate (beta): ";
                cin >> params.beta;
                cout << "Enter recovery rate (gamma): ";
                cin >> params.gamma;
                cout << "Enter simulation duration (days): ";
                cin >> params.days;
                cout << "Enter time step (dt) in days (e.g., 0.1): ";
                cin >> params.dt;
                break;
            }
            case '2': {
                if (params.population <= 0 || params.dt <= 0 || params.days <= 0) {
                    cout << "Please set valid parameters first (option 1).\n";
                    break;
                }
                SIRResult result = runSimulation(params);
                displayResults(result);
                break;
            }
            case '3':
                exit = true;
                break;
            default:
                cout << "Invalid choice, please try again.\n";
        }
    }
    cout << "Exiting simulation. Goodbye!\n";
    return 0;
}