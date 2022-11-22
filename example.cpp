#include <iostream>
#include <thread>
#include <future>
#include <math.h>
#include <cstdint>
#include <inttypes.h>

double f(double x, double s)
{
	return 2 * x * s;
}

double g(double y, double s)
{
	return 3 * y * s;
}

double h(double z, double s)
{
	return 4 * z * s;
}

int main1(int argc, char const *argv[])
{
	double s = 0.00001;
	double x = 0.00001,
					y = 0.00001,
					z = 0.00001;
	while (s < pow(10, 17))
	{
		std::future<double > f_res = std::async(&f, x, s);
		std::future<double > g_res = std::async(&g, y, s);
		std::future<double > h_res = std::async(&h, z, s);

		x = f_res.get();
		y = g_res.get();
		z = h_res.get();

		s = x + y + z;
		std::cout << x << "\t" << y << "\t" << z << "\t" << s << std::endl;
	}
	// s =  + g(y) + h(z);
	return 0;
}