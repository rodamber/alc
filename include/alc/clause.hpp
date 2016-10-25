#pragma once

#include <cstdint>
#include <list>


namespace alc {

  struct clause {
    clause() = default;

    std::list<std::int64_t> literals;

    void add(std::int64_t literal) {
      literals.push_back(literal);
    }
  };

};
