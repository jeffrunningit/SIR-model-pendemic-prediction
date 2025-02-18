//#include <ctime>
#include <iostream>
#include <windows.h>
#include "dotsmodel.h"
using namespace std;

int main()
{
	double infection_radius;
	double infection_probability;
	int infection_duration;
	double stepperday = 10;
	bool animate = 0;
	bool plotsir = 1;
	srand((unsigned)time(NULL));
	int N = 900;

	while(1){
	cout << "infection_radius: ";
	cin >> infection_radius;
	cout << "infection_probability: ";
	cin >> infection_probability;
	cout << "infection_duration: ";
	cin >> infection_duration;
	cout << "animate? ";
	cin >> animate;
	if(animate){
	cout << "Starting... in 3";
	Sleep(1000);
	cout << "\b2";
	Sleep(1000);
	cout << "\b1";
	Sleep(1000);
	}

	ofstream title("title.txt");
	title << "sir_r=" << infection_radius;
	title << "_p=" << infection_probability;
	title << "_d=" << infection_duration;
	title.close();

	double radsqr = infection_radius * infection_radius;
	double probperstep = infection_probability/stepperday;
	dotarray dots(N, infection_duration*stepperday);
	dots.infectCentre();

	sirdata sir;
	animation ani;
	
	int step = 0;	//1 day = 100 steps
	sir.start();
	do{
		if(animate)
			{ani.refresh(dots);}

		dots.doStep(probperstep, radsqr);
		sir.output(step, dots);
		dots.sircount();
		step++;
		if(step%50==0)
			cout << "Day " << step/stepperday << endl;
		//Sleep(10);
	}while(dots.infected);
	sir.close();
	if (dots.susceptible==0)
		cout << "All people are infected." << endl;
	if (dots.infected==0)
		cout << "No more infection." << endl;
	//Print final frame
	if(animate)
		{ani.refresh(dots);}
	}
	system("pause");
	return 0;
	
}