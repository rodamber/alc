Group: 10

Students:
  - João Nuno Estevão Fidalgo Ferreira Alves (79155)
  - Rodrigo André Moreira Bernardo (78942)

Programming Language: C++

SAT-Solver: minisat

Version: 2.0

Compiler: g++ 5.4.0

# Compiling
```
cd src
make
```

# Encodings:

This encoding discards the use of an entity to represent Jobs, instead every
Virtual Machine has a global identifier and knows to which Job it belongs. This
was done so the code structure and encodings would become simpler to implement.

Our solution uses |V| x |S| variables + auxiliary variables for each encoding,
where V is the complete set of virtual machines and S is the set of servers
considered in the encoding.

If a given variable (apart from the auxiliary ones) is true it means that the
corresponding virtual machine is placed in the corresponding server.
The literal <-> (virtual machine, server) correspondence is given by

 > vm.id * |S| + s.ix + 1

where vm.id is the Virtual Machine global identifier, |S|
represents the total number of servers and s.ix is the server index in the set
of considered servers.

## At least one server per vm

If our problem has V Virtual Machines and S servers, then we will have V
clauses, each one representing all possible allocations.

## At most one server per vm
	
Constraints the allocations of Virtual Machines in at most one Server Pairwise
was chosen for simplicity sake, since Bitwise would require auxiliar variables.

## Anti-collocation constraints

Constraints the allocations of Virtual Machines with anti_collocation equal to
true, within a same job, in at-most one server. The pairwise encoding was chosen
for simplicity sake.

## Cardinality constraints

To ensure that the servers CPU and RAM capacities were not exceeded we resorted
to encode cardinality constraints. For that we implemented the sequential
weighted counter encoding and, again, was chosen instead of generalized
totalizer for simplicity sake.

	
# Optimizations:

1. If the problem is known to be solved in polynomial time then we don't use the
   SAT solver. Instead we solve it directly.

2. In each call to the solver we handpick a subset of servers, according to
   their RAM and CPU capacity, in a way that ensures that the amount of server
   combinations tested is minimized.

   We do this by first obtaining the set of the "best" servers according to
   their RAM and CPU. We then try all k-combinations of servers and check if
   there is a solution. If not we get the best from the remaining servers,
   trying all the k-combinations of those plus the already picked servers. Thus
   we evade from trying all k-combinations of the whole new subset of servers
   and, obviously, from trying all combinations of the whole set.

3. The initial number of servers tested is equal to the max number of
   anti-collocations within all jobs, meaning that we will never test an encoding
   that is known to be impossible already.

# Notes regarding Minisat

We resorted to the Minisat API instead of relying on writing to files and
sending them to the solver. We included the Minisat source code and the makefile
assumes it exists under the minisat folder and compiles it.
