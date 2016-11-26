include "constraints.mzn";

var servers: on_count;

solve :: int_search([on_count], first_fail, indomain_min, complete)
      minimize on_count;

output["o " ++ show(on_count) ++ "\n"] ++
      [show(vjob[v]) ++ " " ++ show(vindex[v]) ++ " -> "++
       show(sid[place[v]]) ++ "\n" | v in vms];
