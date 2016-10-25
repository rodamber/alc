#include "alc/solver.hpp"

// FIXME
std::list<std::int64_t> alc::solver::solve() {
  return {};
}

std::experimental::optional<std::list<std::int64_t>> alc::solver::search() const {
  return {};
}

void alc::solver::add_clauses(std::list<alc::clause> &clauses) {
  add_clauses(clauses);
}

void alc::solver::add_clauses(std::list<alc::clause> &&clauses) {
  clauses_.splice(clauses_.begin(), clauses);
}
