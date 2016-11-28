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

% max number of anti-collocation vms per job
servers: min_num_servers;

% number of servers turned on (that is what we want to find out)
var min_num_servers..num_servers: on_count;

predicate on(servers: s) = (cpu_load[s] != 0);

% ------------------------------------------------------------------------------
% Constraints
% ------------------------------------------------------------------------------

constraint on_count = sum (s in servers) (on(s));

constraint forall (s in servers) (cpu_load[s] = sum (v in vms where place[v] = s) (vcpu[v]));
constraint forall (s in servers) (ram_load[s] = sum (v in vms where place[v] = s) (vram[v]));

% Servers capacities cannot be exceeded.
constraint forall (s in servers) (cpu_load[s] <= scpu[s]);
constraint forall (s in servers) (ram_load[s] <= sram[s]);

% Anti-collocation
constraint forall (v1 in vms where vac[v1])
  (forall (v2 in vms where vac[v2] /\ vjob[v1] = vjob[v2] /\ v1 != v2)
    (place[v1] != place[v2]));

% ------------------------------------------------------------------------------
% Redundant Constraints
% ------------------------------------------------------------------------------

constraint sum (v in vms) (vcpu[v]) = sum (s in servers) (cpu_load[s]);
constraint sum (v in vms) (vram[v]) = sum (s in servers) (ram_load[s]);

constraint sum (s in servers) (scpu[s]) >= sum (v in vms) (vcpu[v]);
constraint sum (s in servers) (sram[s]) >= sum (v in vms) (vram[v]);

constraint forall (s1 in servers)
  (forall (s2 in servers where (scpu[s1] <  scpu[s2] /\ sram[s1] <= sram[s2]) \/
                               (scpu[s1] <= scpu[s2] /\ sram[s1] <  sram[s2]))
    (on(s1) -> on(s2)));

% ------------------------------------------------------------------------------
% Solve
% ------------------------------------------------------------------------------

solve :: int_search([on_count], first_fail, indomain_min, complete)
      minimize on_count;

output["o " ++ show(on_count) ++ "\n"] ++
      [show(vjob[v]) ++ " " ++ show(vindex[v]) ++ " -> "++
       show(sid[place[v]]) ++ "\n" | v in vms];
