#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#include "parser.hpp"

void parse(std::istream& infile) {
  size_t num_servers;
  size_t num_jv_pairs;

  size_t s_cpu;
  size_t s_ram;
  size_t s_id;

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

