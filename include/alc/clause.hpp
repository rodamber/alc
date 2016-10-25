#pragma once

#include <cstdint>
#include <initializer_list>
#include <list>


namespace alc {

  struct clause {
    clause() = default;

    clause(const clause &cl) : literals(cl.literals) { }
    clause(clause &&cl) : literals(std::move(cl.literals)) { }

    clause(std::initializer_list<std::int64_t> lits) : literals(lits) { }


    std::list<std::int64_t> literals;

    void add(std::initializer_list<std::int64_t> &&lits) {
      literals.splice(literals.end(), lits);
    }

    void add(std::int64_t literal) {
      literals.push_back(literal);
    }
  };

};
