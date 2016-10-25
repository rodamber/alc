#pragma once

#include <cmath>
#include <iostream>
#include <string>
#include <tuple>

#include <alc/problem.hpp>

namespace dimacs {
  const std::string sep = " ";
  const std::string nl  = " 0\n";
};

inline int literal_to_int(const alc::problem &prob, int i, int j, int k) {
  const std::size_t s = prob.servers.size();
  return s * (prob.h[i] + j) + k + 1;
}

inline std::tuple<int,int,int> int_to_literal(const alc::problem &prob, int y) {
  const std::size_t s = prob.servers.size();
  const int y_ = y - 1;

  const std::size_t w = std::floor(y_ / s);

  std::size_t ix = 0;
  for (; prob.h[ix] <= w && ix < prob.h.size(); ++ix)
    ;

  const int i = ix - 1;
  const int j = w - prob.h[i];
  const int k = y_ - s * (prob.h[i] + j);

  return std::make_tuple(i, j, k);
}


void at_least_one_constraint(std::ostream &os, const alc::problem &prob);

void at_most_one_constraint(std::ostream &os, const alc::problem &prob);

void cpu_constraint(std::ostream &os, const alc::problem &prob);

void ram_constraint(std::ostream &os, const alc::problem &prob);

void anti_col_constraint(std::ostream &os, const alc::problem &prob);
