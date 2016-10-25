#include <iostream>
#include <fstream>
#include <string>
#include <tuple>
#include <vector>

#include <alc/parser.hpp>
#include <alc/problem.hpp>
#include <alc/solver.hpp>

std::ostream& operator<<(std::ostream& os, const alc::answer &answer) {
  os << "o " << answer.min_server_count << "\n";

  for (auto &config : answer.configurations) {
    os << config.job_id << " "
       << config.vm_index << " -> "
       << config.server_id << "\n";
  }

  return os;
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
  //   std::cout << *maybe_answer << std::flush;
  // } else {
  //   std::cout << "The solver has a bug..." << std::endl;
  // }

  return 0;
}
