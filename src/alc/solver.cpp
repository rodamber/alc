#include "alc/solver.hpp"

// FIXME
std::experimental::optional<std::list<std::size_t>> alc::solver::solve() {
  return {};
}

std::experimental::optional<std::list<std::size_t>> alc::solver::search() const {
  return {};
}

void alc::solver::add_clauses(std::list<alc::clause> &clauses) {
  clauses_.splice(clauses_.begin(), clauses);
}
