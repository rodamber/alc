#!/usr/bin/env python3
# encoding: utf-8

from copy import deepcopy
from itertools import *

import sys

from z3 import *

class hardware:
    CPU = "CPU"
    RAM = "RAM"

class server:

    def __init__(self, id, cpu_cap, ram_cap):
        if (not isinstance(id, int)):
            raise TypeError("{} must be of type {}".format(id, int))
        if (not isinstance(cpu_cap, int)):
            raise TypeError("{} must be of type {}".format(cpu_cap, int))
        if (not isinstance(ram_cap, int)):
            raise TypeError("{} must be of type {}".format(ram_cap, int))

        self.id = id
        self.cpu_cap = cpu_cap
        self.ram_cap = ram_cap

    def __eq__(self, other):
        if isinstance(other, server):
            return self.id == other.id
        return False

    def __str__(self):
        template = '{{id: {}, cpu_cap: {}, ram_cap: {}}}'
        return template.format(self.id, self.cpu_cap, self.ram_cap)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.id

class virtual_machine:

    def __init__(self, id, job_id, vm_index, cpu_req, ram_req, anti_collocation):
        if (not isinstance(id, int)):
            raise TypeError("{} must be of type {}".format(vm_id, int))
        if (not isinstance(job_id, int)):
            raise TypeError("{} must be of type {}".format(job_id, int))
        if (not isinstance(vm_index, int)):
            raise TypeError("{} must be of type {}".format(vm_index, int))
        if (not isinstance(cpu_req, int)):
            raise TypeError("{} must be of type {}".format(cpu_req, int))
        if (not isinstance(ram_req, int)):
            raise TypeError("{} must be of type {}".format(ram_req, int))
        if (not isinstance(anti_collocation, bool)):
            raise TypeError("{} must be of type {}".format(anti_collocation, bool))

        self.id = id
        self.job_id = job_id
        self.vm_index = vm_index
        self.cpu_req = cpu_req
        self.ram_req = ram_req
        self.anti_collocation  = anti_collocation

    def __eq__(self, other):
        if isinstance(other, virtual_machine):
            return self.id == other.id
        return False

    def __str__(self):
        template = '{{job_id: {}, vm_index: {}, cpu_req: {}, ram_req: {}, ac: {}}}'
        return template.format(self.job_id, self.vm_index, self.cpu_req,
                               self.ram_req, self.anti_collocation)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.id

def get_program_args():
    """IO [String]
    Returns a list containing the program arguments.
    """
    return sys.argv[1:]

def get_file_name():
    """IO String
    Returns the name of the file to read or empty if we got no file to read.
    """
    args = get_program_args()
    if (len(args)):
        return args[0]
    else:
        return ""

def get_problem(file_name):
    """ String -> IO {String: []}
    Parses the file named file_name and returns a dictionary returning the
    specification of the problem.
    """
    if (not isinstance(file_name, str)):
        raise TypeError("file_name must be of type string")

    servers = []
    vms = []

    with open(file_name) as f:
        num_servers = int(f.readline())
        # print("num_servers = {}".format(num_servers))
        for _ in range(num_servers):
            server_id, cpu_cap, ram_cap = [int(x) for x in f.readline().split()]
            # print("server_id: {}, cpu_cap: {}, ram_cap: {}".format(server_id, cpu_cap, ram_cap))
            servers += [server(server_id, cpu_cap, ram_cap)]
        num_vms = int(f.readline())
        # print("num_vms = {}".format(num_vms))
        for vm_id in range(num_vms):
            line = f.readline().split()
            job_id, vm_index, cpu_req, ram_req = [int(x) for x in line[:-1]]
            anti_collocation = (line[-1] == "True")
            # print("job_id: {}, vm_index: {}, cpu_req: {}, ram_req: {}, anti_collocation: {}".format(job_id, vm_index, cpu_req, ram_req, anti_collocation))
            vms += [virtual_machine(vm_id, job_id, vm_index, cpu_req,
                                    ram_req, anti_collocation)]
    return servers, vms

def cardinality_constraints(V, S):
    return [And(0 <= v, v < len(S)) for v in V.values()]

def anti_collocation_constraints(V):
    jobs            = [list(g) for _, g in groupby(V.keys(), lambda v: v.job_id)]
    ac_matrix       = [[V[vm] for vm in job if vm.anti_collocation] for job in jobs]

    constraints     = [Distinct(j) for j in ac_matrix if j]
    min_num_servers = max([len(j) for j in ac_matrix])

    return min_num_servers, constraints

def server_capacity_constraints(V, S):
    constraints = []

    for server, s in S.items():
        for v in V.values():
            constraints += [If(v == server.id, s(v) == 1, s(v) == 0)]

        constraints += [Sum([s(v) * vm.cpu_req for vm, v in V.items()]) <= server.cpu_cap,
                        Sum([s(v) * vm.ram_req for vm, v in V.items()]) <= server.ram_cap]

    return constraints

