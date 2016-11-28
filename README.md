Group: 13

Students:
  - João Nuno Estevão Fidalgo Ferreira Alves (79155)
  - Rodrigo André Moreira Bernardo (78942)

Programming Language: python3

Solver: MiniZinc 2.1.0 using the G12/LazyFD backend

# Running

We assume *mzn-g12lazy* is in the path. To run the project just issue

```
./proj3 path/to/input/file
```

# Solution sketch

The solution sketch is simple: if the problem only requires the placement of
"simple" virtual machines (VM), i.e., VMs with cpu and ram capacities equal to
1, then we apply a polynomial complexity algorithm; if not we use minizinc
to find a placement for the VMs.

We added the usual constraints stating that each VM must be on one server, that
the cpu/ram capacities of the servers must not be exceeded and regarding
anti-collocation constraints.

The servers and the VMs are coded in minizinc using arrays to represent their
attributes (cpu, ram, where each VM is placed, etc.).


# Optimizations

We added redundant restrictions that implied that the sum of the cpu/ram
capacities of the servers was always greater than or equal to the sum of the
cpu/ram requirements of the virtual machines. We also said that if a server x is
"worse" than another and is turned on, then all the servers "better" than server x
must be turned on. Finally, the cpu/ram load of all the servers must be equal to
the sum of the cpu/ram requirements of all the VMs.

We also provided a solve annotation to try to improve the search speed.

With these optimizations we were able to solve all the provided instances
sequentially in under 13s.

