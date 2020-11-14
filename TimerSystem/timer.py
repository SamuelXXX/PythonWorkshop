class Timer(object):
	# region Timer Register
	__handler_dict = None

	def register_timer_func(self, name, func):
		if self.__handler_dict is None:
			self.__handler_dict = {}
		self.__handler_dict[name] = func
	# endregion

	# region Timer Context
	__in_timer_context = False
	def __enter__(self):
		self.__in_timer_context = True

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.__in_timer_context = False
	# endregion

	# region Timer Processing
	__current_time = None # 保证先写后读
	# 都是只在process中使用的变量，用来保存在timer中创建的和timer相关的命令
	__cancelled_timers = None
	__added_timers = None
	__force_clear_all_timers = False

	def set_time(self, time):
		self.__current_time = time

	def process_all_timers(self, time):
		if self.running_timers is None:
			return

		self.__current_time = time

		self.__added_timers = {}
		self.__cancelled_timers = []
		self.__force_clear_all_timers = False

		for index, info in self.running_timers.items():
			func_name=info[0]
			tick_time=info[1]
			func=self.__handler_dict[func_name]

			if self.__current_time >= tick_time:
				with self:
					ret=func()

				if self.__force_clear_all_timers: # 如果发现了强制清空的命令，就直接停用停止迭代
					break

				if ret is None:
					self.__cancelled_timers.append(index)
				else:
					info[1] = self.__current_time + ret

		if self.__force_clear_all_timers:
			self.running_timers={}

		self.running_timers.update(self.__added_timers) # 将执行中创建的timer
		for i in self.__cancelled_timers:
			if i in self.running_timers:
				del self.running_timers[i]
		self.__current_time = None
	# endregion

	# region Timer Management
	running_timers = None
	assigned_timer_id = 0

	def start_timer(self, name, first_tick_delay):
		"""
		开启一个Timer
		在Timer函数内部使用没有任何限制
		在Timer函数之外使用的话，使用前一定要先调用set_time来确定一个基准时间，否则会报错
		:param name:
		:param first_tick_delay:
		:return:
		"""
		if self.running_timers is None:
			self.running_timers = {}

		assert name in self.__handler_dict

		if self.__in_timer_context:
			timer_id = self.assigned_timer_id
			self.__added_timers[timer_id] = [name, self.__current_time + first_tick_delay]
			self.assigned_timer_id += 1
			return timer_id

		timer_id=self.assigned_timer_id
		self.running_timers[timer_id] = [name, self.__current_time + first_tick_delay]
		self.assigned_timer_id+=1
		return timer_id

	def stop_timer(self, timer_id):
		if self.__in_timer_context:
			self.__cancelled_timers.append(timer_id)
			return

		if self.running_timers is None or timer_id not in self.running_timers:
			return

		del self.running_timers[timer_id]

	def stop_all_timers(self):
		if self.__in_timer_context:
			self.__force_clear_all_timers = True
			self.__added_timers = {} # 将在timer中创建的新的timer也清空掉
			return

		self.running_timers = {}
		# endregion
