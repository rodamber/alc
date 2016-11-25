include "constraints.mzn";

% ------------------------------------------------------------------------------
% Solve 
% ------------------------------------------------------------------------------

solve satisfy;

output["o " ++ show(on_count) ++ "\n"] ++
      [show(vjob[v]) ++ " " ++ show(vindex[v]) ++ " -> "++
       show(sid[place[v]]) ++ "\n" | v in vms];
