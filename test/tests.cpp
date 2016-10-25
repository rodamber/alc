#include <cassert>
#include <fstream>
#include <iostream>
#include <sstream>
#include <tuple>
#include <vector>

#include <alc/restrictions.hpp>
#include <alc/parser.hpp>

#include "tests.hpp"

using namespace alc;

int main() {

#ifdef NDEBUG
  std::cout << "NDEBUG is defined" << std::endl;
#endif
  parser_test();
  literal_conversion_test();
  at_least_one_test();
  at_most_one_test();

  return 0;
}

problem spec_problem() {

  const server s0(0, 5, 2), s1(1, 4, 1), s2(2, 7, 3), s3(3, 8, 5);
  std::vector<server> servers {s0, s1, s2, s3};

  virtual_machine
    v0(0, 0, 0, 1, 1, true), v1(1, 0, 1, 1, 1, true), v2(2, 1, 0, 1, 1, false),
    v3(3, 2, 0, 1, 1, true), v4(4, 2, 1, 1, 1, true), v5(5, 2, 2, 1, 1, false),
    v6(6, 3, 0, 1, 1, true), v7(7, 3, 1, 1, 1, true);

  std::vector<virtual_machine> vms {v0, v1, v2, v3, v4, v5, v6, v7};

  std::vector<std::size_t> h { 0, 2, 3, 6 };

  return problem(servers, vms, h);

}

void parser_test() {

  std::cout << "=== PARSER: ";

  std::string input_filename = "../input/01.in";
  std::ifstream infile(input_filename);

  problem parsed_problem = parse(infile);
  problem spec = spec_problem();

  assert(parsed_problem.servers == spec.servers);
  assert(parsed_problem.vms == spec.vms);
  assert(parsed_problem.h == spec.h);
  assert(parsed_problem == spec);

  std::cout << "PASS" << std::endl;
}

void literal_conversion_test() {
  std::cout << "=== LITERAL CONVERSION: ";

  problem prob = spec_problem();

  // for (std::size_t ix = 0; ix < prob.h.size(); ++ix) {
  //   std::cout << "h[" << ix << "] = "  << prob.h[ix] << std::endl;
  // }

  int x = 1;

  for (std::size_t i = 0; i < prob.jobs.size(); ++i) {
    for (std::size_t j = 0; j < prob.jobs.at(i).vms.size(); ++j) {
      for (std::size_t k = 0; k < prob.servers.size(); ++k) {

        // std::cout << "literal_to_int(prob, " << i << ", " << j << ", " << k << ") = "
        //           << literal_to_int(prob, i, j, k) << std::endl;

        // auto ijk = int_to_literal(prob, x);
        // std::cout << "int_to_literal(prob, " << x << ") = "
        //           << "("  << std::get<0>(ijk)
        //           << ", " << std::get<1>(ijk)
        //           << ", " << std::get<2>(ijk)
        //           << ")"  << std::endl;

        assert(literal_to_int(prob, i, j, k) == x);
        assert(int_to_literal(prob, x) == std::make_tuple(i, j, k));

        ++x;
      }
    }
  }

  std::cout << "PASS" << std::endl;
}

void at_least_one_test() {
  std::cout << "=== AT LEAST ONE: ";

  problem prob = spec_problem();

  std::size_t vms_count = 0;
  for (auto &j: prob.jobs) {
    vms_count += j.vms.size();
  }

  int x = 1;
  std::ostringstream test;

  for (std::size_t ix = 0; ix < vms_count; ++ix) {
    for (std::size_t jx = 0; jx < prob.servers.size(); ++jx, ++x) {
      test << x << dimacs::sep;
    }
    test << dimacs::nl;
  }

  std::ostringstream out;
  at_least_one_constraint(out, prob);

  // std::cout << "TEST\n"
  //           << "====" << std::endl;

  // std::cout << test.str() << std::endl;

  // std::cout << "OUT\n"
  //           << "===" << std::endl;

  // std::cout << out.str() << std::endl;

  assert(test.str() == out.str());

  std::cout << "PASS" << std::endl;
}

void at_most_one_test() {
  std::cout << "=== AT MOST ONE: ";

  problem prob = spec_problem();

  int x = 1;
  std::ostringstream test;

  for (std::size_t i = 0; i < prob.jobs.size(); ++i) {
    for (std::size_t j = 0; j < prob.jobs.at(i).vms.size(); ++j) {
      int y = x;
      for (std::size_t k0 = 0; k0 < prob.servers.size() - 1; ++k0, ++x) {
        for (std::size_t k1 = k0 + 1; k1 < prob.servers.size(); ++k1) {
          test << -1 * (int)(y + k0) << dimacs::sep;
          test << -1 * (int)(y + k1) << dimacs::nl;
        }
      }
      ++x;
    }
  }

  std::ostringstream out;
  at_most_one_constraint(out, prob);

  // std::cout << "TEST\n"
  //           << "====" << std::endl;

  // std::cout << test.str() << std::endl;

  // std::cout << "OUT\n"
  //           << "===" << std::endl;

  // std::cout << out.str() << std::endl;

  assert(test.str() == out.str());

  std::cout << "PASS" << std::endl;
}
