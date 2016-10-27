#include <iostream>
#include <fstream>
#include <string>
#include <tuple>
#include <vector>

#include <alc/encoder.hpp>
#include <alc/parser.hpp>
#include <alc/problem.hpp>
#include <alc/solver.hpp>


std::ostream& operator<<(std::ostream& os, const alc::solution &solution) {
  os << "o " << solution.min_server_count << "\n";

  for (auto &config : solution.configurations) {
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

  alc::encoder encoder(alc::parse(infile));

  try {
    std::cout << encoder.solution() << std::flush;
  } catch (const std::exception& e) {
    std::cout << e.what() << std::endl;
  }

  return 0;
}
