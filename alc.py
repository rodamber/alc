#!/usr/bin/env python3
# encoding: utf-8

from itertools import *
import os
import subprocess
import sys
import tempfile

from dzn import *

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
        for _ in range(num_servers):
            server_id, cpu_cap, ram_cap = [int(x) for x in f.readline().split()]
            servers += [server(server_id, cpu_cap, ram_cap)]
        num_vms = int(f.readline())
        for vm_id in range(num_vms):
            line = f.readline().split()
            job_id, vm_index, cpu_req, ram_req = [int(x) for x in line[:-1]]
            anti_collocation = (line[-1] == "True")
            vms += [virtual_machine(vm_id, job_id, vm_index, cpu_req,
                                    ram_req, anti_collocation)]
    return servers, vms

def minizinc_cmd(model_file_name, data):
    executable = './MiniZinc/minizinc'
    solution_sep = '--solution-separator ""'
    search_complete_msg = '--search-complete-msg ""'
    unsat_msg = '--unsat-msg "unsat"'

    return ' '.join([executable, solution_sep, search_complete_msg, unsat_msg,
                     model_file_name, '-D "{}"'.format(data)])

def min_num_servers(vms):
    jobs            = [list(g) for _, g in groupby(vms, lambda v: v.job_id)]
    ac_matrix       = [[vm for vm in job if vm.anti_collocation] for job in jobs]
    min_num_servers = max([len(j) for j in ac_matrix])

    return min_num_servers

def solve(csp, data):
    import stdchannel

    cmd = minizinc_cmd(csp, data)
    with stdchannel.redirect(sys.stderr, os.devnull):
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')

        # print('output={}'.format(output))
        if output[:5] != 'unsat': # sat
            return True, output[:-2]
        else:
            return False, output

def satisfy(problem, on_count=None):
    if on_count is None:
        on_count = len(problem[0])
    data = problem2dzn(problem, on_count)
    return solve('satisfy.mzn', data)

def minimize(problem):
    data = problem2dzn(problem, type='minimize')
    return solve('minimize.mzn', data)

def main(file_name=''):
    if (file_name == ''):
        print("USAGE: proj3 <scenario-file-name>")
        return

    servers, vms = get_problem(file_name)

    sat, output = minimize((servers, vms))
    if sat: print(output)

    # Search
    # sat = False
    # for num_servers in range(min_num_servers(vms), len(servers) + 1):
    #     print('num_servers={}'.format(num_servers))

    #     print('--------------0--------------')
    #     ss = sorted(servers, key=lambda s: s.ram_cap, reverse=True)[:num_servers]
    #     print('servers={}'.format([s.id for s in ss]))

    #     sat, output = satisfy((ss, vms))
    #     if sat:
    #         print(output)
    #         print('=== Good call!')
    #         break

    #     # print('--------------1--------------')
    #     # ss = sorted(servers, key=lambda s: s.cpu_cap, reverse=True)[:num_servers]
    #     # print('servers={}'.format([s.id for s in ss]))

    #     # sat, output = satisfy((ss, vms))
    #     # if sat:
    #     #     print(output)
    #     #     print('=== Good call!')
    #     #     break

    #     print('--------------2--------------')
    #     sat, output = satisfy((servers, vms), num_servers)
    #     if sat:
    #         print(output)
    #         break


if __name__ == "__main__":
    main(get_file_name())
