% ------------------------------------------------------------------------------
% Variables
% ------------------------------------------------------------------------------

int: num_servers;
set of int: servers = 1..num_servers;

array[servers] of int: sid;
array[servers] of int: scpu;
array[servers] of int: sram;

% ------------------------------------------------------------------------------

int: num_vms;
set of int: vms = 1..num_vms;

array[vms] of int: vjob;
array[vms] of int: vindex;
array[vms] of int: vcpu;
array[vms] of int: vram;
array[vms] of bool: vac;

% ------------------------------------------------------------------------------

% place[i] is the server where vm i is placed.
array[vms] of var servers: place;

% cpu_load[i] is the load of server i
array[servers] of var int: cpu_load;

% ram_load[i] is the load of server i
array[servers] of var int: ram_load;

% ------------------------------------------------------------------------------

predicate on(servers: s) = (cpu_load[s] != 0);
servers: on_count;
