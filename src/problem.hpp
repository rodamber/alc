#pragma once

#include <vector>


struct server {
  server() = default;
  server(std::size_t id_, std::size_t cpu_cap_, std::size_t ram_cap_)
    : cpu_cap(cpu_cap_), ram_cap(ram_cap_), id(id_) {
  }

  std::size_t cpu_cap;
  std::size_t ram_cap;
  std::size_t id;
};

struct virtual_machine {
  virtual_machine() = default;
  virtual_machine(std::size_t id_, std::size_t cpu_req_, std::size_t ram_req_, bool anti_col_)
    : cpu_req(cpu_req_), ram_req(ram_req_), id(id_), anti_col(anti_col_) {
  }

  std::size_t cpu_req;
  std::size_t ram_req;
  std::size_t id;
  bool anti_col;
};

struct job {
  job() = default;
  job(std::size_t id_, const std::vector<virtual_machine> &vms_)
    : id(id_), vms(vms_) {
  }

  std::size_t id;
  std::vector<virtual_machine> vms;
};

struct problem {
  problem() = default;
  problem(const std::vector<server> &servers_, const std::vector<job> &jobs_,
          const std::vector<std::size_t> &h_)
    : servers(servers_), jobs(jobs_), h(h_) {
  }

  std::vector<server> servers;
  std::vector<job> jobs;
  std::vector<std::size_t> h;
};
