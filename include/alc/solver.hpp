#pragma once

#include <experimental/optional>
#include <list>

#include <alc/clause.hpp>


namespace alc {

  class solver {
  public:

    solver() = default;

    // Tries to solve the problem and returns a model if one is found.
    std::experimental::optional<std::list<std::int64_t>> solve();

    // Adds clauses to the solver. The argument will be emptied.
    // Complexity: O(1)
    void add_clause(alc::clause &&clause);

    inline std::int64_t new_var() {
      return ++var_count_;
    }

    inline std::int64_t var_count() {
      return var_count_;
    }

    std::list<std::list<std::int64_t>> clauses() const {
      std::list<std::list<std::int64_t>> cs;

      for (auto &clause : clauses_) {
        std::list<std::int64_t> clause_copy(clause.literals);
        cs.push_back(clause_copy);
      }

      return cs;
    }

  private:
    // The current number of variables.
    std::int64_t var_count_= 0;

    // The clauses.
    std::list<alc::clause> clauses_;

  };

};
