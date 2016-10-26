#pragma once

#include <experimental/optional>
#include <iostream>
#include <list>

#include <alc/clause.hpp>


namespace alc {

  class solver {
  public:

    solver() : var_count_(0) { }

    // Tries to solve the problem and returns a model if one is found.
    std::experimental::optional<std::list<std::int64_t>> solve();

    // Adds clauses to the solver. The argument will be emptied.
    // Complexity: O(1)
    void inline add_clause(alc::clause &&clause) {
      clauses_.push_back(clause);
    }

    inline std::int64_t new_var() {
      return ++var_count_;
    }

    inline std::int64_t var_count() const {
      return var_count_;
    }

    std::list<std::list<std::int64_t>> clauses() const;

    void write_dimacs_cnf(std::ostream &os);

  private:
    // The current number of variables.
    std::int64_t var_count_;

    // The clauses.
    std::list<alc::clause> clauses_;

  };

};
