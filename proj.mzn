int: nServers;
int: nVMs;

set of int: Servers = 1..nServers;
set of int: VMs     = 1..nVMs;

array[Servers, 1..2] of int: servers;
array[VMs, 1..5]     of int: vms;

int: vjob   = 1; % job id
int: vindex = 2; % job index
int: vcpu   = 3; % cpu_req
int: vram   = 4; % ram_req
int: vac    = 5; % anti-collocation

int: scpu = 1; % cpu_cap
int: sram = 2; % ram_cap

% assignment[i] is the set of ids of the VMs assigned to server i.
array[VMs] of var int: assignment;

% on[i] is true if server i is on and false otherwise.
array[Servers] of var bool: on;

% on[i] is true if server i is on and false otherwise.
% constraint forall (vid in VMs) (on[assignment[vid]] == true);
constraint forall (sid in Servers)
  (on[sid] = exists (vid in VMs) (assignment[vid] == sid));

% Each VM is assigned to exactly one server.
constraint forall (vid in VMs) (assignment[vid] in Servers);

% Servers capacities cannot be exceeded.
constraint forall (sid in Servers)
  ((sum (vid in VMs where assignment[vid] == sid) (vms[vid, vcpu])) <= servers[sid, scpu]);
constraint forall (sid in Servers)
  ((sum (vid in VMs where assignment[vid] == sid) (vms[vid, vram]) <= servers[sid, sram]));
  
% Anti-collocation constraints.
constraint
  forall (vid1 in VMs where vms[vid1, vac] == 1)
    (forall (vid2 in VMs where vid1 != vid2 /\ vms[vid1, vjob] == vms[vid2, vjob])
      ((vms[vid2, vac] == 1) -> assignment[vid1] != assignment[vid2]));

% Redundant constraints.
constraint sum (sid in Servers) (bool2int(on[sid]) * servers[sid, scpu]) >= 
           sum (vid in VMs) (vms[vid, vcpu]);
constraint sum (sid in Servers) (bool2int(on[sid]) * servers[sid, sram]) >= 
           sum (vid in VMs) (vms[vid, vram]);

% Heuristic (not optimal!)
% If a server is on then all the servers with more ram must be on too.
constraint forall (sid1 in Servers where on[sid1])
  (forall (sid2 in Servers where servers[sid1, sram] < servers[sid2, sram])
    (on[sid2]));
      

solve minimize (sum (sid in Servers) (bool2int(on[sid])));

output["o " ++ show(sum (s in Servers) (bool2int(on[s]))) ++ "\n"] ++
      [show(vms[vid, vjob]) ++ " " ++ show(vms[vid, vindex]) ++ " -> "++
       show(assignment[vid] - 1) ++ "\n" | vid in VMs];
