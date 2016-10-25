#include <alc/restrictions.hpp>


// void at_least_one_constraint(std::ostream &os, const alc::problem &prob) {
//   for (std::size_t i = 0; i < prob.jobs.size(); ++i) {
//     for (std::size_t j = 0; j < prob.jobs.at(i).vms.size(); ++j) {
//       for (std::size_t k = 0; k < prob.servers.size(); ++k) {
//         os << literal_to_int(prob, i, j, k) << dimacs::sep;
//       }
//       os << dimacs::nl;
//     }
//   }
// }

void at_most_one_constraint(std::ostream &os, const alc::problem &prob) {
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

void cpu_constraint(std::ostream &os, const alc::problem &prob) {
  (void) os; (void) prob;
}

void ram_constraint(std::ostream &os, const alc::problem &prob) {
  (void) os; (void) prob;
}

void anti_col_constraint(std::ostream &os, const alc::problem &prob) {
  (void) os; (void) prob;
  // std::vector<int> anti_col;

  // for(std::size_t i = 0; i < prob.jobs.size(); i++) {
  //   for (std::size_t j = 0; j < prob.jobs.at(i).vms.size(); j++) {
  //     if(prob.jobs.at(i).vms.at(j).anti_col){
  //       anti_col.push_back(literal_to_int(prob, i, j, 0));
  //     }
  //   }
  // }

  // for (std::size_t k = 0; i < prob.servers.size(); k++) {
  //   for(std::size_t v; v < anti_col.size(); v++) {
  //     os << -1 * (v + k);

  //     if(v == anti_col - 1) {
  //       os << dimacs::sep;
  //     } else {
  //       os << dimacs::nl;
  //     }
  //   }
  // }
}
