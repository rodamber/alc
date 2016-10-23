#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

struct Data{
  unsigned servers;
  unsigned machines;
  unsigned jobs;
} problem;

void input(std::istream& infile) {
  size_t num_servers;
  size_t num_jv_pairs;

  size_t s_cpu;
  size_t s_ram;
  size_t s_id;

  //num of servers
  std::string line;

  getline(infile, line);
  std::istringstream iss(line);

  if (iss >> num_servers) {
    std::cout << num_servers << std::endl;
  }

  for(size_t tmp = 0; tmp < num_servers; tmp++){
    getline(infile, line);
    iss = std::istringstream(line);

    //create server object
    if(iss >> s_id >> s_cpu >> s_ram) {
      std::cout << s_id << " " << s_ram << " " << s_cpu << std::endl;
    }
  }

  //num of (jobs, machines)
  getline(infile, line);
  iss = std::istringstream(line);

  if(iss >> num_jv_pairs) {
    std::cout << "Number of Pairs: " << num_jv_pairs << std::endl;
  }

  for(size_t tmp = 0; tmp < num_jv_pairs; tmp++){
    getline(infile, line);
    //create jv_pair
  }
}

int main(int argc, char* argv[]) {
  (void) argc;
  const char* filename = argv[1];
  std::ifstream infile(filename);
  input(infile);
  return 0;
}
