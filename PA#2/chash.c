#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum
{
    threads,
    insert,
    delete,
    search,
    print
} COMMAND;

int cmdStrToEnum(char *commandName);

int main(int argc, char **argv)
{
    int salary = 0;
    int arraySize = 0;
    char *name = (char *)malloc((40) * sizeof(char));
    char *commandName = (char *)malloc((8) * sizeof(char));
    char *fileRow = (char *)malloc((100) * sizeof(char));

    FILE *fptr = fopen("commands.txt", "r");

    if (fptr == NULL)
    {
        fprintf(stderr, "File not found or could not be opened\n");
        return EXIT_FAILURE;
    }

    COMMAND commandEnum;
    while (fgets(fileRow, 100, fptr) != NULL)
    {
        fileRow[strlen(fileRow) - 1] = '\0';
        char *token = strtok(fileRow, ",");

        for (size_t i = 0; i < 3; i++)
        {
            if (i == 0)
            {
                strcpy(commandName, token);
            }
            else if (i == 1)
            {
                if (atoi(token) != 0)
                {
                    arraySize = atoi(token);
                }
                else
                {
                    strcpy(name, token);
                }
            }
            else
            {
                salary = atoi(token);
            }
            token = strtok(NULL, ",");
        }

        commandEnum = cmdStrToEnum(commandName);

        switch (commandEnum)
        {
        case threads:
            printf("Threads\n");
            break;
        case insert:
            printf("Insert\n");
            break;
        case delete:
            printf("Delete\n");
            break;
        case search:
            printf("Search\n");
            break;
        case print:
            printf("Print\n");
            break;
        default:
            fprintf(stderr, "Inputted Command Does Not Exist\n");
            break;
        }
    }

    return 0;
}

int cmdStrToEnum(char *commandName)
{
    if (strcmp(commandName, "threads") == 0)
    {
        return 0;
    }
    else if (strcmp(commandName, "insert") == 0)
    {
        return 1;
    }
    else if (strcmp(commandName, "delete") == 0)
    {
        return 2;
    }
    else if (strcmp(commandName, "search") == 0)
    {
        return 3;
    }
    else if (strcmp(commandName, "print") == 0)
    {
        return 4;
    }
    return -1;
}
