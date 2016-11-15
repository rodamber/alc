#!/usr/bin/env python3
# encoding: utf-8

import unittest
import pytest

from alc import *

class TestPlace(unittest.TestCase):

    # def test_does_not_mutate_vm(self):
    #     s0 = server(0, 0, 0)
    #     v0 = virtual_machine(0, 0, 0, 1, 1, False)
    #     place(v0, s0, {s0 : []})
    #     self.assertTrue(v0 == v0)

    def test_servers_with_no_capacity(self):
        s0 = server(0, 0, 0)
        v0 = virtual_machine(0, 0, 0, 1, 1, False)
        self.assertIsNone(place(v0, s0, {s0: []}))

        s1 = server(0, 64, 0)
        self.assertIsNone(place(v0, s1, {s1: []}))

        s2 = server(0, 0, 256)
        self.assertIsNone(place(v0, s2, {s2: []}))

    def test_vm_with_anti_collocation_constraint(self):
        v0 = virtual_machine(0, 0, 0, 1, 1, True)
        v1 = virtual_machine(1, 0, 1, 1, 1, True)
        v2 = virtual_machine(2, 0, 2, 1, 1, False)
        v3 = virtual_machine(3, 1, 0, 1, 1, True)

        s0 = server(0, 100, 100)
        assignment = place(v0, s0, {s0: []})

        self.assertIsNotNone(assignment)
        self.assertIsNone(place(v1, s0, assignment))

        self.assertIsNotNone(place(v2, s0, assignment))
        self.assertIsNotNone(place(v3, s0, assignment))

    def test_vm_with_no_anti_collocation_constraint(self):
        v0 = virtual_machine(0, 0, 0, 1, 1, False)
        v1 = virtual_machine(1, 0, 1, 1, 1, True)
        v2 = virtual_machine(2, 0, 2, 1, 1, False)
        v3 = virtual_machine(3, 1, 0, 1, 1, True)
        v4 = virtual_machine(4, 1, 1, 1, 1, False)

        s0 = server(0, 100, 100)
        assignment = {s0: []}

        self.assertIsNotNone(place(v0, s0, assignment))
        self.assertIsNotNone(place(v1, s0, assignment))
        self.assertIsNotNone(place(v2, s0, assignment))
        self.assertIsNotNone(place(v3, s0, assignment))
        self.assertIsNotNone(place(v4, s0, assignment))

    def test_server_capacity_is_decreased(self):
        v0 = virtual_machine(0, 0, 0, 1, 1, False)
        v1 = virtual_machine(1, 0, 1, 1, 1, True)
        v2 = virtual_machine(2, 0, 2, 1, 1, False)

        s0 = server(0, 2, 2)
        assignment = place(v0, s0, {s0: []})

        self.assertEqual(s0.cpu_cap, 1)
        self.assertEqual(s0.ram_cap, 1)

        place(v1, s0, assignment)

        self.assertEqual(s0.cpu_cap, 0)
        self.assertEqual(s0.ram_cap, 0)

        self.assertIsNone(place(v2, s0, assignment))

    def test_vm_already_in_server(self):
        v0 = virtual_machine(0, 0, 0, 1, 1, False)

        s0 = server(0, 100, 100)
        assignment = {s0: []}

        self.assertIsNotNone(place(v0, s0, assignment))
        self.assertIsNone(place(v0, s0, assignment))

class TestAssign(unittest.TestCase):

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

    def test_space_left(self):
        self.assertIsNotNone(assign([self.v0, self.v2], {self.s0: []}))
        self.assertIsNone(assign([self.v0, self.v2, self.v3], {self.s0: []}))

    def test_anti_collocation_constraints(self):
        self.assertIsNone(   assign([self.v1],          {self.s0: [self.v0]}))
        self.assertIsNone(   assign([self.v1, self.v2], {self.s0: [self.v0]}))
        self.assertIsNotNone(assign([self.v1, self.v4], {self.s2: [self.v0], 
                                                         self.s3: [self.v3]}))

    def test_no_anti_collocation_constraints(self):
        self.assertIsNotNone(assign([self.v2],          {self.s3: [self.v0]}))
        self.assertIsNotNone(assign([self.v2, self.v5], {self.s3: [self.v0]}))
        self.assertIsNotNone(assign([self.v2, self.v5], {self.s2: [self.v0, self.v3], 
                                                         self.s3: [self.v1, self.v4]}))

    def test_1st_project_example(self):
        result = assign(self.vms, {self.s2: [], self.s3: []})
        self.assertIsNotNone(result)


class TestAssignmentFromModel(unittest.TestCase):
    pass

class TestBasicSolve(unittest.TestCase):

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
        result = basic_solve(self.servers, self.vms)
        self.assertIsNotNone(result)
        self.assertEqual(2, len(result))

class TestSolve(unittest.TestCase):

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


class TestMain(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
