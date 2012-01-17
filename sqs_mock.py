import os
import pickle

class SQSQueueMock:
	_fp = None
	name = None
	def __init__(self, filename, create=False):
		try:
			open(filename + ".sqs")
		except IOError:
			if create:
				self._fp = open(filename + ".sqs", 'w')
			else:
				raise SyntaxError("Queue %s does not exist" % filename)
		self.name = filename	
		
	def clear(self, page_size=10, vtimeout=10):
		try:
			open(self.name + '.sqs', 'w').close()
		except EOFError:
			return False
		return True
	
	def count(self, page_size=10, vtimeout=10):
		try:
			prev_data = pickle.load(open(self.name + '.sqs', 'r'))
		except EOFError:
			return 0
		return len(prev_data)
		
	def count_slow(self, page_size=10, vtimeout=10):
		return count(page_size=10, vtimeout=10)
		
	def delete(self):
		try:
			os.remove(self.name + '.sqs')
		except OSError:
			# What happens here?
			return False
		return True
	def delete_message(self, message):
		prev_data = pickle.load(open(self.name + '.sqs', 'r'))
		for data in prev_data:
			if data.get_body() == message.get_body():
				try:
					prev_data.remove(data)
					break
				except ValueError:
					return False
		try:
			pickle.dump(prev_data, open(self.name + '.sqs', 'w'))
		except IOError:
			return False
		
		return True
	def get_messages(self, num_messages=1, visibility_timeout=None, attributes=None):
		messages = []
		try:
			prev_data = pickle.load(open(self.name + '.sqs', 'r'))
		except EOFError:
			prev_data = []
		i = 0
		while i < num_messages and len(prev_data) > 0:
			try:
				messages.append(prev_data[i])
			except IndexError:
				pass
			i += 1
		return messages
	def read(self, visibility_timeout=None):
		prev_data = pickle.load(open(self.name + '.sqs', 'r'))
		try:
			return prev_data.pop(0)
		except IndexError:
			# Is this the real action?
			return None
	def write(self, message):
		# Should do some error checking
		
		# read in all the data in the queue first
		try:
			prev_data = pickle.load(open(self.name + '.sqs', 'r'))
		except EOFError:
			prev_data = []

		prev_data.append(message)
		
		try:
			pickle.dump(prev_data, open(self.name + '.sqs', 'w'))
		except IOError:
			return False
			
		return True
	
class SQSConnectionMock:
	def get_queue(self, queue):
		try:
			queue_file = open(queue + ".sqs")
		except IOError:
			return None
		try:
			return SQSQueueMock(queue_file)
		except SyntaxError:
			return None
			
	def get_all_queues(self, prefix=""):
		queue_list = []
		files = os.listdir(".")
		for f in files:
			if f[-4:] == '.sqs':
				if prefix != "":
					if f[0:len(prefix)] == prefix:
						try:
							# Try to make the queue. If there's something wrong, just move on.
							q = SQSQueueMock(f)
						except SyntaxError:
							continue
						queue_list.append(q)
				else:
					try:
						# Try to make the queue. If there's something wrong, just move on.
						q = SQSQueueMock(f[:-4])
					except SyntaxError:
						print 'err', f
						continue
					queue_list.append(q)
		return queue_list
	def delete_queue(self, queue, force_deletion=False):
		if q.count() != 0:
			# Can only delete empty queues
			return False
		q = self.get_queue(queue)
		return q.delete()
		
	def delete_message(self, queue, message):
		return queue.delete_message(message)
		
	def create_queue(self, name):
		a = SQSQueueMock(name, create=True)
		return a
		