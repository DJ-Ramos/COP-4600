# Compiler and flags
CC = gcc
CFLAGS = -Wall -pthread
LDFLAGS = -lm

# Source files
SRCS = chash.c hashdb.c rwlocks.c
OBJS = $(SRCS:.c=.o)

# Executable
TARGET = chash

# Output file
OUTPUT_FILE = output.txt

# Phony targets
.PHONY: all clean

# Default target
all: $(TARGET)

# Compile rule for object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Linking rule
$(TARGET): $(OBJS)
	$(CC) $(OBJS) $(LDFLAGS) -o $(TARGET)

# Rule for creating output.txt
$(OUTPUT_FILE):
	touch $(OUTPUT_FILE)

# Clean rule
clean:
	rm -f $(OBJS) $(TARGET) $(OUTPUT_FILE)
