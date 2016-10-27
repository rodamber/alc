#include <util.hpp>

std::vector<std::vector<int>> combinations(int N, int K) {
  std::string bitmask(K, 1); // K leading 1's
  bitmask.resize(N, 0); // N-K trailing 0's

  std::vector<std::vector<int>> all_combinations;

  // print integers and permute bitmask
  do {
    std::vector<int> combination;

    for (int i = 0; i < N; ++i) { // [0..N-1] integers
      if (bitmask[i]) {
        combination.push_back(i);
      }
    }
    all_combinations.push_back(combination);
  } while (std::prev_permutation(bitmask.begin(), bitmask.end()));

  return all_combinations;
}

std::size_t vms_ac_count(const job &job) {
  return std::count_if(job.begin(), job.end(), [](alc::virtual_machine vm) {
      return vm.anti_collocation;
    });
}

std::size_t max_anti_collocation_count_per_vm(const std::vector<alc::virtual_machine> &vms) {
  // Get VMs organized by job
  std::vector<job> jobs;
  group_by(vms, jobs, [](alc::virtual_machine a, alc::virtual_machine b) {
      return a.job_id == b.job_id;
    });

  std::vector<std::size_t> anti_collocation_counts;

  for (auto &j: jobs) {
    anti_collocation_counts.push_back(vms_ac_count(j));
  }

  return *std::max_element(anti_collocation_counts.begin(), anti_collocation_counts.end());
}
