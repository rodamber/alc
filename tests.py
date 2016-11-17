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

class TestAssignmentFromModel(unittest.TestCase):
    def setUp(self):
        self.servers = [server(0, 6, 6), server(1, 7, 8), server(2, 8, 6),
                        server(3, 7, 10)]
        self.s0, self.s1, self.s2, self.s3 = self.servers
        self.vms = [virtual_machine(0, 0, 0, 1, 2, True),
                    virtual_machine(1, 0, 1, 2, 1, True),
                    virtual_machine(2, 1, 0, 3, 3, False),
                    virtual_machine(3, 2, 0, 1, 1, True),
                    virtual_machine(4, 2, 1, 1, 4, True),
                    virtual_machine(5, 2, 2, 1, 2, False),
                    virtual_machine(6, 3, 0, 3, 2, True),
                    virtual_machine(7, 3, 1, 1, 3, True)]
        self.v0, self.v1, self.v2, self.v3, self.v4, self.v5, self.v6, self.v7 = self.vms

    def test_assignment_from_model(self):
        V = {vm : Int('VM{}'.format(vm.id)) for vm in self.vms}
        S = {s : Function('s{}'.format(s.id), IntSort(), IntSort()) for s in self.servers}
        f = Function('f', IntSort(), IntSort())

        #-----------------------------------------------------------------------

        solver = Solver()

        solver.add(cardinality_constraints(V, S))

        min_num_servers, constraints = anti_collocation_constraints(V)
        solver.add(constraints)

        solver.add(server_capacity_constraints(V, S))

        for s in self.servers:
            solver.add(If(Sum([S[s](v) for _, v in V.items()]) >= 1, f(s.id) == 1, f(s.id) == 0))

        #-----------------------------------------------------------------------

        # We know the solution is 2 servers.
        solver.add(Sum([f(s.id) for s in self.servers]) == 2)

        self.assertTrue(solver.check() == sat)
        model = solver.model()

        assignment = {self.s1: [self.v0, self.v4, self.v5, self.v6], 
                      self.s3: [self.v1, self.v2, self.v3, self.v7]}
        assignment_ = assignment_from_model(self.servers, V, model)

        self.maxDiff = None
        self.assertEqual(len(assignment), len(assignment_))

class TestSolve(unittest.TestCase):

    @timeout(10 * 60.0)
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
