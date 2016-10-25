#pragma once

#include <experimental/optional>
#include <list>

#include <alc/clause.hpp>


namespace alc {

  class solver {
  public:

    solver() = default;

    // Tries to solve the problem and returns a model if one is found.
    std::list<std::int64_t> solve();


    // Adds clauses to the solver. The argument will be emptied.
    // Complexity: O(1)
    void add_clauses(std::list<alc::clause> &clauses);
    void add_clauses(std::list<alc::clause> &&clauses);

    inline std::int64_t new_var() {
      return var_count_++;
    }

  private:
    // The current number of variables.
    std::int64_t var_count_= 0;

    // The clauses.
    std::list<alc::clause> clauses_;

  private:
    // Uses a SAT solver to search for the minimum number of up servers.
    // Returns the model if one is found.
    std::experimental::optional<std::list<std::int64_t>> search() const;

  };

};
