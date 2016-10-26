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

    class servers_;
    using servers_t = servers_;

    inline servers_t servers() {
      return servers_(*this, server_count_);
    }

    inline const std::vector<virtual_machine> &vms() const {
      return problem_.vms;
    }

    inline std::list<std::list<std::int64_t>> clauses() const {
      return solver_.clauses();
    }

    inline void encode() {
      encode_at_least_one_server_per_vm();
      encode_at_most_one_server_per_vm();
      encode_not_exceeding_server_capacity(CPU);
      encode_not_exceeding_server_capacity(RAM);
    }

    void encode_at_least_one_server_per_vm();
    void encode_at_most_one_server_per_vm();
    void encode_not_exceeding_server_capacity(hardware);
    void encode_sequential_weighted_counter(hardware);

    void write_dimacs_cnf(std::ostream &os);

  private:
    // The solver used to get to the solution.
    solver solver_;

    // The problem to encode and solve.
    problem problem_;

    // Number of servers considered for the encoding.
    std::size_t server_count_;

  private:
    void add_clause(alc::clause &&clause) {
      solver_.add_clause(std::move(clause));
    }

    // Uses a SAT solver to search for the minimum number of up servers.
    // Returns the model if one is found.
    std::experimental::optional<std::list<std::int64_t>> search() const;

  public:
    class servers_ {
    public:
      servers_(encoder &encoder, int server_count)
        : encoder_(encoder), server_count_(server_count) { }

      using iterator = std::vector<server>::iterator;
      using const_iterator = std::vector<server>::const_iterator;

      iterator begin() { return servers().begin(); }
      iterator end() { return servers().begin() + server_count_; }

      const_iterator cbegin() { return servers().cbegin(); }
      const_iterator cend() { return servers().cbegin() + server_count_; }

      std::size_t size() { return server_count_; }

      server &at(std::size_t pos) {
        if (!(pos < size())) throw std::out_of_range("servers_t: " + std::to_string(pos));
        return servers().at(pos);
      }

    private:
      encoder &encoder_;
      int server_count_ = 0;

    private:
      std::vector<server> &servers() const {
        return encoder_.problem_.servers;
      }
    };

  };

};
