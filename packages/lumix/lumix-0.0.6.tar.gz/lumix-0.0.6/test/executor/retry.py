import random
import unittest
from lumix.executor.retry import RetryExecutor



class RetryExecutorTest(unittest.TestCase):
    def test_retry(self):
        def unreliable_operation(x):
            if random.random() < 0.9:  # 50%的概率失败
                raise ValueError("Random failure occurred")
            return x * 2

        executor = RetryExecutor(max_retries=3, verbose=True)
        result = executor.execute(unreliable_operation, 10)
        print(result)
