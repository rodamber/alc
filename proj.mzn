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

% This array allows us to give sorted server arrays to the model.
% sindex[ix] gives us the id of the servers whose index in array servers is ix
array[Servers] of int: sid;

int: scpu = 1; % cpu_cap
int: sram = 2; % ram_cap

% assignment[i] is the set of ids of the VMs assigned to server i.
array[VMs] of var int: assignment;

% on[i] is true if server i is on and false otherwise.
array[Servers] of var bool: on;

% on[i] is true if server i is on and false otherwise.
% constraint forall (vid in VMs) (on[assignment[vid]] == true);
constraint forall (s in Servers)
  (on[s] = exists (vid in VMs) (assignment[vid] == s));

% Each VM is assigned to exactly one server.
constraint forall (vid in VMs) (assignment[vid] in Servers);

% Servers capacities cannot be exceeded.
constraint forall (s in Servers)
  ((sum (vid in VMs where assignment[vid] == s) (vms[vid, vcpu])) <= servers[s, scpu]);
constraint forall (s in Servers)
  ((sum (vid in VMs where assignment[vid] == s) (vms[vid, vram]) <= servers[s, sram]));

% Anti-collocation constraints.
constraint
  forall (vid1 in VMs where vms[vid1, vac] == 1)
    (forall (vid2 in VMs where vid1 != vid2 /\ vms[vid1, vjob] == vms[vid2, vjob])
      ((vms[vid2, vac] == 1) -> assignment[vid1] != assignment[vid2]));

% Redundant constraints.
constraint sum (s in Servers) (bool2int(on[s]) * servers[s, scpu]) >=
           sum (vid in VMs) (vms[vid, vcpu]);
constraint sum (s in Servers) (bool2int(on[s]) * servers[s, sram]) >=
           sum (vid in VMs) (vms[vid, vram]);

% % Heuristic (not optimal!)
% % If a server is on then all the servers with more ram must be on too.
% constraint forall (s1 in Servers where on[s1])
%   (forall (s2 in Servers where servers[s1, sram] < servers[s2, sram])
%     (on[s2]));

% var int: maxid;
% constraint maxid in Servers /\ servers[maxid, sram] == max (s in Servers) (servers[s, sram]);
% constraint on[maxid];


solve minimize (sum (s in Servers) (bool2int(on[s])));
% solve :: bool_search(on, input_order, outdomain_max, complete)
      % minimize (sum (s in Servers) (bool2int(on[s])));

output["o " ++ show(sum (s in Servers) (bool2int(on[s]))) ++ "\n"] ++
      [show(vms[vid, vjob]) ++ " " ++ show(vms[vid, vindex]) ++ " -> "++
       show(sid[assignment[vid]]) ++ "\n" | vid in VMs];
