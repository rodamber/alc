#include <cassert>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <string.h>

#include <parser.hpp>

void parse_servers_spec(std::istream &infile, problem &prob) {
  std::string line;
  getline(infile, line);
  std::istringstream iss(line);

  size_t num_servers;
  if (iss >> num_servers) {
  }

  for(size_t i = 0; i < num_servers; i++){
    getline(infile, line);
    iss = std::istringstream(line);

    server s;
    if(iss >> s.id >> s.cpu_cap >> s.ram_cap){
      prob.servers.push_back(s);
    }
  }
}


void parse_vms_spec(std::istream &infile, problem &prob) {
  std::string line;
  getline(infile, line);
  std::istringstream iss(line);

  size_t num_vms;
  if(iss >> num_vms) {
  }

  size_t prev_job_id = 0;
  size_t current_job_id = 0;

  for (size_t i = 0; i < num_vms; i++){
    getline(infile, line);
    iss = std::istringstream(line);

    job j;
    if ((iss >> current_job_id) && (prev_job_id != current_job_id)){
      prob.jobs.push_back(j);

      prev_job_id = current_job_id;
      j.vms = std::vector<virtual_machine>();
    }

    virtual_machine vm;
    std::string anti_col;

    j.id = current_job_id;
    iss >> vm.id >> vm.cpu_req >> vm.ram_req >> anti_col;
    vm.anti_col = (anti_col == "True");

    j.vms.push_back(vm);

    if (i + 1 == num_vms) {
      prob.jobs.push_back(j);
    }
  }

}

void create_h(problem &prob) {
  for (std::size_t i = 1; i < prob.jobs.size(); ++i) {
    const auto accum = prob.h[i - 1] + prob.jobs[i - 1].vms.size();
    prob.h.push_back(accum);
  }
}

problem parse(std::istream &infile) {
  problem prob;

  parse_servers_spec(infile, prob);
  parse_vms_spec(infile, prob);
  create_h(prob);

  return prob;
}
