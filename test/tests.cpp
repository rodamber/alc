#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

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

  return 0;
}

namespace dimacs {
  const std::string sep = " ";
  const std::string nl  = " 0\n";
};

template <class T>
std::ostream &operator<<(std::ostream& os, const std::list<std::list<T>> ll) {
  // const std::size_t var_count =
  //   std::accumulate(ll.begin(), ll.end(), 0, [](std::size_t lhs, std::list<T> rhs) {
  //       return lhs + rhs.size();
  //     });
  // const std::size_t clause_count = ll.size();

  // os << "p cnf " << var_count << " " << clause_count << "\n";

  for (auto &l: ll) {
    for (auto &x: l) {
      os << x << " ";
    }
    os << " 0\n";
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

  encoder encoder(solver(), spec_problem());

  std::int64_t x = 1;

  for (auto &vm: encoder.vms()) {
    for (auto &s: encoder.servers()) {
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

  encoder encoder(solver(), spec_problem());

  const std::size_t vms_count = encoder.vms().size();
  const std::size_t servers_count = encoder.servers().size();

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

  encoder encoder(solver(), spec_problem());

  const std::size_t vms_count = encoder.vms().size();
  const std::size_t servers_count = encoder.servers().size();

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
