#include <fstream>

#include "parser.hpp"

int main(int argc, char* argv[]) {
  (void) argc;

  const char* filename = argv[1];
  std::ifstream infile(filename);

  parse(infile);

  return 0;
}
