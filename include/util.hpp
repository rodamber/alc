#include <algorithm>
#include <string>
#include <vector>

// From Rosetta code (slightly modification)
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
