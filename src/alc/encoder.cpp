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
  // FIXME
  return;
}

void alc::encoder::encode_not_exceeding_server_capacity(alc::hardware hw) {
  // FIXME
  return;
}

void alc::encoder::encode_sequential_weighted_counter(alc::hardware hw) {
  // FIXME
  return;
}
