#include <cmath>
#include <random>
#include <vector>
#include <iostream>

#define PI 3.141592
#define BOXSIZE 30
#define DOTVEL 0.05

using namespace std;

static double getRandomDouble(double min, double max) {
    static random_device rd;
    static mt19937 gen(rd());
    uniform_real_distribution<double> dis(min, max);
    return dis(gen);
}

class Dot {
public:
    double x, y, vx, vy;
    int state; // 0: Susceptible, 1: Infected, 2: Recovered
    int infected_no = 0;
    int infected_days = 0;

    

    Dot() { // initialize random position and velocity
        x = getRandomDouble(0, BOXSIZE);
        y = getRandomDouble(0, BOXSIZE);
        double randangle = getRandomDouble(0, 2 * PI);
        vx = DOTVEL * sin(randangle);
        vy = DOTVEL * cos(randangle);
        state = 0;
    }

    void move() {
        x += vx;
        y += vy;

        // Boundary conditions
        if (x < 0 || x > BOXSIZE) vx *= -1;
        if (y < 0 || y > BOXSIZE) vy *= -1;

        if (state == 1) infected_days++;
    }
};

class DotArray {
public:
    vector<Dot> dots;
    int susceptible = 0, infected = 0, recovered = 0;

    DotArray(int N) {
        dots.reserve(N);
        for (int i = 0; i < N; ++i) {
            dots.emplace_back();
        }
        dots[0].state = 1; // Start with one infected dot
    }

    void update(double infection_radius, double infection_probability, int infection_duration) {
        for (Dot& dot : dots) {
            dot.move();
        }

        for (int i = 0; i < dots.size(); i++) {
            if (dots[i].state == 2) continue;

            for (int j = i + 1; j < dots.size(); j++) {
                if (dots[j].state + dots[i].state != 1) continue;
                // Distance check + probability check
                double dx = dots[i].x - dots[j].x; // distance check
                double dy = dots[i].y - dots[j].y;
                if (dx * dx + dy * dy <= infection_radius * infection_radius && getRandomDouble(0, 1) < infection_probability) {
                    dots[j].state = 1;  // infected
                }
                
            }
            
        }

        for (Dot& dot : dots) {
            if (dot.state == 1 && dot.infected_days > infection_duration)
                dot.state = 2;
        }
    }
};