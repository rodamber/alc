#pragma once

#include <alc/problem.hpp>
#include <alc/solver.hpp>

namespace alc {

  enum hardware { CPU, RAM };

  class encoder {
  public:

    encoder(solver, problem);

    alc::solution solution();

    // Gets the sat solver integer variable corresponding to the given pair (VM, Server)
    inline int literal(virtual_machine vm, server s) {
      return vm.id * servers().size() + s.id + 1;
    }

    inline std::vector<server> &servers() {
      return problem_.servers;
    }

    inline std::vector<virtual_machine> &vms() {
      return problem_.vms;
    }

  protected:

    inline void encode(solver solver) {
      encode_at_least_one_server_per_vm(solver);
      encode_at_most_one_server_per_vm(solver);
      encode_not_exceeding_server_capacity(solver, CPU);
      encode_not_exceeding_server_capacity(solver, RAM);
    }

    void encode_at_least_one_server_per_vm(solver);
    void encode_at_most_one_server_per_vm(solver);
    void encode_not_exceeding_server_capacity(solver, hardware);

  private:
    // The solver used to get to the solution.
    solver solver_;

    // The problem to encode and solve.
    problem problem_;

  private:
    void encode_sequential_weighted_counter(solver, hardware);

  };

};
