#include <mutex>
#include <vector>
#include <queue>
#include <condition_variable>
#include <functional>
#include <thread>

#ifndef POOL_H
#define POOL_H
class Pool
{
public:
	void Start();
	void QueueJob(const std::function<void()> &job);
	void Stop();
	bool busy();

private:
	void ThreadLoop();

	bool should_terminate = false;
	std::mutex queue_mutex;
	std::condition_variable mutex_condition;
	std::vector<std::thread> threads;
	std::queue<std::function<void()>> jobs;
};

#endif