#!/usr/bin/env python3
# encoding: utf-8

import unittest
import multiprocessing.pool
import functools

from alc import *

# Taken from this SO answer: http://stackoverflow.com/a/35139284/3854518
def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator

class TestSolve(unittest.TestCase):

    @timeout(30.0)
    def meta_test(self, file, result):
        servers, vms = get_problem(file)
        assignment = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(result, len(assignment))

    def test_bench11_small_1(self):
        self.meta_test('input/bench11-small/s32-vm25p-map0p-1-111c-small.desc', 8)

    def test_bench11_small_2(self):
        self.meta_test('input/bench11-small/s32-vm25p-map0p-2-111c-small.desc', 7)

    def test_bench11_small_3(self):
        self.meta_test('input/bench11-small/s32-vm25p-map0p-3-111c-small.desc', 7)

    def test_bench11_small_4(self):
        self.meta_test('input/bench11-small/s32-vm50p-map0p-4-111c-small.desc', 7)

    def test_bench11_small_5(self):
        self.meta_test('input/bench11-small/s32-vm50p-map0p-5-111c-small.desc', 5)

    def test_bench11_1(self):
        self.meta_test('input/bench11/s32-vm25p-map0p-1-111c.desc', 17)

    def test_bench11_2(self):
        self.meta_test('input/bench11/s32-vm25p-map0p-2-111c.desc', 16)

    def test_bench11_3(self):
        self.meta_test('input/bench11/s32-vm25p-map0p-3-111c.desc', 8)

    def test_bench11_4(self):
        self.meta_test('input/bench11/s32-vm50p-map0p-4-111c.desc', 10)

    def test_bench11_5(self):
        self.meta_test('input/bench11/s32-vm50p-map0p-5-111c.desc', 9)

    def test_bench22_small_1(self):
        self.meta_test('input/bench22-small/s32-vm25p-map0p-1-222a-small.desc', 8)

    def test_bench22_small_2(self):
        self.meta_test('input/bench22-small/s32-vm25p-map0p-2-222a-small.desc', 6)

    def test_bench22_small_3(self):
        self.meta_test('input/bench22-small/s32-vm25p-map0p-3-222a-small.desc', 6)

    def test_bench22_small_4(self):
        self.meta_test('input/bench22-small/s32-vm50p-map0p-4-222a-small.desc', 6)

    def test_bench22_small_5(self):
        self.meta_test('input/bench22-small/s32-vm50p-map0p-5-222a-small.desc', 5)

    def test_bench22_1(self):
        self.meta_test('input/bench22/s32-vm25p-map0p-1-222a.desc', 14)

    def test_bench22_2(self):
        self.meta_test('input/bench22/s32-vm25p-map0p-2-222a.desc', 10)

    def test_bench22_3(self):
        self.meta_test('input/bench22/s32-vm25p-map0p-3-222a.desc', 8)

    def test_bench22_4(self):
        self.meta_test('input/bench22/s32-vm50p-map0p-4-222a.desc', 8)

    def test_bench22_5(self):
        self.meta_test('input/bench22/s32-vm50p-map0p-5-222a.desc', 5)

if __name__ == '__main__':
    unittest.main()
