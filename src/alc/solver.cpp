#include <cmath>
#include <alc/solver.hpp>

std::experimental::optional<std::list<std::int64_t>> alc::solver::solve() {

  using namespace Minisat;

  Solver solver;

  for (int64_t i = 0; i < var_count(); ++i) {
    solver.newVar();
  }

  for (auto c: clauses_) {
    vec<Lit> clause;

    for (auto x: c.literals) {
      clause.push(mkLit(abs(x) - 1, x < 0));
    }

    solver.addClause(clause);
  }

  if (solver.solve()) { // Problem is SAT so let's get the model
    std::list<std::int64_t> l;

    for (int i = 0; i < solver.nVars(); ++i) {
      if (solver.modelValue(i) == l_True) {
        l.push_back(i + 1);
      }
    }

    return { l };
  }

  return {};
}

std::list<std::list<std::int64_t>> alc::solver::clauses() const {
  std::list<std::list<std::int64_t>> cs;

  for (auto &clause : clauses_) {
    std::list<std::int64_t> clause_copy(clause.literals);
    cs.push_back(clause_copy);
  }

  return cs;
}

void alc::solver::write_dimacs_cnf(std::ostream &os) {
  os << "p cnf " << var_count() << " " << clauses_.size() << "\n";
  for (auto &c: clauses_) {
    os << c;
  }
}
