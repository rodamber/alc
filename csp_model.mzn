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
% Constraints
% ------------------------------------------------------------------------------

predicate on(servers: s) = (cpu_load[s] != 0);

var servers: on_count = sum (s in servers) (bool2int(on(s)));

% constraint on_count = 14;

constraint forall (s in servers) (cpu_load[s] = sum (v in vms where place[v] = s) (vcpu[v]));
constraint forall (s in servers) (ram_load[s] = sum (v in vms where place[v] = s) (vram[v]));

% Servers capacities cannot be exceeded.
constraint forall (s in servers) (cpu_load[s] <= scpu[s]);
constraint forall (s in servers) (ram_load[s] <= sram[s]);

% Anti-collocation
constraint forall (v1 in vms where vac[v1])
  (forall (v2 in vms where vac[v2] /\ vjob[v1] = vjob[v2] /\ v1 != v2)
    (place[v1] != place[v2]));

% Redundant constraints.
constraint sum (v in vms) (vcpu[v]) = sum (s in servers) (cpu_load[s]);
constraint sum (v in vms) (vram[v]) = sum (s in servers) (ram_load[s]);

constraint sum (s in servers where on(s)) (scpu[s]) >= sum (v in vms) (vcpu[v]);
constraint sum (s in servers where on(s)) (sram[s]) >= sum (v in vms) (vram[v]);

% ------------------------------------------------------------------------------
% Solve 
% ------------------------------------------------------------------------------

solve minimize on_count;
% solve satisfy;

output["o " ++ show(on_count) ++ "\n"] ++
      [show(vjob[v]) ++ " " ++ show(vindex[v]) ++ " -> "++
       show(sid[place[v]]) ++ "\n" | v in vms];