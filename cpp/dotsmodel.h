#include <cmath>
#include <ctime>
#include <fstream>
#include <iostream>
#define PI 3.141592
#define boxsize 30
using namespace std;

class dot
{
public:
	double x;
	double y;
	double vx;
	double vy;
	int state;
	int infected_no;
	int infected_days;
	dot(){
		x = (rand() / (double)RAND_MAX) * 30;
		y = (rand() / (double)RAND_MAX) * 30;
		double randangle = rand() / (double)RAND_MAX * 2 * PI;
		vx = 0.05*sin(randangle);
		vy = 0.05*cos(randangle);
		state = 0;
		infected_no = 0;
		infected_days = 0;
	};
	void move()
	{
		x += vx;
		y += vy;
		if (x < 0) {
			x = -x;
			vx = -vx;
		}
		else if (x > boxsize) {
			x = boxsize * 2 - x;
			vx = -vx;
		}
		if (y < 0) {
			y = -y;
			vy = -vy;
		}
		else if (y > boxsize) {
			y = boxsize * 2 - y;
			vy = -vy;
		}
		if(state == 1){
			infected_days++;
		}
	}
};
class dotarray
{
public:
	dot* d;
	int N;
	int susceptible;
	int infected;
	int removed;
	double R;
	int infection_duration;
	dotarray(int arraysize, int dur)
	{
		N = arraysize;
		d = new dot[N];
		susceptible = arraysize;
		infected = 0;
		removed = 0;
		R = 0;
		infection_duration = dur;
	}
	void infectCentre()
	{
		double distFromCent = 1000;
		int centMarker = 0;
		for(int i = 0; i < N; i++)
		{
			double dx = d[i].x - boxsize/2;
			double dy = d[i].y - boxsize/2;
			double dist = sqrt(dx*dx + dy*dy);
			if(dist < distFromCent)
			{
				centMarker = i;
				distFromCent = dist;
			}
		}
		d[centMarker].state = 1;
	}
	void sircount()
	{
		susceptible = 0;
		infected = 0;
		removed = 0;
		R = 0;
		for (int i = 0; i < N; i++)
		{
			if(d[i].state == 1)
			{
				infected++;
				R += (double)d[i].infected_no / (double)d[i].infected_days * (double)infection_duration;
			}
			else if(d[i].state == 0)
			{
				susceptible++;
			}
			else
			{
				removed++;
			}
		}
		if(infected)
		R = (double)R / (double)(infected+removed);
	}
	double ijdistsqr(dot a, dot b)
	{
		double dx = a.x - b.x;
		double dy = a.y - b.y;
		return dx*dx + dy*dy;
	}
	void doStep(double infection_probability, double radsqr)
	{
		for (int i = 0; i < N; ++i)	//infect
		{
			for (int j = 0; j < N; ++j)
			{
				if(d[i].state == 1 && d[j].state == 0 && (rand()/(double)RAND_MAX)<infection_probability && ijdistsqr(d[i], d[j]) < radsqr)
				{
					d[j].state = 1;
					d[i].infected_no += 1;
				}
			}
		}
		for(int i = 0; i < N; i++)	//move a step
		{
			d[i].move();
		}
		for(int i = 0; i < N; i++)	//check infection time
		{
			if(d[i].infected_days >= infection_duration)
			d[i].state = 2;
		}
	}
};
class animation
{
public:
	ofstream data;
	void refresh(dotarray dots)
	{
		data.open("people.csv", ofstream::out);
		if (data.is_open() == false)
			{
				cout << "File write error";
				system("pause");
				exit(1);
			}
		data << " ,x,y,state" << endl;
		for(int i = 0; i < dots.N; i++)
		{
			data << i << "," << dots.d[i].x << "," << dots.d[i].y << "," << dots.d[i].state << endl;
		}	
		data.close();
	}
};
class sirdata
{
public:
	ofstream data;
	void start()
	{
		data.open("sir.csv", ofstream::out);
		if (data.is_open() == false)
		{
			cout << "File write error";
			system("pause");
			exit(1);
		}
		data << "Time,Susceptible,Infected,Removed,R value" << endl;
	}
	void output(int step, dotarray dots)
	{
		data << step << ",";
		data << dots.susceptible << ",";
		data << dots.infected << ",";
		data << dots.removed << ",";
		data << dots.R << endl;
	}
	void close()
	{
		data.close();
	}
};