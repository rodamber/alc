#include <algorithm>
#include <utility>

#include <alc/polynomial_solver.hpp>
#include <util.hpp>


// Tries to assign a virtual_machine to a server. Returns true if successful, false
// otherwise.
bool assign(const alc::virtual_machine &vm,
            alc::server &s,
            std::vector<alc::configuration> &configurations) {
  if (s.cpu_cap < 1 || s.ram_cap < 1)
    return false;

  --s.cpu_cap;
  --s.ram_cap;

  configurations.push_back({ vm.job_id, vm.job_index, s.id });

  return true;
}

// Tries to assign all the vms.
void assign_vms_to_servers(const std::vector<job> &jobs,
                           std::vector<alc::server> &servers,
                           std::vector<alc::configuration> &configurations) {

  for (auto &job: jobs) {
    auto server_it = servers.begin();

    for (auto vm_it = job.begin(); vm_it != job.end(); /* empty */) {
      if (server_it == servers.end()) {
        server_it = servers.begin();
      }

      if (assign(*vm_it, *server_it, configurations)) {
        // Got a hit!
        ++vm_it;
      }

      ++server_it;
    }
  }
}

std::pair<std::vector<job>, std::vector<job>>
jobs_stable_partition(const std::vector<job> &jobs) {
  std::vector<job> jobs_vms_anti_col, jobs_vms_not_anti_col;

  for (auto &j: jobs) {
    auto pair = stable_partition(j, [](alc::virtual_machine vm) {
        return vm.anti_collocation;
      });

    jobs_vms_anti_col.push_back(pair.first);
    jobs_vms_not_anti_col.push_back(pair.second);
  }

  return { jobs_vms_anti_col, jobs_vms_not_anti_col };
}

std::size_t count_distinct_abs(std::vector<std::size_t> v) {
  std::transform(v.begin(), v.end(), v.begin(), abs);
  std::sort(v.begin(), v.end());

  auto unique_end = std::unique(v.begin(), v.end());
  return std::distance(v.begin(), unique_end);
}

// -----------------------------------------------------------------------------
// Solution

alc::solution alc::polynomial_solver::solution() {

  // Sort servers by descending order of min(cpu, ram) capacity
  std::sort(problem_.servers.begin(), problem_.servers.end(), [](server a, server b) {
      return std::min(a.cpu_cap, a.ram_cap) > std::min(b.cpu_cap, b.ram_cap);
    });


  // Get VMs organized by job
  std::vector<job> jobs;
  group_by(problem_.vms, jobs, [](virtual_machine a, virtual_machine b) {
      return a.job_id == b.job_id;
    });


  // Sort jobs by descending number of VMs anti-collocation
  std::sort(jobs.begin(), jobs.end(), [](job a, job b) {
      return vms_ac_count(a) > vms_ac_count(b);
    });


  // Atribute VMs to the servers
  // Start by the VMs anti-collocation for each job by the order defined earlier

  auto pair = jobs_stable_partition(jobs);
  std::vector<alc::configuration> configurations;

  assign_vms_to_servers(pair.first, problem_.servers, configurations);
  assign_vms_to_servers(pair.second, problem_.servers, configurations);


  // Then sort the configurations by job id, then by vm index.
  std::sort(configurations.begin(), configurations.end(), [](configuration a, configuration b) {
      return a.vm_index < b.vm_index;
    });

  std::stable_sort(configurations.begin(), configurations.end(), [](configuration a, configuration b) {
      return a.job_id < b.job_id;
    });

  // Count the number of servers used
  std::vector<std::size_t> servers_used;
  for (auto config: configurations) {
    servers_used.push_back(config.server_id);
  }

  const auto server_count = count_distinct_abs(servers_used);

  return { server_count, configurations };
}
