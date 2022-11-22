#include <iostream>
#include <thread>
#include <math.h>
#include <cstdint>
#include <fstream>
#include <math.h>
#include <omp.h>
#include <time.h>
#include "includes/functions.h"

#define iterations 100000

int main(int argc, char const *argv[])
{
	double time_spent = 0.0;
	long double V_val[iterations];
	long double
			n_val[iterations],
			m_val[iterations],
			h_val[iterations];

	n_val[0] = (an(0)) / (an(0) + bn(0));
	m_val[0] = (am(0)) / (am(0) + bm(0));
	h_val[0] = (ah(0)) / (ah(0) + bh(0));
	long double dn, dm, dh, dV;
	double dt = 0.01;
	clock_t begin = clock();
	for (int i = 1; i < iterations; i++)
	{
			#pragma omp target teams distribute parallel
		{
			#pragma omp section
			dV = V(V_val[i - 1], n_val[i - 1], m_val[i - 1], h_val[i - 1]);
			#pragma omp section
			dm = m(V_val[i - 1], m_val[i - 1]);
			#pragma omp section
			dn = n(V_val[i - 1], n_val[i - 1]);
			#pragma omp section
			dh = h(V_val[i - 1], h_val[i - 1]);
			#pragma omp section
			{
				n_val[i] = n_val[i - 1] + dn * dt;
				m_val[i] = m_val[i - 1] + dm * dt;
				h_val[i] = h_val[i - 1] + dh * dt;
				V_val[i] = V_val[i - 1] + dV * dt;
			}
		}
	}
	clock_t end = clock();
	for (int i = 0; i < iterations; i++)
	{
		std::cout << V_val[i] << std::endl;
	}
	time_spent += (double)(end - begin) / CLOCKS_PER_SEC;
	printf("The elapsed time is %f seconds", time_spent);
	return 0;
}