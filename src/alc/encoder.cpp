#include <vector>

#include <alc/encoder.hpp>

alc::encoder::encoder(alc::solver solver, alc::problem problem)
  : solver_(solver), problem_(problem) {
  for (auto &vm: vms()) {
    for (auto &server: servers()) {
      // We don't need to store these because we can calculate them in O(1).
      solver.new_var();
    }
  }
}

alc::solution alc::encoder::solution() {
  // FIXME
  return {};
}

void alc::encoder::encode_at_least_one_server_per_vm() {
  for (auto &vm: vms()) {
    alc::clause clause;

    for (auto &s: servers()) {
      clause.add(literal(vm, s));
    }
    solver_.add_clauses({clause});
  }
}

void alc::encoder::encode_at_most_one_server_per_vm() {
  for (auto &vm: vms()) {
    // Pairwise encoding.
    // Pay special atention to the iterators bounds!
    for (auto lhs_it = servers().begin(); lhs_it != servers().end() - 1; ++lhs_it) {
      for (auto rhs_it = lhs_it + 1; rhs_it != servers().end(); ++rhs_it) {
        alc::clause clause;

        clause.add(neg(literal(vm, *lhs_it)));
        clause.add(neg(literal(vm, *rhs_it)));

        solver_.add_clauses({clause});
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

    const auto x = [&](std::size_t i) { // get VM literal of column s.id, line i - 1
      return literal(i - 1, server.id);
    };

    const auto w = [&](std::size_t i) { // weight of VM of index i - 1
      auto vm = vms().at(i - 1);
      return vm.requirement(hw);
    };

    // -------------------------------------------------------------------------

    // Tabela de variaveis auxiliares.
    std::vector<std::vector<std::int64_t>> s(n + 1, std::vector<std::int64_t>(k + 1, 0));

    // Preencher tabela de vars auxiliares com os numeros das variaveis (para o minisat)
    // Reparar que nao preenchem (0,j) (i,0) (apenas por comodidade).
    for (std::size_t i = 1; i <= n; ++i) {
      for (std::size_t j = 1; j <= k; ++j) {
        s[i][j] = solver_.new_var();
      }
    }

    // -------------------------------------------------------------------------


    // 1. x[i] => s[i][j]                     !i,j. (1 <= i <= n, 1 <= j < = w[i])
    // forall i, j: 1 <= i <= n,
    //              1 <= j <= w[i]
    for (std::size_t i = 1; i <= n; ++i) {
      for (std::size_t j = 1; j <= w(i); ++j) {
        alc::clause clause;

        clause.add(neg(x(i)));
        clause.add(s[i][j]);

        solver_.add_clauses({clause});
      }
    }

    // 2. -s[1][j]
    // forall j: w[1] < j <= k
    for (std::size_t j = w(1) + 1; j <= k; ++j) {
      alc::clause clause;

      clause.add(neg(s[1][j]));

      solver_.add_clauses({clause});
    }

    // 3. s[i-1][j] => s[i][j]
    // forall i, j: 2 <= i <= n,
    //              1 <= j <= k
    for (std::size_t i = 2; i <= n; ++i) {
      for (std::size_t j = 1; j <= k; ++j) {
        alc::clause clause;

        clause.add(neg(s[i-1][j]));
        clause.add(s[i][j]);

        solver_.add_clauses({clause});
      }
    }

    // 4. x[i] . s[i - 1][j] => s[i][j + w[i]]
    // forall i, j: 2 <= i <= n,
    //              1 <= j <= k - w[i]
    for (std::size_t i = 2; i <= n; ++i) {
      for (std::size_t j = 1; j <= k - w(i); ++j) {
        alc::clause clause;

        clause.add(neg(x(i)));
        clause.add(neg(s[i - 1][j]));
        clause.add(s[i][j + w(i)]);

        solver_.add_clauses({clause});
      }
    }

    // 5. x[i] => s[i-1][k+1-w[i]]
    // forall i: 2 <= i <= n
    for (std::size_t i = 2; i <= n; ++i) {
      alc::clause clause;

      clause.add(neg(x(i)));
      clause.add(s[i - 1][k + 1 - w(i)]);

      solver_.add_clauses({clause});
    }

  }
}
