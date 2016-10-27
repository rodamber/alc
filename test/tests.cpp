#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include <util.hpp>
#include <alc/encoder.hpp>
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
  anti_col_test();
  combinations_test();

  return 0;
}

namespace dimacs {
  const std::string sep = " ";
  const std::string nl  = " 0\n";
};

template <class T>
std::ostream &operator<<(std::ostream& os, const std::list<std::list<T>> ll) {
  for (auto &l: ll) {
    for (auto &x: l) {
      os << x << " ";
    }
    os << " 0\n";
  }

  return os;
}

template <class T>
std::ostream &operator<<(std::ostream &os, const std::vector<T> vec) {
  for (auto x: vec) {
    os << x << " ";
  }
  return os;
}


problem spec_problem() {

  const server s0(0, 5, 2), s1(1, 4, 1), s2(2, 7, 3), s3(3, 8, 5);
  std::vector<server> servers {s0, s1, s2, s3};

  virtual_machine
    v0(0, 0, 0, 1, 1, true), v1(1, 0, 1, 1, 1, true), v2(2, 1, 0, 1, 1, false),
    v3(3, 2, 0, 1, 1, true), v4(4, 2, 1, 1, 1, true), v5(5, 2, 2, 1, 1, false),
    v6(6, 3, 0, 1, 1, true), v7(7, 3, 1, 1, 1, true);

  std::vector<virtual_machine> vms {v0, v1, v2, v3, v4, v5, v6, v7};

  std::vector<std::size_t> job_sizes { 2, 1, 3, 2 };

  return problem(servers, vms, job_sizes);

}

void parser_test() {

  std::cout << "=== PARSER: ";

  std::string input_filename = "../input/01.in";
  std::ifstream infile(input_filename);

  problem parsed_problem = parse(infile);
  problem spec = spec_problem();

  assert(parsed_problem.servers == spec.servers);
  assert(parsed_problem.vms == spec.vms);
  assert(parsed_problem.job_sizes == spec.job_sizes);
  assert(parsed_problem == spec);

  std::cout << "PASS" << std::endl;
}

void literal_conversion_test() {
  std::cout << "=== LITERAL CONVERSION: ";

  problem problem = spec_problem();
  encoder encoder(problem);

  std::int64_t x = 1;

  for (auto &vm: problem.vms) {
    for (auto &s: problem.servers) {
      // std::cout << "literal(" << vm.id << ", " << s.id << ") = "
      //           << encoder.literal(vm, s) << "; x = " << x << std::endl;

      assert(encoder.literal(vm, s) == x);
      ++x;
    }
  }


  // assert(literal_to_int(prob, i, j, k) == x);
  // assert(int_to_literal(prob, x) == std::make_tuple(i, j, k));

  std::cout << "PASS" << std::endl;
}

void at_least_one_test() {
  std::cout << "=== AT LEAST ONE: ";

  problem problem = spec_problem();
  encoder encoder(problem);

  const std::size_t vms_count = problem.vms.size();
  const std::size_t servers_count = problem.servers.size();

  int x = 1;
  std::ostringstream test;

  for (std::size_t ix = 0; ix < vms_count; ++ix) {
    for (std::size_t jx = 0; jx < servers_count; ++jx, ++x) {
      test << x << dimacs::sep;
    }
    test << dimacs::nl;
  }

  encoder.encode_at_least_one_server_per_vm();

  std::ostringstream out;
  out << encoder.clauses();

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

  problem problem = spec_problem();
  encoder encoder(problem);

  const std::size_t vms_count = problem.vms.size();
  const std::size_t servers_count = problem.servers.size();

  int x = 1;
  std::ostringstream test;

  for (auto &vm: encoder.vms()) {
    int y = x;

    for (std::size_t k0 = 0; k0 < servers_count - 1; ++k0, ++x) {
      for (std::size_t k1 = k0 + 1; k1 < servers_count; ++k1) {
        test << -1 * (int)(y + k0) << dimacs::sep;
        test << -1 * (int)(y + k1) << dimacs::sep << dimacs::nl;
      }
    }
    ++x;
  }

  encoder.encode_at_most_one_server_per_vm();

  std::ostringstream out;
  out << encoder.clauses();

  // std::cout << "TEST\n"
  //           << "====" << std::endl;

  // std::cout << test.str() << std::endl;

  // std::cout << "OUT\n"
  //           << "===" << std::endl;

  // std::cout << out.str() << std::endl;

  assert(test.str() == out.str());

  std::cout << "PASS" << std::endl;
}

void anti_col_test() {
  std::cout << "=== ANTI COL: ";

  problem problem = spec_problem();
  encoder encoder(problem);

  std::ostringstream test;

  test << -1 << dimacs::sep << -5 << " " << dimacs::nl;
  test << -2 << dimacs::sep << -6 << " " << dimacs::nl;
  test << -3 << dimacs::sep << -7 << " " << dimacs::nl;
  test << -4 << dimacs::sep << -8 << " " << dimacs::nl;
  test << -13 << dimacs::sep << -17 << " " << dimacs::nl;
  test << -14 << dimacs::sep << -18 << " " << dimacs::nl;
  test << -15 << dimacs::sep << -19 << " " << dimacs::nl;
  test << -16 << dimacs::sep << -20 << " " << dimacs::nl;
  test << -25 << dimacs::sep << -29 << " " << dimacs::nl;
  test << -26 << dimacs::sep << -30 << " " << dimacs::nl;
  test << -27 << dimacs::sep << -31 << " " << dimacs::nl;
  test << -28 << dimacs::sep << -32 << " " << dimacs::nl;

  std::ostringstream out;

  encoder.encode_at_most_one_anti_collocation_vm_per_job_per_server();
  out << encoder.clauses();

  // std::cout << "TEST\n"
  //           << "====" << std::endl;

  // std::cout << test.str() << std::endl;

  // std::cout << "OUT\n"
  //     << "===" << std::endl;

  // std::cout << out.str() << std::endl;


  assert(test.str() == out.str());


  std::cout << "PASS" << std::endl;
}

void combinations_test() {
  std::cout << "=== COMBS: ";
  std::ostringstream test;

  test << 0 << 1 << 2 << std::endl
       << 0 << 1 << 3 << std::endl
       << 0 << 1 << 4 << std::endl
       << 0 << 2 << 3 << std::endl
       << 0 << 2 << 4 << std::endl
       << 0 << 3 << 4 << std::endl
       << 1 << 2 << 3 << std::endl
       << 1 << 2 << 4 << std::endl
       << 1 << 3 << 4 << std::endl
       << 2 << 3 << 4 << std::endl;

  std::ostringstream out;

  combination_generator generate(5, 3);
  std::vector<int> combination;

  while (!((combination = generate()).empty())) {
    for (auto x: combination) {
      out << x;
    }
    out << std::endl;
  }
  // std::cout << "TEST\n"
  //           << "====" << std::endl;

  // std::cout << test.str() << std::endl;

  // std::cout << "OUT\n"
  //           << "===" << std::endl;

  // std::cout << out.str() << std::endl;


  assert(test.str() == out.str());

  std::cout << "PASS" << std::endl;
}
