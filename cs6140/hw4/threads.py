import threading, time, numpy

def string_num(num):
	time.sleep(0.1)
	return str(num)

def multi_thread_test():
	result = {}
	threads = []
	for i in range(100):
		#result[i] = string_num(i)
		t = threading.Thread(target=test_1, args=(i,result))
		threads.append(t)
		t.start()
		if len(threads) >= 10:
			for t in threads:
				t.join()
			threads = []
	for t in threads:
		t.join()

def test_1(num,result):
	result[num] = string_num(num)

if __name__ == '__main__':
	multi_thread_test()