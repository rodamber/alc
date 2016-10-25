#pragma once

#include <experimental/optional>
#include <vector>

// FIXME: change lib to alc. change makefile so that headers are like #include <alc/problem>
// FIXME: namespace alc

namespace alc {

    class solver {
  public:

    solver() = default;

    std::experimental::optional<std::vector<std::size_t>> solve();

    inline std::size_t new_var() {
      return var_count_++;
    }

  private:
    // The current number of variables.
    std::size_t var_count_= 0;

  private:
    // Uses a SAT solver to search for the minimum number of up servers.
    std::experimental::optional<std::vector<std::size_t>> search() const;

  };

};
