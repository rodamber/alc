#pragma once

#include <algorithm>
#include <string>
#include <vector>

// From Rosetta code (slightly modification)
// std::vector<std::vector<int>> combinations(int N, int K) {
//   std::string bitmask(K, 1); // K leading 1's
//   bitmask.resize(N, 0); // N-K trailing 0's

//   std::vector<std::vector<int>> all_combinations;

//   // print integers and permute bitmask
//   do {
//     std::vector<int> combination;

//     for (int i = 0; i < N; ++i) { // [0..N-1] integers
//       if (bitmask[i]) {
//         combination.push_back(i);
//       }
//     }
//     all_combinations.push_back(combination);
//   } while (std::prev_permutation(bitmask.begin(), bitmask.end()));

//   return all_combinations;
// }

// Generator functor. Lazily generates all the possible k-combinations of the
// numbers from 0 to N - 1.
class combination_generator {
public:
  combination_generator(int N, int K)
    : bitmask_(K, 1), N_(N), K_(K) {
    bitmask_.resize(N, 0);
  }

public:
  std::vector<int> operator()() {
    auto combination = yield();
    next();
    return combination;
  }

  std::vector<int> yield() const {
    if (finished_)
      return {};

    std::vector<int> combination;

    for (int i = 0; i < N_; ++i)
      if (bitmask_[i])
        combination.push_back(i);

    return combination;
  }

  void next() {
    finished_ = !std::prev_permutation(bitmask_.begin(), bitmask_.end());
  }

private:
  std::string bitmask_;

  const int N_;
  const int K_;

  bool finished_ = false;
};

// private:
//   combination_generator(bool finished)
//     : N_(0), K_(0), finished_(finished) {
//   }

// class combination_iterator {
// public:
//   combination_iterator(combination_generator &generator)
//     : generator_(generator) {
//   }

//   combination_iterator(combination_generator &&generator)
//     : generator_(generator) {
//   }

//   combination_iterator &operator++() {
//     generator_.next();
//     return *this;
//   }

//   std::vector<int> operator*() const {
//     return generator_.yield();
//   }

//   bool operator!=(const combination_iterator &c_it) const {
//     return **this != *c_it;
//   }

// private:
//   combination_generator &generator_;
// };

// using iterator = combination_iterator;

// iterator begin() { return combination_iterator(*this);}
// iterator end() { return combination_iterator(combination_generator(true)); }
