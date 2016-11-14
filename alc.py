#!/usr/bin/env python3

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
        return false

    def __str__(self):
        template = '{{id: {}, cpu_cap: {}, ram_cap: {}}}'
        return template.format(self.id, self.cpu_cap, self.ram_cap)

    def __repr__(self):
        return str(self)

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

    def __str__(self):
        template = '{{job_id: {}, vm_index: {}, cpu_req: {}, ram_req: {}, ac: {}}}'
        return template.format(self.job_id, self.vm_index, self.cpu_req,
                               self.ram_req, self.anti_collocation)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return (self.job_id * self.vm_index * self.cpu_req) % self.ram_req

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
    return [And(0 <= V[vm.id], V[vm.id] < len(servers)) for vm in vms]

def anti_collocation_constraints(servers, vms, V):
    num_jobs = len({vm.job_id for vm in vms})
    ac_matrix = [[] for _ in range(num_jobs)]

    for vm in vms:
        if(vm.anti_collocation):
            ac_matrix[vm.job_id].append(V[vm.id])
    
    constraints     = [Distinct(j) for j in ac_matrix if j]
    min_num_servers = max([len(l) for l in ac_matrix])

    return min_num_servers, constraints

def server_capacity_constraints(servers, vms, V, S):
    constraints = []

    for s in servers:
        for vm in vms:
            constraints += [If(V[vm.id] == s.id, 
                               S[s.id](V[vm.id]) == 1, 
                               S[s.id](V[vm.id]) == 0)]
    
        cpu_cons = (Sum([S[s.id](V[vm.id]) * vm.cpu_req for vm in vms]) 
                    <= servers[s.id].cpu_cap)
        ram_cons = (Sum([S[s.id](V[vm.id]) * vm.ram_req for vm in vms]) 
                    <= servers[s.id].ram_cap)
        constraints += [cpu_cons, ram_cons]

    return constraints

def solve(servers, vms):
    V = [Int('VM{}'.format(vm.id)) for vm in vms]
    S = [Function('s{}'.format(s.id), IntSort(), IntSort()) for s in servers]
    f = Function('f', IntSort(), IntSort())

    solver = Solver()

    #---------------------------------------------------------------------------
    # Search

    # complex_vms = list(filter(lambda vm: vm.cpu_req != 1 or vm.ram_req != 1, vms))
    # simple_vms = list(set(vms) - set(complex_vms))

    # solver.push()

    # # 1. Solve for "complex" VMs
    # solver.add(cardinality_constraints(servers, complex_vms, V))

    # min_num_servers, constraints = anti_collocation_constraints(servers, complex_vms, V)
    # solver.add(constraints)

    # solver.add(server_capacity_constraints(servers, complex_vms, V, S))

    # solver.push()
    # # 2. Check if the solution holds when adding the "simple" VMs
    # solver.pop()
    # # 3. If not, negate the model resulting from step 1 and add it to the solver as
    # #    a constraint. Go back to step 1.
    # # 4. If yes, try again for another (better) number of servers.
    # solver.pop()

    #---------------------------------------------------------------------------
    # Cardinality constraints
    solver.add(cardinality_constraints(servers, vms, V))

    #---------------------------------------------------------------------------
    # Anti-collocation constraints
    min_num_servers, constraints = anti_collocation_constraints(servers, vms, V)
    for c in constraints: solver.add(c)
   
    #---------------------------------------------------------------------------
    # Server capacity constraints
    solver.add(server_capacity_constraints(servers, vms, V, S))

    for s in servers:
        solver.add(If(Sum([S[s.id](v) for v in V]) >= 1, 
                      f(s.id) == 1, 
                      f(s.id) == 0))
        
    model = None
    for num_servers in reversed(range(1, len(servers) + 1)):
        solver.push()
        solver.add(Sum([f(s.id) for s in servers]) <= num_servers)

        solution = solver.check()
        if solution == unsat:
            server_dict = {vm : model[v] for vm, v in zip(vms, V)}
            return num_servers + 1, server_dict
        elif solution == sat:
            model = solver.model()
            solver.pop()
            print("Finished iteration with |S| = {}".format(num_servers))
        else:
            return None

    return None


    #---------------------------------------------------------------------------
    # Cardinality constraints
    # solver.add(cardinality_constraints(servers, vms, V))

    #---------------------------------------------------------------------------
    # Anti-collocation constraints
    # min_num_servers, constraints = anti_collocation_constraints(servers, vms, V)
    # for c in constraints: solver.add(c)
   
    #---------------------------------------------------------------------------
    # Server capacity constraints
    # solver.add(server_capacity_constraints(servers, vms, V, S))

def main():
    file_name = get_file_name()  

    if (file_name == ""):
        print("USAGE: proj2 <scenario-file-name>")
        return

    servers, vms = get_problem(file_name)
    result = solve(servers, vms)

    if result is None:
        print('Bug: Found no solution.')
        return

    num_servers, server_dict = result

    print('o {}'.format(num_servers))
    for vm in vms:
        print('{} {} -> {}'.format(vm.job_id, vm.vm_index, server_dict[vm]))

if __name__ == "__main__":
    main()
