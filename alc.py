#!/usr/bin/env python3
# encoding: utf-8

from itertools import *
import os
import subprocess
import sys
import tempfile

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

def problem2dzn(problem, heuristic=''):

    def sid2dzn(servers):
        lid = [s.id for s in servers]

        sid = 'sid = ['
        for ix in lid:
            sid += '{}, '.format(ix)
        sid += '];'

        return sid

    def server_to_list(srv):
        return [srv.cpu_cap, srv.ram_cap]

    def vm_to_list(vm):
        return [vm.job_id, vm.vm_index, vm.cpu_req, vm.ram_req, int(vm.anti_collocation)]

    def dzn_array2d(lst, padding=''):
        res = '['
        for i, row in enumerate(lst):
            res += ('' if i == 0 else padding) + '| '
            for col in row:
                res += '{}, '.format(col)
            res += '\n'
        res += padding + '|];'

        return res

    servers, vms = problem
    lines = []

    lines.append("nServers = {};".format(len(servers)))
    lines.append("nVMs = {};".format(len(vms)))

    ss = None
    if heuristic == '':
        ss = servers
    elif heuristic == 'cpu':
        ss = sorted(servers, key=lambda s: s.cpu_cap, reverse=True)
    elif heuristic == 'ram':
        ss = sorted(servers, key=lambda s: s.ram_cap, reverse=True)
    else:
        raise ValueError('heuristic must be empty, cpu or ram')


    servers_list = [server_to_list(srv) for srv in ss]
    vms_list = [vm_to_list(vm) for vm in vms]

    lines.append(sid2dzn(ss))
    lines.append('servers = ' + dzn_array2d(servers_list, padding='           '))
    lines.append('vms = ' + dzn_array2d(vms_list, padding='       '))

    return "\n".join(lines)

def solve(csp_model, data):
    import stdchannel

    tf = tempfile.NamedTemporaryFile(mode='w', suffix='.mzn', delete=False)
    tf.write(csp_model)
    csp_model_file_name = tf.name
    tf.close()

    cmd = "./MiniZinc/minizinc --solution-separator \"\" --search-complete-msg \"\" " + \
        "{model} -D \"{dzn}\"".format(model=csp_model_file_name, dzn=data)

    with stdchannel.redirect(sys.stderr, os.devnull):
        output = subprocess.check_output(cmd, shell=True)
        os.remove(csp_model_file_name)

        if output != b'=====UNSATISFIABLE=====\n': # sat
            return True, output.decode('utf-8')[:-2]
        else:
            return False, output.decode('utf-8')


def min_num_servers(vms):
    jobs            = [list(g) for _, g in groupby(vms, lambda v: v.job_id)]
    ac_matrix       = [[vm for vm in job if vm.anti_collocation] for job in jobs]
    min_num_servers = max([len(j) for j in ac_matrix])

    return min_num_servers

def main(file_name=''):
    if (file_name == ''):
        print("USAGE: proj3 <scenario-file-name>")
        return

    f = open("csp_model.mzn.template")
    template = f.read()
    f.close()

    myheuristic = 'ram'
    servers, vms = get_problem(file_name)
    data = problem2dzn((servers, vms), heuristic=myheuristic)

    # Search
    sat = False
    for num_servers in range(min_num_servers(vms), len(servers) + 1):
        csp_model = template

        if myheuristic == '':
            csp_model = template.format(heuristic='', num_servers=num_servers)
        elif myheuristic in ['cpu', 'ram']:
            constraint = 'constraint forall (s in 1..{}) (on[s] == true);'.format(num_servers)
            csp_model = template.format(heuristic=constraint, num_servers=num_servers)
        else:
            raise ValueError("c'mon, give me a good heuristic")

        print('--------------0--------------')
        print('num_servers={}'.format(num_servers))
        print('servers={}'.format([s.id for s in sorted(servers, key=lambda s: s.ram_cap, reverse=True)][:num_servers]))

        sat, output = solve(csp_model, data)

        if sat:
            print(output)
            break

        print('--------------1--------------')

        csp_model = template.format(heuristic='', num_servers=num_servers)
        sat, output = solve(csp_model, data)

        if sat:
            print(output)
            break




if __name__ == "__main__":
    main(get_file_name())
