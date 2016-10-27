#pragma once

#include <algorithm>
#include <string>
#include <vector>

#include <alc/problem.hpp>

// ------------------------------------------------------------------------
// Combinations utilities

// From Rosetta code (slightly modification)
std::vector<std::vector<int>> combinations(int N, int K);

// Generator functor. Lazily generates all the possible k-combinations of the
// numbers from 0 to N - 1.
template <class Collection>
class combination_generator {
public:
  combination_generator(const Collection &coll, int K)
    : bitmask_(K, 1), collection_(coll), N_(coll.size()), K_(K) {
    bitmask_.resize(N_, 0);
  }

public:
  Collection operator()() {
    auto combination = yield();
    next();
    return combination;
  }

  Collection yield() const {
    if (finished_)
      return {};

    Collection combination;

    for (int i = 0; i < N_; ++i)
      if (bitmask_[i])
        combination.push_back(collection_.at(i));

    return combination;
  }

  void next() {
    finished_ = !std::prev_permutation(bitmask_.begin(), bitmask_.end());
  }

private:
  std::string bitmask_;

  Collection collection_;

  const int N_;
  const int K_;

  bool finished_ = false;
};




using job = std::vector<alc::virtual_machine>;


template <class T, class BinaryPredicate>
void group_by(const std::vector<T> &origin,
              std::vector<std::vector<T> > &result,
              BinaryPredicate predicate) {
  if(origin.empty())
    return;

  result.clear();
  result.resize(1);
  result[0].push_back(origin[0]);

  for(size_t i = 1; i < origin.size(); ++i) {
    if(!predicate(origin[i], origin[i-1])) {
      result.push_back(std::vector<T>());
    }
    result.back().push_back(origin[i]);
  }
}

template <class T, class UnaryPredicate>
std::pair<std::vector<T>, std::vector<T>>
  stable_partition(const std::vector<T> &xs, UnaryPredicate predicate) {
  std::vector<T> v1, v2;

  for (auto x: xs) {
    if (predicate(x)) {
      v1.push_back(x);
    } else {
      v2.push_back(x);
    }
  }

  return {v1, v2};
}
