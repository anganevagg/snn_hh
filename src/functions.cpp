#include <math.h>
#include "includes/variables.h"
#include "includes/functions.h"

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
	// std::future<long double> an_res = std::async(std::launch::async, an, V_val), bn_res = std::async(std::launch::async, bn, V_val);
	return an(V_val) * (1 - n_val) - bn(V_val) * n_val;
}

long double m(long double V_val, long double m_val)
{
	// std::future<long double> am_res = std::async(std::launch::async, am, V_val), bm_res = std::async(std::launch::async, bm, V_val);
	return am(V_val) * (1 - m_val) - bm(V_val) * m_val;
}

long double h(long double V_val, long double h_val)
{
	// std::future<long double> ah_res = std::async(std::launch::async, ah, V_val), bh_res = std::async(std::launch::async, bh, V_val);
	return ah(V_val) * (1 - h_val) - bh(V_val) * h_val;
}

long double V(long double x, long double n_val, long double m_val, long double h_val)
{
	#pragma omp private(Cm, Im, gK, EK, gNa, ENa, gL, EL)
	return ((-gK * pow(n_val, 4) * (x - EK)) - gNa * pow(m_val, 3) * h_val * (x - ENa) - gL * (x - EL) + Im) / Cm;
}