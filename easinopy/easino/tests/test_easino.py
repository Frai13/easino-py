import unittest
import io
import os
import unittest.mock
import threading
from easinopy.easino.easino import *

class TestEasIno(unittest.TestCase):
    
    class EasinoTest(EasIno):
        
        def __init__(self):
            self._timeout = 100
            self.not_join = False
            self.data_test = DataCom(operation='TEST')
            self.time_send = 0
            self.data_subcribed = []
            self.thread = None

        @property
        def timeout(self):
            return self._timeout
        
        @timeout.setter
        def timeout(self, value):
            self._timeout = value
        
        def start(self):
            pass
        
        def stop(self):
            pass
        
        def _derived_send(self, line):
            if self.thread is not None and not self.not_join:
                self.thread.join()
            def simulate_received():
                time.sleep(self.time_send / 1000)
                data_args = DataReceivedArgs(DataCom._from_str(line))
                self._call_data_received_callback(data_args)
            self.thread = threading.Thread(target=simulate_received)
            self.thread.start()
    
    def test_version(self):
        self.assertRegex(EasIno.get_api_version(), r'\d+\.\d+\.\d+')

    def test_abstract(self):
        def helper_abstract_exception():
            class EasinoFail(EasIno):
                pass
            easino_fail = EasinoFail()
        
        with self.assertRaises(TypeError) as cm:
            helper_abstract_exception()
        self.assertEqual(str(cm.exception), ('Can\'t instantiate abstract class EasinoFail with ' +
                         'abstract methods _derived_send, start, stop, timeout'))

    def test_receive(self):
        easino_test = self.EasinoTest()
        self.assertRaises(TimeoutError, easino_test.receive)
        easino_test.time_send = 50
        d = easino_test.send_and_receive(easino_test.data_test)
        self.assertEqual(d, easino_test.data_test)
        d = easino_test.send_and_receive(DataCom())
        self.assertEqual(d, DataCom())
        easino_test.time_send = 150
        self.assertRaises(TimeoutError, easino_test.send_and_receive, easino_test.data_test)
        easino_test.thread.join()
        
        easino_test.time_send = 250
        easino_test.not_join = True
        d = easino_test.try_send_and_receive(easino_test.data_test, 3)
        easino_test.thread.join()
        self.assertEqual(d, easino_test.data_test)
        easino_test.time_send = 500
        self.assertRaises(TimeoutError, easino_test.try_send_and_receive, easino_test.data_test, 3)
        easino_test.not_join = False
        easino_test.thread.join()

    def test_subscribe(self):
        easino_test = self.EasinoTest()
        easino_test.data_subcribed = []
        def data_received(args):
            easino_test.data_subcribed.append(args)
        easino_test.subscribe_data_received_callback(data_received)

        easino_test.time_send = 50
        d = easino_test.send_and_receive(easino_test.data_test)
        self.assertEqual(d, easino_test.data_test)
        self.assertEqual(len(easino_test.data_subcribed), 0)

        easino_test.send(easino_test.data_test)
        easino_test.thread.join()
        self.assertEqual(len(easino_test.data_subcribed), 1)
        self.assertEqual(easino_test.data_subcribed[0].data, easino_test.data_test)
        
        easino_test.data_subcribed = []
        easino_test.send(easino_test.data_test)
        easino_test.send(easino_test.data_test)
        easino_test.send(easino_test.data_test)
        easino_test.thread.join()
        self.assertEqual(len(easino_test.data_subcribed), 3)



if __name__ == '__main__':
    unittest.main()
