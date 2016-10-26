#include <cassert>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <string.h>

#include <alc/parser.hpp>

void parse_servers_spec(std::istream &infile, alc::problem &prob) {
  std::string line;
  getline(infile, line);
  std::istringstream iss(line);

  size_t num_servers;
  if (iss >> num_servers) {
  }

  for(size_t i = 0; i < num_servers; i++){
    getline(infile, line);
    iss = std::istringstream(line);

    alc::server s;
    if(iss >> s.id >> s.cpu_cap >> s.ram_cap){
      prob.servers.push_back(s);
    }
  }
}


void parse_vms_spec(std::istream &infile, alc::problem &prob) {

  std::string line;
  getline(infile, line);

  std::size_t id = 0;

  while (getline(infile, line)) {
    std::size_t job_id, job_index, cpu_req, ram_req;
    std::string anti_collocation;

    std::istringstream iss(line);
    iss >> job_id >> job_index >> cpu_req >> ram_req >> anti_collocation;

    prob.vms.push_back(alc::virtual_machine(id++, job_id, job_index, cpu_req, ram_req,
                                            (anti_collocation == "True")));
  }

}

void fill_job_sizes(alc::problem &prob) {
  std::size_t job_id = 0;

  for (auto vm_it = prob.vms.begin(); vm_it != prob.vms.end(); ++vm_it) {
    if (vm_it->job_id != job_id) {
      job_id = vm_it->job_id;
      prob.job_sizes.push_back(std::prev(vm_it)->job_index + 1);
    }
  }

  const auto last_vm_it = prob.vms.end() - 1;
  prob.job_sizes.push_back(last_vm_it->job_index + 1);
}

alc::problem alc::parse(std::istream &infile) {
  alc::problem prob;

  parse_servers_spec(infile, prob);
  parse_vms_spec(infile, prob);
  fill_job_sizes(prob);

  return prob;
}
