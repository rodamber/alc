#pragma once

#include <vector>


struct server {
  server() = default;
  server(std::size_t id_, std::size_t cpu_cap_, std::size_t ram_cap_)
    : cpu_cap(cpu_cap_), ram_cap(ram_cap_), id(id_) {
  }

  friend bool operator==(const server &x, const server &y) {
    return x.cpu_cap == y.cpu_cap
      && x.ram_cap == y.ram_cap
      && x.id == y.id;
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

  friend bool operator==(const virtual_machine &x, const virtual_machine &y) {
    return x.cpu_req == y.cpu_req
      && x.ram_req == y.ram_req
      && x.id == y.id
      && x.anti_col == y.anti_col;
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

  friend bool operator==(const job &x, const job &y) {
    return x.id == y.id && x.vms == y.vms;
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

  friend bool operator==(const problem &x, const problem &y) {
    return x.servers == y.servers
      && x.jobs == y.jobs
      && x.h == y.h;
  }

  std::vector<server> servers;
  std::vector<job> jobs;
  std::vector<std::size_t> h;
};
