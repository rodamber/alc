#pragma once

#include <experimental/optional>
#include <iostream>

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

    inline const std::vector<server> &servers() const {
      return considered_servers_;
    }

    inline const std::vector<virtual_machine> &vms() const {
      return problem_.vms;
    }

    inline std::list<std::list<std::int64_t>> clauses() const {
      return solver_.clauses();
    }

    void encode();
    void encode_at_least_one_server_per_vm();
    void encode_at_most_one_server_per_vm();
    void encode_at_most_one_anti_collocation_vm_per_job_per_server();
    void encode_not_exceeding_server_capacity(hardware);
    void encode_sequential_weighted_counter(hardware);

    void write_dimacs_cnf(std::ostream &os);

  private:
    // The solver used to get to the solution.
    solver solver_;

    // The problem to encode and solve.
    problem problem_;

    // Servers considered for the encoding.
    std::vector<server> considered_servers_;

  private:
    void add_clause(alc::clause &&clause) {
      solver_.add_clause(std::move(clause));
    }

    void considered_servers(std::vector<int> servers_indices) {
      considered_servers_.clear();

      for (auto i: servers_indices) {
        considered_servers_.push_back(problem_.servers.at(i));
      }
    }

    // Uses a SAT solver to search for the minimum number of up servers.
    // Returns the model if one is found.
    std::experimental::optional<std::list<std::int64_t>> search() const;

  };

};
