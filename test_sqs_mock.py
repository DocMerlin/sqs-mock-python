import unittest
from sqs_mock import SQSConnectionMock, SQSQueueMock
from boto.sqs.message import Message
import os

class QueueTest(unittest.TestCase):
	def setUp(self):
		open('test.sqs', 'w').close()
	def tearDown(self):
		try:
			os.remove('test.sqs')
		except OSError:
			pass
	def test_create(self):
		q = SQSQueueMock('test')
		self.assertTrue(isinstance(q, SQSQueueMock ))
		self.assertTrue(q.name == 'test')
	def test_clear(self):
		q = SQSQueueMock('test')
		m = Message()
		m.set_body('this is a test')
		status = q.write(m)
		self.assertTrue(q.count() == 1)
		status = q.write(m)
		status = q.write(m)
		status = q.write(m)
		self.assertTrue(q.count() == 4)
		self.assertTrue(q.clear())
		self.assertTrue(q.count() == 0)
	def test_count(self):
		q = SQSQueueMock('test')
		m = Message()
		m.set_body('this is a test')
		status = q.write(m)
		self.assertTrue(status)
		self.assertTrue(q.count() == 1)
		
		status = q.write(m)
		self.assertTrue(status)
		self.assertTrue(q.count() == 2)
		
		status = q.write(m)
		self.assertTrue(status)
		self.assertTrue(q.count() == 3)
		
		messages = q.get_messages(num_messages=1)
		self.assertTrue(q.delete_message(messages[0]))
		self.assertTrue(q.count() == 2)
		
		messages = q.get_messages(num_messages=1)
		self.assertTrue(q.delete_message(messages[0]))
		self.assertTrue(q.count() == 1)
		
		messages = q.get_messages(num_messages=1)
		self.assertTrue(q.delete_message(messages[0]))
		self.assertTrue(q.count() == 0)
	def test_delete(self):
		q = SQSQueueMock('test')
		self.assertTrue(q.delete())
		self.assertFalse(os.path.exists('test.sqs'))
	def test_delete_message(self):
		m = Message()
		m.set_body('this is a test')
		q = SQSQueueMock('test')
		status = q.write(m)
		self.assertTrue(status)
		
		messages = q.get_messages(num_messages=2)
		self.assertTrue(len(messages) == 1)
		self.assertTrue(messages[0].get_body() == 'this is a test')
		
		self.assertTrue(q.delete_message(messages[0]))
		
		messages = q.get_messages(num_messages=1)
		self.assertTrue(len(messages) == 0)
		
	def test_get_messages(self):
		pass
	def test_read(self):
		m = Message()
		m.set_body('this is a test')
		q = SQSQueueMock('test')
		status = q.write(m)
		self.assertTrue(status)
		
		messages = q.get_messages(num_messages=2)
		self.assertTrue(len(messages) == 1)
		self.assertTrue(messages[0].get_body() == 'this is a test')
	def test_write(self):
		m = Message()
		m.set_body('this is a test')
		q = SQSQueueMock('test')
		status = q.write(m)
		self.assertTrue(status)
	
class ConnectionTest(unittest.TestCase):
	def tearDown(self):
		try:
			os.remove('conntest.sqs')
		except OSError:
			pass
	def test_get_queue(self):
		# Try to create a queue
		conn = SQSConnectionMock()
		self.assertTrue(conn.get_queue('conntest') == None)
	def test_get_all_queues(self):
		conn = SQSConnectionMock()
		self.assertTrue(conn.create_queue('conntest'))
		self.assertTrue(conn.create_queue('conntest1'))
		queues = conn.get_all_queues()
		self.assertTrue(queues != None)
		self.assertTrue(len(queues) == 2)
		
		os.remove('conntest1.sqs')
	def test_delete_queue(self):
		conn = SQSConnectionMock()
		self.assertTrue(conn.create_queue('conntest'))
		self.assertTrue(conn.delete_queue('conntest'))
		self.assertFalse(os.path.exists('conntest.sqs'))
	def test_delete_message(self):
		pass
	def test_create_queue(self):
		conn = SQSConnectionMock()
		self.assertTrue(conn.create_queue('conntest'))
		self.assertTrue(os.path.exists('conntest.sqs'))
if __name__ == '__main__':
	unittest.main()