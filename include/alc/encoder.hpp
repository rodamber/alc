#pragma once

#include <alc/problem.hpp>
#include <alc/solver.hpp>

namespace alc {

  class encoder {
  public:

    encoder(solver, problem);

    alc::solution solution();

    // Gets the sat solver integer variable corresponding to the given pair (VM, Server)
    inline int literal(virtual_machine vm, server s) {
      return vm.id * servers().size() + s.id + 1;
    }

    inline int literal(std::size_t vm_id, std::size_t s_id) {
      return vm_id * servers().size() + s_id + 1;
    }

    // Negate a literal.
    inline int neg(int lit) {
      return -1 * lit;
    }

    inline std::vector<server> &servers() {
      return problem_.servers;
    }

    inline std::vector<virtual_machine> &vms() {
      return problem_.vms;
    }

    inline std::list<std::list<std::int64_t>> clauses() const {
      return solver_.clauses();
    }

    inline void encode(solver solver) {
      encode_at_least_one_server_per_vm();
      encode_at_most_one_server_per_vm();
      encode_not_exceeding_server_capacity(CPU);
      encode_not_exceeding_server_capacity(RAM);
    }

    void encode_at_least_one_server_per_vm();
    void encode_at_most_one_server_per_vm();
    void encode_not_exceeding_server_capacity(hardware);
    void encode_sequential_weighted_counter(hardware);

  private:
    // The solver used to get to the solution.
    solver solver_;

    // The problem to encode and solve.
    problem problem_;

  };

};
