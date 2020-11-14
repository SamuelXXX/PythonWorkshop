import time
from timer import Timer

class TimerUseCase1(object):
	timer_core=None
	count=0
	def __init__(self):
		self.timer_core=Timer()

		self.timer_core.register_timer_func("func1", self.timer_func1)
		self.timer_core.register_timer_func("func2", self.timer_func2)

		self.timer_core.set_time(time.time()) # 先设置时间
		self.timer_core.start_timer("func1",2) # 再开启第一个timer function

	def timer_func1(self):
		print("timer func1:"+str(self.count))
		self.count += 1

		if self.count==5:
			# self.timer_core.stop_all_timers()
			self.timer_core.start_timer("func2",2.5)
		# if self.count<10:
		return 1

	def timer_func2(self):
		print("timer func2:"+str(self.count))
		self.count += 1
		return 1

	def launch(self):
		while True:
			self.timer_core.process_all_timers(time.time())


