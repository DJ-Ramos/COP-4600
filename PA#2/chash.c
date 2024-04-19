#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include "hashdb.h"

#define MAX_COMMAND_LENGTH 50

void *process_command(void *arg);

typedef struct
{
    char command[MAX_COMMAND_LENGTH];
} commandStruct;

FILE *output_file = NULL;
pthread_mutex_t output_lock;

int main()
{
    FILE *fptr = fopen("commands.txt", "r");
    char line[MAX_COMMAND_LENGTH];
    memset(line, '\0', sizeof(char));
    int num_commands;

    if (!fptr)
    {
        perror("Failed to open file");
        return EXIT_FAILURE;
    }

    fgets(line, sizeof(line), fptr); // Read the first line for number of threads
    sscanf(line, "threads,%d,0", &num_commands);
    printf("Running %d threads\n", num_commands);
    pthread_t *threads = malloc(num_commands * sizeof(pthread_t));
    if (threads == NULL)
    {
        perror("Failed to allocate memory for threads");
        fclose(fptr);
        return EXIT_FAILURE;
    }

    commandStruct *commands = malloc(num_commands * sizeof(commandStruct));
    if (commands == NULL)
    {
        perror("Failed to allocate memory for commands");
        free(threads);
        fclose(fptr);
        return EXIT_FAILURE;
    }

    output_file = fopen("output.txt", "w");
    if (!output_file)
    {
        perror("Failed to open output file");
        free(threads);
        free(commands);
        fclose(fptr);
        return EXIT_FAILURE;
    }

    int i = 0;
    while (fgets(line, sizeof(line), fptr) && i < num_commands)
    {
        strcpy(commands[i].command, line);
        pthread_create(&threads[i], NULL, process_command, &commands[i]);
        i++;
    }

    for (int j = 0; j < i; j++)
    {
        pthread_join(threads[j], NULL);
    }

    fclose(fptr);
    fclose(output_file);
    free(threads);
    free(commands);
    return 0;
}

void *process_command(void *arg)
{
    commandStruct *cmd = (commandStruct *)arg;
    char name[50];
    uint32_t salary;

    if (sscanf(cmd->command, "insert,%50[^,],%u", name, &salary) == 2)
    {
        insert(name, salary);
    }
    else if (sscanf(cmd->command, "delete,%50s", name) == 1)
    {
        delete(name);
    }
    else if (sscanf(cmd->command, "search,%50s", name) == 1)
    {
        uint32_t found_salary = search(name);
        pthread_mutex_lock(&output_lock);
        fprintf(output_file, "%s: %u\n", name, found_salary);
        pthread_mutex_unlock(&output_lock);
    }
    else if (strcmp(cmd->command, "print,0,0\n") == 0)
    {
        print();
    }

    return NULL;
}
