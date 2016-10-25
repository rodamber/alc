#include <iostream>
#include <fstream>
#include <string>
#include <tuple>
#include <vector>

#include <parser.hpp>
#include <problem.hpp>

// Returns if the problem is SAT or UNSAT
bool solve(const problem &prob) {
  (void) prob;
  return false;
}

// A set of triples. The first element of the triple is the job, the second is
// the vm and the third is the server.
using answer = std::vector<std::tuple<int, int, int>>;

// Uses the solve function to search for the optimal solution.
// Returns the minimal number of servers needed.
size_t search(const problem &prob, answer &ans) {
  (void) prob; (void) ans;
  return -1;
}

int main(int argc, char* argv[]) {
  if (argc < 2 || (argc == 2 && std::string(argv[1]) == "--help")) {
    std::cout << "USAGE: proj1 <scenario-file-name>" << std::endl;
    return 0;
  }

  const std::string filename(argv[1]);
  std::ifstream infile(filename);

  problem prob = parse(infile);
  return 0;
}
