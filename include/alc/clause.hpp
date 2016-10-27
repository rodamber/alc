#pragma once

#include <cstdint>
#include <initializer_list>
#include <iostream>
#include <list>


namespace alc {

  struct clause {
    clause() = default;

    clause(const clause &cl) : literals(cl.literals) { }
    clause(clause &&cl) : literals(std::move(cl.literals)) { }

    clause(std::initializer_list<std::int64_t> lits) : literals(lits) { }

    clause &operator=(const clause &c) {
      literals = c.literals;
      return *this;
    }

    void add(std::initializer_list<std::int64_t> &&lits) {
      literals.splice(literals.end(), lits);
    }

    void add(std::int64_t literal) {
      literals.push_back(literal);
    }

    inline std::size_t size() const {
      return literals.size();
    }

    friend std::ostream &operator<<(std::ostream &os, const clause &c) {
      for (auto &lit: c.literals) {
        os << lit << " ";
      }
      return (os << " 0\n");
    }


    std::list<std::int64_t> literals;

  };

};
