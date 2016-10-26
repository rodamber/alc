#include <alc/solver.hpp>

std::experimental::optional<std::list<std::int64_t>> alc::solver::solve() {
  // FIXME
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
