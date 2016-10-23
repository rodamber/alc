#include "restrictions.hpp"


void at_least_one_constraint(std::ostream &os, const problem &prob) {
  for (std::size_t i = 0; i < prob.jobs.size(); ++i) {
    for (std::size_t j = 0; j < prob.jobs.at(i).vms.size(); ++j) {
      for (std::size_t k = 0; k < prob.servers.size(); ++k) {
        os << literal_to_int(prob, i, j, k) << dimacs::sep;
      }
      os << dimacs::nl;
    }
  }
}

void at_most_one_constraint(std::ostream &os, const problem &prob) {
  for (std::size_t i = 0; i < prob.jobs.size(); ++i) {
    for (std::size_t j = 0; j < prob.jobs.at(i).vms.size(); ++j) {
      for (std::size_t k0 = 0; k0 < prob.servers.size() - 1; ++k0) {
        for (std::size_t k1 = k0 + 1; k1 < prob.servers.size(); ++k1) {
          os << -1 * literal_to_int(prob, i, j, k0) << dimacs::sep
             << -1 * literal_to_int(prob, i, j, k1) << dimacs::nl;
        }
      }
    }
  }
}

void cpu_constraint(std::ostream &os, const problem &prob) {
  (void) os; (void) prob;
}

void ram_constraint(std::ostream &os, const problem &prob) {
  (void) os; (void) prob;
}

void anti_col_constraint(std::ostream &os, const problem &prob) {
  (void) os; (void) prob;
}
