#include "alc/solver.hpp"

// FIXME
std::list<std::int64_t> alc::solver::solve() {
  return {};
}

std::experimental::optional<std::list<std::int64_t>> alc::solver::search() const {
  return {};
}

void alc::solver::add_clause(alc::clause &&clause) {
  clauses_.push_back(clause);
}
