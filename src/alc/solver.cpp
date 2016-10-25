#include "alc/solver.hpp"

// FIXME
std::experimental::optional<std::list<std::int64_t>> alc::solver::solve() {
  return {};
}

void alc::solver::add_clause(alc::clause &&clause) {
  clauses_.push_back(clause);
}
