import sys
import os


class Process:
    def __init__(self, name, arrival_time, execution_time, status):
        self.name = name
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.status = status


def main(argv):
    # inputFile = sys.argv[1]
    validAlgos = ['fcfs', 'sjf', 'rr']
    file = open(
        rf"{os.path.dirname(os.path.realpath(__file__))}/pa1-testfiles/c2-fcfs.in", 'r')
    processes = []

    directive = file.readline().split()
    if directive[0].lower() == 'processcount' and directive[1].isdecimal() >= 0:
        processcount = directive[1]
    else:
        print('Error: Missing parameter "processcount"')

    directive = file.readline().split()
    if directive[0].lower() == 'runfor' and directive[1].isdecimal() >= 0:
        runfor = directive[1]
    else:
        print('Error: Missing parameter "runfor"')

    directive = file.readline().split()
    if directive[0].lower() == 'use' and directive[1] in validAlgos:
        use = directive[1]
        if use == 'rr':
            directive = file.readline().split()
            if directive[0].lower() == 'quantum' and directive[1].isdecimal() >= 0:
                quantum = directive[1]
            else:
                print('Error: Missing quantum parameter when use is rr')
    else:
        print('Error: Missing parameter "use"')

    for directive in range(int(processcount)):
        directive = file.readline().split()
        if directive[0].lower() == 'process' and directive[1].lower() == 'name' and directive[3].lower() == 'arrival' and directive[4].isdecimal() >= 0 and directive[5].lower() == 'burst' and directive[6].isdecimal() >= 0:
            processes.append(Process(directive[2], directive[4], 8, "huh"))
        else:
            print('Error: Missing parameter "process"')

    directive = file.readline().split()
    if directive[0] == 'end':
        file.close
    else:
        print('Error: Missing parameter end')


if __name__ == "__main__":
    main(sys.argv[1:])
