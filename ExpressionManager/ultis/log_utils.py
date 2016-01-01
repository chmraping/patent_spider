# coding:utf8 #
__author__ = 'damon_lin'

from ExpressionManager.models import logdata, history_log


class logger:
	cnt = 0
	buffer = ''
	# data = logdata.objects.get(id=1)
	data = logdata()
	history = None

	def __init__(self):
		super(logger, self)

	@classmethod
	def log(self, content, flush=False, count=None):
		print content
		self.cnt += 1
		self.buffer += ("<p>" + content + "<p>")
		if self.cnt > 10 or flush == True:
			self.flush(count)

	@classmethod
	def flush(self, count=None):
		self.cnt = 0
		# self.data = logdata.objects.get(id=1)
		self.data.content += self.buffer
		if count is not None:
			self.data.count = count
			self.history.end_id = count
		self.data.save()
		self.history.work_time = ''.join(str(self.history.end_time - self.history.start_time).split('.')[:1])
		self.history.save()
		self.buffer = ''

	@classmethod
	def clear(self):
		self.data.content = ' '
		self.data.save()
		self.buffer = ' '

	@classmethod
	def begin(self, start_day, end_day, start):
		self.history = history_log(start_day=start_day,end_day=end_day,start_id=start,end_id=start)
		self.history.save()

	@classmethod
	def finished(self):
		self.history.state = '成功'

		self.history.work_time = ''.join(str(self.history.end_time - self.history.start_time).split('.')[:1])
		self.history.save()
		self.data = logdata()


