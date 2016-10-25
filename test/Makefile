.PHONY: clean

# Declaration of variables
CC = g++
CC_FLAGS = -std=c++17 -Wall -Wextra -Wfatal-errors -Wno-unused-parameter -g \
					 -I../include

# File names
EXEC = test
SOURCES = $(wildcard *.cpp) $(wildcard ../src/alc/*.cpp)
OBJECTS = $(SOURCES:.cpp=.o)

# Main target
$(EXEC): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(EXEC)

# To obtain object files
%.o: %.cpp
	$(CC) -c $(CC_FLAGS) $< -o $@

# To remove generated files
clean:
	rm -f $(EXEC) $(OBJECTS)
