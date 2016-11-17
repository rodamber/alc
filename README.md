Group: 13
Students:
  - João Nuno Estevão Fidalgo Ferreira Alves (79155)
  - Rodrigo André Moreira Bernardo (78942)
Programming Language: python3
Solver: Z3 version 4.4.1

*Note*: We resorted to using the z3py API instead of using the SMT-LIB v2 language
interface.

# Running

If Z3 is not on path we have to point the PYTHONPATH variable path to the
directory where libz3.so is, along with the z3 python scripts:

```
export PYTHONPATH=path/to/z3/build/directory
```

The program is run by issuing

```
./proj2 <input-file>
```

# Solution sketch

The solution sketch is simple: if the problem only requires the placement of
"simple" virtual machines (VM), i.e., VMs with cpu and ram capacities equal to
1, then we apply a polynomial complexity algorithm; if not we use the z3 solver
to find a placement for the VMs. In the second case, we make use of integer
arithmetic and uninterpreted functions to ensure the constraints mentioned in
the specs are satisfied.

The search for the minimum number of servers is also pretty straightforward. We
know that we need a number of servers of at least the maximum number of
anti-collocation VMs per job, *n*. We summon z3 for each number from n to the
total number of servers until we get sat as a result. For each iteration we add
a new restriction stating the number of servers that must be on. We make use of
the push and pop methods of the z3 solver object to ensure that we don't
recompute the complete formula each time.

# Optimizations

We tried some symmetry breaking approaches, but in the end they seemed to just
add more overhead. What worked for us were two things:
    1. Redundant restrictions. We added two redundant restrictions that implied
       that the sum of the capacities of servers turned on was always less or
       equal than the requirements of the virtual machines. With this we were
       able to solve all but two of the bench22{-small} instances in seconds.
    2. Heuristics. On each iteration, before the usual call to the solver we
       tried two heuristics to solve the problem. We ordered the servers based
       on their cpu/ram capacity and asked the solver to find a solution with
       the best servers according to that heuristic. The heuristic approach is
       not complete so, if the solver cannot find a solution by using them, we
       resort to the safe approach.

With optimizations 1 and 2 we were able to solve all the provided instances
(bench11-small, bench11, bench22-small and bench22) sequentially in under 9s.


