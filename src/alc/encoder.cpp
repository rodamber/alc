#include <algorithm>
#include <vector>

#include <alc/encoder.hpp>

alc::encoder::encoder(alc::solver solver, alc::problem problem)
  : solver_(solver), problem_(problem), server_count_(problem_.servers.size()) {
  for (auto &vm: vms()) {
    for (auto &server: servers()) {
      // We don't need to store these because we can calculate them in O(1).
      solver_.new_var();
    }
  }
}

alc::solution alc::encoder::solution() {
  // FIXME
  return {};
}

std::experimental::optional<std::list<std::int64_t>> alc::encoder::search() const {
  // FIXME
  return {};
}



void alc::encoder::encode() {
  encode_at_least_one_server_per_vm();
  encode_at_most_one_server_per_vm();
  encode_not_exceeding_server_capacity(CPU);
  encode_not_exceeding_server_capacity(RAM);
}

void alc::encoder::encode_at_least_one_server_per_vm() {
  for (auto &vm: vms()) {
    alc::clause clause;

    for (auto &s: servers()) {
      clause.add(literal(vm, s));
    }

    add_clause(std::move(clause));
  }
}

void alc::encoder::encode_at_most_one_server_per_vm() {
  for (auto &vm: vms()) {
    // Pairwise encoding.
    // Pay special atention to the iterators bounds!
    for (auto lhs_it = servers().begin(); lhs_it != servers().end() - 1; ++lhs_it) {
      for (auto rhs_it = lhs_it + 1; rhs_it != servers().end(); ++rhs_it) {
        add_clause({ neg(literal(vm, *lhs_it)),
                     neg(literal(vm, *rhs_it)) });
      }
    }
  }

}

void alc::encoder::encode_at_most_one_anti_collocation_vm_per_job_per_server() {
  for (auto job_it = vms().begin();
       job_it != vms().end();
       job_it += problem_.job_sizes.at(job_it->job_id)) {
    for (auto lhs = job_it;
         lhs != job_it + problem_.job_sizes.at(lhs->job_id) - 1;
         ++lhs) {
      if (!(lhs->anti_collocation)) {
        continue;
      }
      for (auto rhs = lhs + 1;
           rhs != job_it + problem_.job_sizes.at(lhs->job_id);
           ++rhs) {
        if (rhs->anti_collocation) {
          for (auto &s: servers()) {
            add_clause({ neg(literal(*lhs, s)), neg(literal(*rhs, s)) });
          }
        }
      }
    }
  }
}


void alc::encoder::encode_not_exceeding_server_capacity(alc::hardware hw) {
  encode_sequential_weighted_counter(hw);
}

void alc::encoder::encode_sequential_weighted_counter(alc::hardware hw) {
  for (auto &server: servers()) {

    // -------------------------------------------------------------------------
    // Mini DSL (domain-specific language) for our problem

    const std::size_t n = vms().size();
    const std::size_t k = servers().at(server.id).capacity(hw);

    // Sequential weighted counter encoding table of auxiliary variables
    std::vector<std::vector<std::int64_t>> s_table(n + 1, std::vector<std::int64_t>(k + 1, 0));

    // Fill auxiliary table with minisat vars.
    for (std::size_t i = 0; i < n; ++i) {
      for (std::size_t j = 0; j < k; ++j) {
        s_table[i][j] = solver_.new_var();
      }
    }

    const auto x = [&](std::size_t i) { // get VM literal of column s.id, line i - 1
      return literal(i - 1, server.id);
    };

    const auto w = [&](std::size_t i) { // weight of VM of index i - 1
      auto vm = vms().at(i - 1);
      return vm.requirement(hw);
    };

    const auto s = [&](std::size_t i) {
      const auto s_j = [&](std::size_t j) {
        return s_table[i - 1][j - 1];
      };
      return s_j;
    };

    // -------------------------------------------------------------------------

    // 1. x[i) => s[i)[j) | forall i, j: 1 <= i <= n, 1 <= j <= w[i)
    for (std::size_t i = 1; i <= n; ++i)
      for (std::size_t j = 1; j <= w(i); ++j)
        add_clause({ neg(x(i)), s(i)(j) });

    // 2. -s(1)(j) | forall j: w(1) < j <= k
    for (std::size_t j = w(1) + 1; j <= k; ++j)
      add_clause({ neg(s(1)(j)) });

    // 3. s(i-1)(j) => s(i)(j) | forall i, j: 2 <= i <= n, 1 <= j <= k
    for (std::size_t i = 2; i <= n; ++i)
      for (std::size_t j = 1; j <= k; ++j)
        add_clause({ neg(s(i-1)(j)), s(i)(j) });

    // 4. x(i) . s(i - 1)(j) => s(i)(j + w(i)) | forall i, j: 2 <= i <= n, 1 <= j <= k - w(i)
    for (std::size_t i = 2; i <= n; ++i)
      for (std::size_t j = 1; j <= k - w(i); ++j)
        add_clause({ neg(x(i)), neg(s(i - 1)(j)), s(i)(j + w(i)) });

    // 5. x(i) => s(i-1)(k+1-w(i)) | forall i: 2 <= i <= n
    for (std::size_t i = 2; i <= n; ++i)
      add_clause({ neg(x(i)), s(i - 1)(k + 1 - w(i)) });

  }
}

void alc::encoder::write_dimacs_cnf(std::ostream &os) {
  solver_.write_dimacs_cnf(os);
}
