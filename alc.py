#!/usr/bin/env python3

import pdb

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
            return self.cpu_cap == other.cpu_cap \
               and self.ram_cap == other.ram_cap
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
            return self.cpu_req == other.cpu_req \
               and self.ram_req == other.ram_req \
               and self.anti_collocation == other.anti_collocation
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
    # FIXME: experiment
    # vms = list(filter(lambda vm: vm.cpu_req != 1 or vm.ram_req != 1, vms))

    return servers, vms

def cardinality_constraints(servers, vms, V):
    return [And(0 <= V[vm], V[vm] < len(servers)) for vm in vms]

def anti_collocation_constraints(servers, vms, V):
    num_jobs = len({vm.job_id for vm in vms})
    ac_matrix = [[] for _ in range(num_jobs)]

    for vm in vms:
        if(vm.anti_collocation):
            ac_matrix[vm.job_id].append(V[vm])

    constraints     = [Distinct(j) for j in ac_matrix if j]
    min_num_servers = max([len(j) for j in ac_matrix])

    return min_num_servers, constraints

def server_capacity_constraints(servers, vms, V, S):
    constraints = []

    for s in servers:
        for vm in vms:
            constraints += [If(V[vm] == s.id,
                               S[s](V[vm]) == 1,
                               S[s](V[vm]) == 0)]

        cpu_cons = (Sum([S[s](V[vm]) * vm.cpu_req for vm in vms]) <= s.cpu_cap)
        ram_cons = (Sum([S[s](V[vm]) * vm.ram_req for vm in vms]) <= s.ram_cap)
        constraints += [cpu_cons, ram_cons]

    return constraints

def assign(servers, simple_vms, partial_assignment):
    servers_ = [deepcopy(s) for s in partial_assignment.keys()]

    for s in servers_:
        for vm in partial_assignment[s]:
            s.cpu_cap -= vm.cpu_req
            s.ram_cap -= vm.ram_req

    key = lambda s: min(s.cpu_cap, s.ram_cap)

    # Is there enough space?
    if sum(key(s) for s in servers_) < len(simple_vms):
        return None

    servers_ = sorted(servers, key=key, reverse=True)

    i = 0
    full_assignment = {s : [] for s in servers_}

    for s in servers_:
        full_assignment[s] = simple_vms[i:i + key(s)]
        i += key(s)

    return full_assignment

def assignment_from_model(servers, vms, V, model):
    """
    Returns a dictionary of (s, vms_) pairs, where vms_ are the virtual machines
    assigned to server s.
    """
    assignment_ = [[]] * len(servers)

    for vm, v in V.items():
        assignment_[model[v].as_long()] += [vm]

    assignment = {s : assignment_[s.id] for s in servers if assignment_[s.id]}
    return assignment

def solve(servers, vms):
    key = lambda vm: vm.cpu_req != 1 or vm.ram_req != 1

    complex_vms = list(filter(key, vms))

    if not complex_vms:
        # The problem can be solved with a polynomial solution.

        jobs            = [list(g) for _, g in groupby(vms, lambda v: v.job_id)]
        ac_matrix       = [list(filter(lambda vm: vm.anti_collocation, j)) for j in jobs]
        min_num_servers = max(map(len, ac_matrix))

        servers = sorted(servers, key=lambda s: min(s.cpu_cap, s.ram_cap), reverse=True)

        for num_servers in range(min_num_servers, len(servers) + 1):
            assignment = {s : [] for s in servers[0:num_servers]}
            assignment = assign(servers, vms, assignment)

            if assignment is not None:
                return assignment
        # Bug.
        return None

    simple_vms = list(filterfalse(key, vms))

    V = {vm : Int('VM{}'.format(vm.id)) for vm in complex_vms}
    S = {s : Function('s{}'.format(s.id), IntSort(), IntSort()) for s in servers}

    # FIXME: Do we really need this?
    f = Function('f', IntSort(), IntSort())

    solver = Solver()


    # 1. Solve for "complex" VMs
    solver.add(cardinality_constraints(servers, complex_vms, V))

    min_num_servers, constraints = anti_collocation_constraints(servers, complex_vms, V)
    solver.add(constraints)

    solver.add(server_capacity_constraints(servers, complex_vms, V, S))

    for s in servers:
        solver.add(If(Sum([S[s](v) for _, v in V.items()]) >= 1,
                      f(s.id) == 1,
                      f(s.id) == 0))

    model = None
    full_assignment = None
    for num_servers in reversed(range(1, len(servers) + 1)):
        solver.push()

        solver.add(Sum([f(s.id) for s in servers]) <= num_servers)

        if solver.check() == unsat:
            break

        while solver.check() == sat:
            # Check if the solution holds when adding the "simple" VMs.
            model = solver.model()
            partial_assignment = assignment_from_model(servers, vms, V, model)
            assignment_ = assign(servers, simple_vms, partial_assignment)

            if assignment_ is None:
                # Doesn't hold, which implies that the problem may be (!) unsat.
                solver.add(Or([v != model[v] for _, v in V.items()]))
            else:
                # Its sat, but maybe there is a better solution.
                full_assignment = assignment_
                break
        print("Finished iteration with |S| = {}".format(num_servers))

        solver.pop()

    return full_assignment

def main():
    pdb.set_trace()

    # file_name = get_file_name()
    file_name = 'input/01.in'

    if (file_name == ""):
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
    main()
