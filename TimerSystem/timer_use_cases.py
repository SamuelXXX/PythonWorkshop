import time
from TimerSystem.timer import Timer

class TimerUseCase1(object):
	timer_core=None
	count=0
	def __init__(self):
		self.timer_core=Timer()

		self.timer_core.register_timer_func("count", self.count_timer)
		self.timer_core.register_timer_func("func1", self.timer_func1)
		self.timer_core.register_timer_func("func2", self.timer_func2)
		self.timer_core.register_timer_func("func3", self.timer_func3)

		self.timer_core.set_time(time.time()) # 先设置时间
		self.timer_core.start_timer("count", 1)  # 一秒后开启count function
		self.timer_core.start_timer("func1", 1.4) # 1.4秒后开启第一个timer function

	def count_timer(self):
		self.count += 1
		print(">>>Seconds:"+str(self.count))
		return 1

	def timer_func1(self):
		print("timer func1")
		if self.count==5:
			self.timer_core.start_timer("func2",2.5)
			return None
		return 1

	def timer_func2(self):
		print("timer func2")
		if self.count==20:
			self.timer_core.stop_all_timers()
			self.timer_core.start_timer("func3",5)
		return 1

	def timer_func3(self):
		print("timer func3")
		print(">>>Re-Initializing...")
		self.count=0
		self.timer_core.start_timer("count", 2)  # 2秒后开启count function
		self.timer_core.start_timer("func1", 2.4)  # 2.4秒后开启第一个timer function
		return None

	def launch(self):
		while True:
			self.timer_core.process_all_timers(time.time())



