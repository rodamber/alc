#pragma once

#include <iostream>

#include "problem.hpp"


void at_least_one_constraint(std::ostream &os, const problem &prob);

void at_most_one_constraint(std::ostream &os, const problem &prob);

void cpu_constraint(std::ostream &os, const problem &prob);

void ram_constraint(std::ostream &os, const problem &prob);

void anti_col_constraint(std::ostream &os, const problem &prob);
