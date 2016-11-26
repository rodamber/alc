#!/usr/bin/env python3
# encoding: utf-8

from alc import *

def list2array1d(name, xs):
    return name + ' = [' + ', '.join([str(x) for x in xs]) + '];'

def servers2dzn(servers):
    num_servers = 'num_servers = {};'.format(len(servers))
    sid  = list2array1d('sid',  [s.id      for s in servers])
    scpu = list2array1d('scpu', [s.cpu_cap for s in servers])
    sram = list2array1d('sram', [s.ram_cap for s in servers])
    return '\n'.join([num_servers, sid, scpu, sram])

def vms2dzn(vms):
    num_vms = 'num_vms = {};'.format(len(vms))
    vjob   = list2array1d('vjob',   [vm.job_id   for vm in vms])
    vindex = list2array1d('vindex', [vm.vm_index for vm in vms])
    vcpu   = list2array1d('vcpu',   [vm.cpu_req  for vm in vms])
    vram   = list2array1d('vram',   [vm.ram_req  for vm in vms])
    vac    = list2array1d('vac',    ['true' if vm.anti_collocation else 'false' 
                                                 for vm in vms])
    return '\n'.join([num_vms, vjob, vindex, vcpu, vram, vac])

def min_num_servers(vms):
    jobs            = [list(g) for _, g in groupby(vms, lambda v: v.job_id)]
    ac_matrix       = [[vm for vm in job if vm.anti_collocation] for job in jobs]
    min_num_servers = max([len(j) for j in ac_matrix])

    return min_num_servers

def problem2dzn(problem, on_count=None, type='satisfy'):
    if on_count is None:
        on_count = len(problem[0])

    servers, vms = problem
    on = 'on_count = {};'.format(on_count)
    mns = 'min_num_servers = {};'.format(min_num_servers(vms))

    return '\n\n'.join([servers2dzn(servers), vms2dzn(vms), mns] + \
                       ([on] if type == 'satisfy' else []))

if __name__ == "__main__":
    print(problem2dzn(get_problem(get_file_name())))
