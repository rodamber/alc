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

def cardinality_constraints(servers, vms, V):
    return [And(0 <= V[vm], V[vm] < len(servers)) for vm in vms]

def anti_collocation_constraints(servers, vms, V):
    jobs            = [list(g) for _, g in groupby(vms, lambda v: v.job_id)]
    ac_matrix       = [[V[vm] for vm in job if vm.anti_collocation] for job in jobs]

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

def assign(simple_vms, partial_assignment):
    if not simple_vms:
        return partial_assignment

    servers_ = [deepcopy(s) for s in partial_assignment]

    for s in servers_:
        for vm in partial_assignment[s]:
            s.cpu_cap -= vm.cpu_req
            s.ram_cap -= vm.ram_req

    key = lambda s: min(s.cpu_cap, s.ram_cap)

    # Is there enough space?
    if sum(key(s) for s in servers_) < len(simple_vms):
        return None

    servers_ = sorted(servers_, key =key, reverse =True)

    ac_vms = sorted([vm for vm in simple_vms if vm.anti_collocation], 
                    key=lambda v: v.job_id)
    ac_matrix = [list(g) for _, g in groupby(ac_vms, lambda v: v.job_id)]
    ac_vms = [x for job in sorted(ac_matrix, key=len, reverse=True) for x in job]

    not_ac_vms = [vm for vm in simple_vms if not vm.anti_collocation]
    vms_       = ac_vms + not_ac_vms 

    full_assignment = {s : partial_assignment[s] for s in servers_}

    for vm in vms_:
        placed = True

        for s in full_assignment:
            if place(vm, s, full_assignment) is not None:
                break
        else:
            placed = False

        if placed == False:
            return None

    return full_assignment

def place(vm, server, assignment):
    assert(vm.cpu_req == vm.ram_req == 1)

    if vm in assignment[server]:
        return None
    elif server.cpu_cap == 0 or server.ram_cap == 0:
        return None
    elif vm.anti_collocation and \
         [v for v in assignment[server] if v.job_id == vm.job_id and v.anti_collocation]:
        return None
    else:
        assignment[server] += [vm]
        server.cpu_cap -= 1
        server.ram_cap -= 1
        return assignment

def assignment_from_model(servers, vms, V, model):
    """
    Returns a dictionary of (s, vms_) pairs, where vms_ are the virtual machines
    assigned to server s.
    """
    assignment_ = [[] for s in servers]

    for vm, v in V.items():
        assignment_[model[v].as_long()] += [vm]

    assignment = {s : assignment_[s.id] for s in servers if assignment_[s.id]}
    return assignment

def basic_solve(servers, vms):
    jobs            = [list(g) for _, g in groupby(vms, lambda v: v.job_id)]
    ac_matrix       = [list(filter(lambda vm: vm.anti_collocation, j)) for j in jobs]
    min_num_servers = max(map(len, ac_matrix))

    servers = sorted(servers, key=lambda s: min(s.cpu_cap, s.ram_cap), reverse=True)

    for num_servers in range(min_num_servers, len(servers) + 1):
        assignment = assign(vms, {s: [] for s in servers[0:num_servers]})

        if assignment is not None:
            return assignment
    return None

def solve(servers, vms):
    key         = lambda vm: vm.cpu_req != 1 or vm.ram_req != 1
    complex_vms = list(filter(key, vms))

    if not complex_vms:
       return basic_solve(servers, vms)

    simple_vms = list(filterfalse(key, vms))

    #---------------------------------------------------------------------------

    V = {vm : Int('VM{}'.format(vm.id)) for vm in complex_vms}
    S = {s : Function('s{}'.format(s.id), IntSort(), IntSort()) for s in servers}

    # FIXME: Do we really need this?
    f = Function('f', IntSort(), IntSort())

    #---------------------------------------------------------------------------

    solver = Solver()

    solver.add(cardinality_constraints(servers, complex_vms, V))

    min_num_servers, constraints = anti_collocation_constraints(servers, complex_vms, V)
    solver.add(constraints)

    solver.add(server_capacity_constraints(servers, complex_vms, V, S))

    for s in servers:
        solver.add(If(Sum([S[s](v) for _, v in V.items()]) >= 1,
                      f(s.id) == 1,
                      f(s.id) == 0))

    #---------------------------------------------------------------------------

    model = None
    assignment = None
    for num_servers in range(min_num_servers, len(servers) + 1):
        solver.push()

        # FIXME: <= or == ?
        solver.add(Sum([f(s.id) for s in servers]) == num_servers)

        print('num_servers = {}'.format(num_servers))
        i = 0
        while solver.check() == sat:
            i += 1
            print('i = {}'.format(i))

            # Check if the solution holds when adding the "simple" VMs.
            model = solver.model()
            partial_assignment = assignment_from_model(servers, vms, V, model)

            # Is there enough space for the rest of the vms? If not, don't
            # bother continuing the loop.
            if not enough_space(simple_vms, partial_assignment):
                print('Ups. Not enough space (i = {})'.format(i))
                break

            assignment = assign(simple_vms, partial_assignment)

            if assignment is None:
                # Doesn't hold, which implies that the problem may be (!) unsat.
                solver.add(Or([v != model[v] for _, v in V.items()]))
            else:
                return assignment
        print("Finished iteration with |S| = {}".format(num_servers))

        solver.pop()

    # Bug.
    return None

def enough_space(vms, partial_assignment):
    servers_ = [deepcopy(s) for s in partial_assignment]

    for s in servers_:
        for vm in partial_assignment[s]:
            s.cpu_cap -= vm.cpu_req
            s.ram_cap -= vm.ram_req

    key = lambda s: min(s.cpu_cap, s.ram_cap)
    return sum(key(s) for s in servers_) < len(vms)



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
