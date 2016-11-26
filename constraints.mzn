include "variables.mzn";

% ------------------------------------------------------------------------------
% Constraints

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

constraint sum (v in vms) (vcpu[v]) = sum (s in servers) (cpu_load[s]);
constraint sum (v in vms) (vram[v]) = sum (s in servers) (ram_load[s]);

constraint sum (s in servers) (scpu[s]) >= sum (v in vms) (vcpu[v]);
constraint sum (s in servers) (sram[s]) >= sum (v in vms) (vram[v]);

% constraint forall (v in vms) (forall (s in servers) (vcpu[v] > scpu[s] -> place[v] != s));
% constraint forall (v in vms) (forall (s in servers) (vram[v] > sram[s] -> place[v] != s));

% Fast
constraint forall (s1 in servers)
  (forall (s2 in servers where (scpu[s1] <  scpu[s2] /\ sram[s1] <= sram[s2]) \/
                               (scpu[s1] <= scpu[s2] /\ sram[s1] <  sram[s2]))
    (on(s1) -> on(s2)));
