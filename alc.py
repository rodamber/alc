#!/usr/bin/env python3

import sys
from z3 import *

class hardware:
    CPU = "CPU"
    RAM = "RAM"

class server:

    def __init__(self, id, cpu_cap, ram_cap):
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

    def __init__(self, job_id, vm_index, cpu_req, ram_req, anti_collocation):
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

    problem = {"servers": [], "vms": []}

    with open(file_name) as f:
        num_servers = int(f.readline())
        # print("num_servers = {}".format(num_servers))
        for _ in range(num_servers):
            server_id, cpu_cap, ram_cap = [int(x) for x in f.readline().split()]
            # print("server_id: {}, cpu_cap: {}, ram_cap: {}".format(server_id, cpu_cap, ram_cap))
            problem["servers"] += [server(server_id, cpu_cap, ram_cap)]
        num_vms = int(f.readline())
        # print("num_vms = {}".format(num_vms))
        for _ in range(num_vms):
            line = f.readline().split()
            job_id, vm_index, cpu_req, ram_req = [int(x) for x in line[:-1]]
            anti_collocation = (line[-1] == "True")
            # print("job_id: {}, vm_index: {}, cpu_req: {}, ram_req: {}, anti_collocation: {}".format(job_id, vm_index, cpu_req, ram_req, anti_collocation))
            problem["vms"] += [virtual_machine(job_id, vm_index, cpu_req,
                                              ram_req, anti_collocation)]
    # print(problem)
    return problem
    

def main():
    file_name = get_file_name()  

    if (file_name == ""):
        print("USAGE: proj2 <scenario-file-name>")
        return

    problem = get_problem(file_name)
    
    solver = Solver()
    
    servers = problem['servers']
    vms = problem['vms']
        
    #V = [Int('j%sv%s' %(vms[i].job_id, vms[i].vm_index)) for i in range(len(vms))]
    
    V = [Int('VM%s' %i) for i in range(len(vms))]
    
    #at-most-one/at-least-one
    at_cons = [ And(0 <= V[i], V[i] < len(servers)) for i in range(len(vms)) ]
    solver.add(at_cons)
    
    #anti-collocation
    num_jobs = vms[-1].job_id + 1
    ac_matrix = [[] for i in range(num_jobs)] #list of lists where no vm can be on the same server as other
    vm_index = 0
    
    print(num_jobs)
    
    for vm in vms:
        if(vm.anti_collocation):
            ac_matrix[vm.job_id].append(V[vm_index])
        
        vm_index += 1
    
    print(ac_matrix)
    
    for i in range(num_jobs):
        if(len(ac_matrix[i]) > 1):
            ac_cons = [Distinct(ac_matrix[i])]
            print(ac_cons)
            solver.add(ac_cons)
    
    #cardinality constraints
    S = [ Function('s%s' %i, IntSort(), IntSort()) for i in range(len(servers))]
    
    for j in range(len(servers)):
        for i in range(len(vms)):
            #not sure if it worked
            tmp = (If(V[i] == j, S[j](V[i]) == 1, S[j](V[i]) == 0))
            solver.add(tmp)
    
    for i in range(len(servers)):
        cpu_cons = (Sum([S[i](V[j]) * vms[j].cpu_req for j in range(len(vms))]) <= servers[i].cpu_cap)
        ram_cons = (Sum([S[i](V[j]) * vms[j].ram_req for j in range(len(vms))]) <= servers[i].ram_cap)
        
        solver.add(cpu_cons)
        solver.add(ram_cons)
        print(cpu_cons)
        print(ram_cons)
    
    if solver.check() == sat:
        print("Sat")
        m = solver.model()
        print (m)
        print("______________DEBUG_________________")
        print("______________SERVER0_________________")
        print(m.evaluate(S[0](V[0])))
        print(m.evaluate(S[0](V[1])))
        print(m.evaluate(S[0](V[2])))
        print(m.evaluate(S[0](V[3])))
        print(m.evaluate(S[0](V[4])))
        print(m.evaluate(S[0](V[5])))
        print(m.evaluate(S[0](V[6])))
        print(m.evaluate(S[0](V[7])))
        print("______________SERVER1_________________")
        print(m.evaluate(S[1](V[0])))
        print(m.evaluate(S[1](V[1])))
        print(m.evaluate(S[1](V[2])))
        print(m.evaluate(S[1](V[3])))
        print(m.evaluate(S[1](V[4])))
        print(m.evaluate(S[1](V[5])))
        print(m.evaluate(S[1](V[6])))
        print(m.evaluate(S[1](V[7])))
        print("______________SERVER2_________________")
        print(m.evaluate(S[2](V[0])))
        print(m.evaluate(S[2](V[1])))
        print(m.evaluate(S[2](V[2])))
        print(m.evaluate(S[2](V[3])))
        print(m.evaluate(S[2](V[4])))
        print(m.evaluate(S[2](V[5])))
        print(m.evaluate(S[2](V[6])))
        print(m.evaluate(S[2](V[7])))
        print("______________SERVER3_________________")
        print(m.evaluate(S[3](V[0])))
        print(m.evaluate(S[3](V[1])))
        print(m.evaluate(S[3](V[2])))
        print(m.evaluate(S[3](V[3])))
        print(m.evaluate(S[3](V[4])))
        print(m.evaluate(S[3](V[5])))
        print(m.evaluate(S[3](V[6])))
        print(m.evaluate(S[3](V[7])))
        print("________________END___________________")

    if solver.check() == unsat:
        print("Unsat")
    
if __name__ == "__main__":
    main()
