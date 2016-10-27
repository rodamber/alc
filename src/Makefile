.PHONY: clean

# Declaration of variables
CC = g++
CC_FLAGS = -std=c++17 -Wall -Wextra -Wfatal-errors -Wno-unused-parameter -O3 \
					 -Wno-unused-variable -I../include -I.. -I./ -I./minisat \
					 -Wno-literal-suffix -Wno-parentheses

# File names
EXEC = proj1
SOURCES = $(wildcard *.cpp alc/*.cpp)
OBJECTS = $(SOURCES:.cpp=.o)

# Main target
$(EXEC): $(OBJECTS)
	(cd minisat/core; make )
	$(CC) $(OBJECTS) minisat/core/Solver.o -o $(EXEC)

# To obtain object files
%.o: %.cpp
	$(CC) -c $(CC_FLAGS) $< -o $@

# To remove generated files
clean:
	rm -f $(EXEC) $(OBJECTS)
	(cd minisat/core; make clean)
