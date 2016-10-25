#include <iostream>
#include <fstream>
#include <string>
#include <tuple>
#include <vector>

#include <parser.hpp>
#include <problem.hpp>
#include <solver.hpp>

void print_answer(std::ostream &os, answer answer) {
  os << "o " << answer.min_server_count << "\n";

  for (auto &config : answer.configurations) {
    os << config.job_id << " "
       << config.vm_index << " -> "
       << config.server_id << "\n";
  }

  os << std::flush;
}

int main(int argc, char* argv[]) {
  if (argc < 2 || (argc == 2 && std::string(argv[1]) == "--help")) {
    std::cout << "USAGE: proj1 <scenario-file-name>" << std::endl;
    return 0;
  }

  const std::string filename(argv[1]);
  std::ifstream infile(filename);

  // encoder encoder;
  // solver solver;

  // encoder.encode(solver, parse(infile));

  // auto maybe_answer = solver.solve();

  // if (maybe_answer) {
  //   print_answer(std::cout, *maybe_answer);
  // } else {
  //   std::cout << "The solver has a bug..." << std::endl;
  // }

  return 0;
}
