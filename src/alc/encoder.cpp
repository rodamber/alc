#include <alc/encoder.hpp>

alc::encoder::encoder(alc::solver solver, alc::problem problem)
  : solver_(solver), problem_(problem) {
}

alc::solution alc::encoder::solution() {
  // FIXME
  return {};
}

void alc::encoder::encode_at_least_one_server_per_vm(alc::solver solver) {
  // FIXME
  return;
}

void alc::encoder::encode_at_most_one_server_per_vm(alc::solver solver) {
  // FIXME
  return;
}

void alc::encoder::encode_not_exceeding_server_capacity(alc::solver solver,
                                                        alc::hardware hw) {
  // FIXME
  return;
}

void alc::encoder::encode_sequential_weighted_counter(solver, hardware) {
  // FIXME
  return;
}
