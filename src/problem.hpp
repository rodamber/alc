#pragma once

#include <vector>


struct server {
  size_t cpu_cap;
  size_t ram_cap;
  size_t id;
};

struct virtual_machine {
  size_t cpu_req;
  size_t ram_req;
  bool anti_col;
  size_t id;
};

struct job {
  std::vector<virtual_machine> vms;
  size_t id;
};

struct problem {
  std::vector<server> servers;
  std::vector<job> jobs;
};
