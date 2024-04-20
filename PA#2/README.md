# ChatGPT Usage in Makefile creation

While initially learning to create and manage makefiles I initially started with online tutorials such as makefiletutorial.com I found myself getting lost within the work. Majority of all the tutorials I tried online were to archaic and pretty confusing so eventually I went to ChatGPT to find some help understanding the context behind each term and the syntax surround makefiles. The information provided was far clearer and would even be easier to find solutions to problems I would face since being able to ask directly for an explanation would prove to be faster than having to search through different paragraphs for context. It was especially useful when the AI provided me with an initial template upon my first time asking if it new anything about makefile basics. The code for the template is as follows: 

# This is a comment

# Variable definitions
CC = gcc
CFLAGS = -Wall -g

# Rule to build the executable
my_program: main.o functions.o
    $(CC) $(CFLAGS) -o my_program main.o functions.o

# Rule to compile main.c
main.o: main.c
    $(CC) $(CFLAGS) -c main.c

# Rule to compile functions.c
functions.o: functions.c
    $(CC) $(CFLAGS) -c functions.c

# Rule to clean the project
clean:
    rm -f *.o my_program

