#!/usr/bin/env python3
# encoding: utf-8

import unittest
import pytest

from alc import *

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

        solver.add(cardinality_constraints(self.servers, self.vms, V))

        min_num_servers, constraints = anti_collocation_constraints(self.servers, self.vms, V)
        solver.add(constraints)

        solver.add(server_capacity_constraints(self.servers, self.vms, V, S))

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

class TestSolveSimple(unittest.TestCase):

    def setUp(self):
        self.servers = [server(0, 5, 2), server(1, 4, 1), server(2, 7, 3),
                        server(3, 8, 5)]
        self.s0, self.s1, self.s2, self.s3 = self.servers
        self.vms = [virtual_machine(0, 0, 0, 1, 1, True),
                    virtual_machine(1, 0, 1, 1, 1, True),
                    virtual_machine(2, 1, 0, 1, 1, False),
                    virtual_machine(3, 2, 0, 1, 1, True),
                    virtual_machine(4, 2, 1, 1, 1, True),
                    virtual_machine(5, 2, 2, 1, 1, False),
                    virtual_machine(6, 3, 0, 1, 1, True),
                    virtual_machine(7, 3, 1, 1, 1, True)]
        self.v0, self.v1, self.v2, self.v3, self.v4, self.v5, self.v6, self.v7 = self.vms

    def test_1st_project_example(self):
        result = solve(self.servers, self.vms)
        self.assertIsNotNone(result)
        self.assertEqual(2, len(result))

    def test_bench11_small_1(self):
        servers, vms = get_problem('input/bench11-small/s32-vm25p-map0p-1-111c-small.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(8, len(assignment))

    def test_bench11_small_2(self):
        servers, vms = get_problem('input/bench11-small/s32-vm25p-map0p-2-111c-small.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(7, len(assignment))

    def test_bench11_small_3(self):
        servers, vms = get_problem('input/bench11-small/s32-vm25p-map0p-3-111c-small.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(7, len(assignment))

    def test_bench11_small_4(self):
        servers, vms = get_problem('input/bench11-small/s32-vm50p-map0p-4-111c-small.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(7, len(assignment))

    def test_bench11_small_5(self):
        servers, vms = get_problem('input/bench11-small/s32-vm50p-map0p-5-111c-small.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(5, len(assignment))

    def test_bench11_1(self):
        servers, vms = get_problem('input/bench11/s32-vm25p-map0p-1-111c.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(17, len(assignment))

    def test_bench11_2(self):
        servers, vms = get_problem('input/bench11/s32-vm25p-map0p-2-111c.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(16, len(assignment))

    def test_bench11_3(self):
        servers, vms = get_problem('input/bench11/s32-vm25p-map0p-3-111c.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(8, len(assignment))

    def test_bench11_4(self):
        servers, vms = get_problem('input/bench11/s32-vm50p-map0p-4-111c.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(10, len(assignment))

    def test_bench11_5(self):
        servers, vms = get_problem('input/bench11/s32-vm50p-map0p-5-111c.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(9, len(assignment))

class TestSolveComplex(unittest.TestCase):

    # This plugin is not working... --'
    # @pytest.mark.timeout(timeout=1, method='thread')
    # def test_timeout(self):
    #     for i in range(1000000000000):
    #         pass
    #     print('done')

    @pytest.mark.timeout(timeout=30, method='thread')
    def test_01_in(self):
        servers, vms = get_problem('input/01.in')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(2, len(assignment))

    @pytest.mark.timeout(timeout=30, method='thread')
    def test_02_in(self):
        servers, vms = get_problem('input/02.in')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(2, len(assignment))

    def test_bench22_small_1(self):
        servers, vms = get_problem('input/bench22-small/s32-vm25p-map0p-1-222a-small.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(8, len(assignment))

    def test_bench22_small_2(self):
        servers, vms = get_problem('input/bench22-small/s32-vm25p-map0p-2-222a-small.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(6, len(assignment))

    def test_bench22_small_3(self):
        servers, vms = get_problem('input/bench22-small/s32-vm25p-map0p-3-222a-small.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(6, len(assignment))

    def test_bench22_small_4(self):
        servers, vms = get_problem('input/bench22-small/s32-vm50p-map0p-4-222a-small.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(6, len(assignment))

    def test_bench22_small_5(self):
        servers, vms = get_problem('input/bench22-small/s32-vm50p-map0p-5-222a-small.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(5, len(assignment))

    def test_bench22_1(self):
        servers, vms = get_problem('input/bench22/s32-vm25p-map0p-1-222a.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(14, len(assignment))

    def test_bench22_2(self):
        servers, vms = get_problem('input/bench22/s32-vm25p-map0p-2-222a.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(10, len(assignment))

    def test_bench22_3(self):
        servers, vms = get_problem('input/bench22/s32-vm25p-map0p-3-222a.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(8, len(assignment))

    def test_bench22_4(self):
        servers, vms = get_problem('input/bench22/s32-vm50p-map0p-4-222a.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(8, len(assignment))

    def test_bench22_5(self):
        servers, vms = get_problem('input/bench22/s32-vm50p-map0p-5-222a.desc')
        assignment   = solve(servers, vms)

        self.assertIsNotNone(assignment)
        self.assertEqual(5, len(assignment))

class TestMain(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
