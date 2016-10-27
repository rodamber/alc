.PHONY: clean

# Declaration of variables
CC = g++
CC_FLAGS = -std=c++17 -Wall -Wextra -Wfatal-errors -Wno-unused-parameter -O3 \
					 -Wno-unused-variable -I../include -I.. -I./ -I../src/minisat -I../src \
					 -Wno-literal-suffix -Wno-parentheses

# File names
EXEC = test
SOURCES = $(wildcard *.cpp) $(wildcard ../src/alc/*.cpp)
OBJECTS = $(SOURCES:.cpp=.o)

# Main target
$(EXEC): $(OBJECTS)
	(cd ../src/minisat/core; make)
	$(CC) $(OBJECTS) ../src/minisat/core/Solver.o -o $(EXEC)

# To obtain object files
%.o: %.cpp
	$(CC) -c $(CC_FLAGS) $< -o $@

# To remove generated files
clean:
	rm -f $(EXEC) $(OBJECTS) ../src/minisat/core/*.o ../src/minisat/utils/*.o ../src/minisat/core/depend.mk ../src/minisat/core/minisat
