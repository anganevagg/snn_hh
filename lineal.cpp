#include <iostream>
#include <thread>
#include <future>
#include <math.h>
#include <cstdint>
#include <fstream>
#include <time.h>
#include <math.h>

#define iterations 100000

long double Cm = 1, Im = 9.5,
						gK = 36, EK = -12, // -60 para el V de -60
		gNa = 120, ENa = 115,
						gL = 0.3, EL = 10.613;
long double am(long double x)
{
	if (x == 25)
		return 0.1;
	long double a = (25.0 - x);
	return (0.1 * a) / (exp(a / 10.0) - 1.0);
}
long double an(long double x)
{
	if (x == 10)
		return 0.1;
	long double a = (10 - x);
	return (0.01 * a) / (exp(a / 10) - 1.0);
}
long double ah(long double x)
{
	return (0.07 * exp(-x / 20.0));
}
long double bm(long double x)
{
	return (4.0 * exp(-x / 18.0));
}
long double bn(long double x)
{
	return (0.125 * exp(-x / 80.0));
}
long double bh(long double x)
{
	return (1.0 / (exp((30.0 - x) / 10) + 1.0));
}

long double n(long double V_val, long double n_val)
{
	return an(V_val) * (1 - n_val) - bn(V_val) * n_val;
}

long double m(long double V_val, long double m_val)
{
	return am(V_val) * (1 - m_val) - bm(V_val) * m_val;
}

long double h(long double V_val, long double h_val)
{
	return ah(V_val) * (1 - h_val) - bh(V_val) * h_val;
}

long double V(long double x, long double n_val, long double m_val, long double h_val)
{
	return ((-gK * pow(n_val, 4) * (x - EK)) - gNa * pow(m_val, 3) * h_val * (x - ENa) - gL * (x - EL) + Im) / Cm;
}

int main(int argc, char const *argv[])
{
	long double V_val[iterations];
	long double
			n_val[iterations],
			m_val[iterations],
			h_val[iterations];

	n_val[0] = (an(0)) / (an(0) + bn(0));
	m_val[0] = (am(0)) / (am(0) + bm(0));
	h_val[0] = (ah(0)) / (ah(0) + bh(0));
	long double dn, dm, dh, dV;
	double time_spent = 0.0;
	double dt = 0.01;
	// std::future<long double> n_res, m_res, h_res, V_res;
	// std::thread V_thread, m_thread, n_thread, h_thread, main_thread;
	clock_t begin = clock();
	for (int i = 1; i < iterations; i++)
	{
		dV = V(V_val[i - 1], n_val[i - 1], m_val[i - 1], h_val[i - 1]);
		dm = m(V_val[i - 1], m_val[i - 1]);

		dn = n(V_val[i - 1], n_val[i - 1]);

		dh = h(V_val[i - 1], h_val[i - 1]);
		n_val[i] = n_val[i - 1] + dn * dt;
		m_val[i] = m_val[i - 1] + dm * dt;
		h_val[i] = h_val[i - 1] + dh * dt;
		V_val[i] = V_val[i - 1] + dV * dt;
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