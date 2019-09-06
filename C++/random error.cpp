/**********************************
Random Error Calculation
***********************************/

#include<iostream>
#include<cmath>

using namespace std;

int main()
{
	int N;
	
	cout << "Input number of measurments: ";
	cin >> N;
	
	float average = 0, value, absolut;
	float S, s = 0, k;
	float* values;
	float student_rate;
	
	values = new float [N];
	
	for(int i = 1; i <= N; i++)
	{
		cout << "Input " << i << " value: ";
		cin >> value;
		
		values[i-1] = value;
	}
	
	for(int i = 0; i < N; i++)
	{
		average += values[i];
	}
	
	average /= N;
		
	k = 1.0 / (N * (N-1));
	
	for(int i = 0; i < N; i++)
	{
		s += (values[i] - average) * (values[i] - average);
	}
	
	s *= k;
	
	S = sqrt(s);
	
	cout << "input Student rate: ";
	cin >> student_rate;
	
	cout << "S = " << S << endl;
	cout << "x = " << average << " +- " << S * student_rate;
	
}
