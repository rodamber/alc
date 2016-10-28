#pragma once

#include <algorithm>
#include <experimental/optional>
#include <iostream>
#include <utility>

#include <alc/problem.hpp>
#include <alc/solver.hpp>

namespace alc {

  class encoder {
  public:

    encoder(problem);

    alc::solution solution();

  public:

    template <class T>
    using opt = std::experimental::optional<T>;

    using model = std::list<std::int64_t>;

  public:

    // Gets the sat solver integer variable corresponding to the given pair (VM, Server)
    inline int literal(virtual_machine vm, server s) const {
      const auto s_ix = std::distance(servers().begin(),
                                      std::find(servers().begin(), servers().end(), s));
      return vm.id * servers().size() + s_ix + 1;
    }

    inline std::pair<virtual_machine, server> from_literal(int64_t x) const {
      const auto x_ = x - 1;
      const auto k = servers().size();

      return { vms().at(x_ / k),
          servers().at(x_ % k) };
    }

  public:

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

  public:

    opt<model> sat(const std::vector<server>&);

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

    void considered_servers(std::vector<server> ss) {
      considered_servers_ = ss;
    }

    // Uses a SAT solver to search for the minimum number of up servers.
    // Returns the model if one is found.
    opt<std::pair<model,std::size_t>> search();

  };

};
