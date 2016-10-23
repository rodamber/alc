#pragma once

#include <vector>


struct server {
  std::size_t cpu_cap;
  std::size_t ram_cap;
  std::size_t id;
};

struct virtual_machine {
  std::size_t cpu_req;
  std::size_t ram_req;
  bool anti_col;
  std::size_t id;
};

struct job {
  std::vector<virtual_machine> vms;
  std::size_t id;
};

struct problem {
  std::vector<server> servers;
  std::vector<job> jobs;
};
