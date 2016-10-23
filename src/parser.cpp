#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <string.h>

#include "parser.hpp"

problem parse(std::istream& infile) {
  size_t num_servers;
  size_t num_jv_pairs; 
  
  std::string line;
  
  getline(infile, line);
  std::istringstream iss(line);

  if (iss >> num_servers) {}
  
  server s;
  problem p;
  
  for(size_t tmp = 0; tmp < num_servers; tmp++){
    getline(infile, line);
    iss = std::istringstream(line);
	if(iss >> s.id >> s.cpu_cap >> s.ram_cap){
		p.servers.push_back(s);
	}
  }

  //num of (jobs, machines)
  getline(infile, line);
  iss = std::istringstream(line);

  if(iss >> num_jv_pairs) {}
  
  job j;
  virtual_machine v;
  size_t prev_id = 0;
  size_t next_id = 0;
  std::string alloc;
  for(size_t tmp = 0; tmp < num_jv_pairs; tmp++){
	getline(infile, line);
	iss = std::istringstream(line);
	
	if((iss >> next_id) && (prev_id != next_id)){
	  p.jobs.push_back(j);
	  prev_id = next_id;
	  j.vms = std::vector<virtual_machine>();
	}
	
	j.id = next_id;
	iss >> v.id;
	iss >> v.cpu_req;
	iss >> v.ram_req;
	iss >> alloc;
	
	if(alloc == "True"){
	  v.anti_col = true;
	}
	else{
	  v.anti_col = false;
	}
	j.vms.push_back(v);
  }
  p.jobs.push_back(j);
/*  
  std::cout << num_servers << std::endl;
  
  for(server s : p.servers)
    std::cout << s.id <<" "<<s.cpu_cap<<" "<<s.ram_cap<< std::endl;

  std::cout << num_jv_pairs << std::endl;
  
  for(job j: p.jobs){
	  for(virtual_machine v: j.vms){
	    std::cout << j.id <<" " << v.id <<" "<<v.cpu_req<<" "<<v.ram_req<< " ";
		if(v.anti_col == 1)
			std::cout << "True" << std::endl;
		else{std::cout << "False"<< std::endl;}
	  }
  }*/
  return p;
}

int main(int argc, char* argv[]) {
  if (argc < 2 || (argc == 2 && !strcmp(argv[1], "--help"))) {
    std::cout << "USAGE: graphcol <input-file>" << std::endl;
    return 0;
  }
	
  const char* filename = argv[1];
  std::ifstream infile(filename);
	
  problem p = parse(infile);

 return 0;
}