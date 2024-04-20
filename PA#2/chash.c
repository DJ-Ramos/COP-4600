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

FILE *outputFile;
unsigned short numLock = 0, numRecord = 0;
pthread_mutex_t output_lock;

int main()
{
    FILE *fptr = fopen("commands.txt", "r");
    char line[MAX_COMMAND_LENGTH];
    memset(line, '\0', 50 * sizeof(char));
    int num_commands;

    if (!fptr)
    {
        perror("Failed to open file");
        return EXIT_FAILURE;
    }

    fgets(line, sizeof(line), fptr); // Read the first line for number of threads
    sscanf(line, "threads,%d,0", &num_commands);
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

    outputFile = fopen("output.txt", "w");
    if (!outputFile)
    {
        perror("Failed to open output file");
        free(threads);
        free(commands);
        fclose(fptr);
        return EXIT_FAILURE;
    }

    fprintf(outputFile, "Running %d threads\n", num_commands);

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

    hashRecord *records = sortRecords(numRecord);
    numLock++;
    fprintf(outputFile, "Number of lock acquisitions: %u\n", numLock);
    fprintf(outputFile, "Number of lock releases: %u\n", numLock);
    fprintf(outputFile, "Final Table:\n");

    for(int i = 0; i < numRecord; i++)
    {
        fprintf(outputFile,"%u,%s,%u\n", records->hash, records->name, records->salary);
        records = records->next;
    }

    fclose(fptr);
    fclose(outputFile);
    free(threads);
    free(commands);
    return EXIT_SUCCESS;
}

void *process_command(void *command)
{
    commandStruct *cmd = (commandStruct *)command;
    char name[50];
    uint32_t salary;

    if (sscanf(cmd->command, "insert,%50[^,],%u", name, &salary) == 2)
    {
        insert(name, salary);
        numRecord++;
        numLock++;
    }
    else if (sscanf(cmd->command, "delete,%50[^,]", name) == 1)
    {
        delete(name);
        numRecord--;
        numLock++;
    }
    else if (sscanf(cmd->command, "search,%50[^,]", name) == 1)
    {
        hashRecord *record = search(name);
        pthread_mutex_lock(&output_lock);
        if (record == NULL)
        {
            fprintf(outputFile, "No Record Found\n");
        }
        else
        {
            fprintf(outputFile, "%u,%s,%u\n", record->hash, record->name, record->salary);
        }
        pthread_mutex_unlock(&output_lock);
        numLock++;
    }
    else if (strcmp(cmd->command, "print,0,0\n") == 0)
    {
        print();
        numLock++;
    }

    return NULL;
}