def cantor_pairing(a, b):
    return 0.5 * (a + b) * (a + b + 1) + b

def server_symmetry_breaking_constraints(V, S, mode='safe'):
    key = lambda s: cantor_pairing(s.cpu_cap, s.ram_cap)

    equals = [list(g) for _, g in groupby(sorted(S.keys(), key=key), key)]

    # This is the set of sets of servers that are equal to each other.
    equals = [x for x in equals if len(x) > 1]

    jobs      = [list(g) for _, g in groupby(V.keys(), lambda v: v.job_id)]
    ac_matrix = [[V[vm] for vm in job if vm.anti_collocation] for job in jobs]

    # key_vm = lambda vm: cantor_pairing(vm.cpu_req, vm.ram_req)
    # vm_equals = [list(g) for _, g in groupby(sorted(V.keys(), key=key_vm), key_vm)]
    # vm_equals_jobs = [[list(g) for _, g in groupby(sorted(vm_eq, 
    #                                                       key=lambda vm: vm.job_id))] 
    #                   for vm_eq in vm_equals]
    # vm_equals = [[vs[0] for vs in vss] for vss in vm_equals_jobs]

    # # This is the set of sets of vms that are equal to each other but belong to
    # # a different job.
    # vm_equals = [x for x in vm_equals if len(x) > 1]
    # v_equals = [[V[vm] for vm in vms] for vms in vm_equals]

    # print(v_equals)
    # sys.exit('vm_equals')

    # vm_equals = [x for x in equals if len(x) > 1]

    constraints = []

    if mode == 'safe':
        for job in ac_matrix:
            v = job[0] # 0 is random
            # v = list(max(v_equals, key=len))[0]
            for ss in equals:
                for s in ss[1:]: # 1 is random
                    constraints.append(v != s.id)
    elif mode == 'unsafe':
        for job in ac_matrix:
            for i, v in enumerate(job):
                for ss in equals:
                    for s in ss[:i] + ss[i+1:]:
                        constraints.append(v != s.id)
    else:
        raise RuntimeError('mode must be either \'safe\' or \'unsafe\'')
    return constraints

def assignment_from_model(servers, V, model):
    """
    Returns a dictionary of (s, vms_) pairs, where vms_ are the virtual machines
    assigned to server s.
    """
    assignment_ = [[] for s in servers]

    for vm, v in V.items():
        assignment_[model[v].as_long()] += [vm]

    assignment = {s : assignment_[s.id] for s in servers if assignment_[s.id]}
    return assignment

def solve(servers, vms):
    #---------------------------------------------------------------------------
    # Constraints
    #---------------------------------------------------------------------------

    V = {vm : Int('vm{}'.format(vm.id)) for vm in vms}
    S = {s : Function('s{}'.format(s.id), IntSort(), IntSort()) for s in servers}

    formula = []
    formula += cardinality_constraints(V, S)

    min_num_servers, cs = anti_collocation_constraints(V)
    formula += cs

    formula += server_capacity_constraints(V, S)

    formula += server_symmetry_breaking_constraints(V, S, mode='safe')

    on = Function('on', IntSort(), IntSort())

    for server, s in S.items():
        formula.append(If(Sum([s(v) for v in V.values()]) >= 1, 
                          on(server.id) == 1, on(server.id) == 0))

    #---------------------------------------------------------------------------
    # Search
    #---------------------------------------------------------------------------

    # Some redundant clauses to make it faster
    formula.append(Sum([on(s.id) * s.cpu_cap for s in S]) >= sum([v.cpu_req for v in V]))
    formula.append(Sum([on(s.id) * s.ram_cap for s in S]) >= sum([v.ram_req for v in V]))

    solver = Solver()
    solver.add(formula)

    for num_servers in range(min_num_servers, len(servers) + 1):
        solver.push()
        solver.add(Sum([on(s.id) for s in servers]) == num_servers)

        result = solver.check()
        if result == unknown:
            raise Z3Exception("Bug: unknown")
        elif result == sat:
            return assignment_from_model(servers, V, solver.model())
        solver.pop()

        print("Finished iteration with number of servers = {}".format(num_servers))

    return None

def main(file_name=''):
    if (file_name == ''):
        print("USAGE: proj2 <scenario-file-name>")
        return

    servers, vms = get_problem(file_name)
    assignment = solve(servers, vms)

    if assignment is None:
        print('Bug: Found no solution.')
        return

    server_dict = {vm: s for s in assignment for vm in assignment[s]}

    for s in assignment.keys():
        for vm in assignment[s]:
            server_dict[vm] = s

    num_servers = len([s for s in assignment if assignment[s]])

    print('o {}'.format(num_servers))
    for vm in vms:
        print('{} {} -> {}'.format(vm.job_id, vm.vm_index, server_dict[vm].id))

if __name__ == "__main__":
    main(get_file_name())
