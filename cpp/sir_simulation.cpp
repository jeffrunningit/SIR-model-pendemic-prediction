#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include "dotsmodel.h"

using namespace std;

int main() {
    double infection_radius = 1, infection_probability = 0.5;
    int infection_duration = 10, N = 10000;
    bool animate = false;

    srand(time(nullptr));

	cout << "-------------------------------" << endl;
	cout << "Default parameters:" << endl;
	cout << "Size of the box = 30 x 30" << endl;
	cout << "Infection radius = " << infection_radius << endl;
	cout << "Infection probability = " << infection_probability << endl;
	cout << "Infection duration = " << infection_duration << endl;
	cout << "-------------------------------" << endl;
	cout << "Use default parameters? (Enter/n)" << endl;
	string input;
	getline(cin, input);
	if (input != ""){
		cout << "Enter infection radius: ";
		while (!(cin >> infection_radius)) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "No input provided. Enter again: ";
		}
		cout << "Enter infection probability (0 to 1): ";
		while (!(cin >> infection_probability)) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "No input provided. Enter again: ";
		}
		cout << "Enter infection duration: ";
		while (!(cin >> infection_duration)) {
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "No input provided. Enter again: ";
		}
	};

    ofstream file("results/SIRsimData.csv");
	if (!file) {
        cerr << "Error: Could not open the file!" << endl;
        return 1;
    }
	file << "day,susceptible,infected,recovered\n";

    DotArray population(N);
	int susceptible = N-1, infected = 1, recovered = 0;
	cout << "Day " << 0 << " | Susceptible: " << susceptible
             << " | Infected: " << infected
             << " | Recovered: " << recovered << endl;
	bool ongoing = true;

    for (int day = 1; day < 1000; ++day) { // Simulate until everyone infected has recovered
        population.update(infection_radius, infection_probability, infection_duration);
        
        // Output counts
        susceptible = 0, infected = 0, recovered = 0;
        for (const auto& dot : population.dots) {
            if (dot.state == 0) susceptible++;
            else if (dot.state == 1) infected++;
            else recovered++;
        }
		
        cout << "Day " << day << " | Susceptible: " << susceptible
             << " | Infected: " << infected
             << " | Recovered: " << recovered << endl;

		file << day << "," << susceptible << "," << infected << "," << recovered << endl;

		if (infected == 0){
			ongoing = false;
			break;
		}
    }

	file.close();

	cout << "Simulation finished!" << endl;
	cout << "Susceptible: " << susceptible
             << " | Infected: " << infected
             << " | Recovered: " << recovered << endl;

	if (ongoing){
		cout << "Pandemic still ongoing after 1000 days. (Infected > 0)" << endl;
	}
	cout << float((infected + recovered)) / N * 100 << "% of the population has been infected." << endl;

    return 0;
}