#pragma once

#include <alc/problem.hpp>

namespace alc {

  class polynomial_solver {
  public:
    polynomial_solver(problem prob)
      : problem_(prob) {
    }

    alc::solution solution();


  private:
    problem problem_;
  };

};
