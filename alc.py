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
    # print(problem)

    # servers = problem['servers']
    # vms = problem['vms']

    # Table of variables
    # vars = [[ Bool('x{}{}'.format(i, j)) for j in range(len(servers))] for i in range(len(vms))]
    # print(vars)
    # print(vars[0][1])
    # print(vars[1][2])

    # vm_is_in_server = Function('f', 
    #                            IntSort(),  # vm id
    #                            IntSort(),  # server id
    #                            BoolSort()) # is the vm running in this server?

    # vms = [Int('vm{}'.format(i)) for i in problem['vms']]
    # servers = [Int('server{}'.format(i)) for i in problem['servers']]

    # vm = Int('vm')
    # server = Int('server')






if __name__ == "__main__":
    main()
