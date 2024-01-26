import sys
import os


class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.status = "Waiting"
        self.start_time = 0
        self.finish_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0


def main(argv):
    # inputFile = sys.argv[1]
    validAlgos = {
        'fcfs': 'First In First Out',
        'sjf': 'Preemptive Shortest Job First',
        'rr': "Round Robin"
    }

    file = open(
        rf"{os.path.dirname(os.path.realpath(__file__))}/pa1-testfiles/c10-fcfs.in", 'r')
    processes = []

    directive = file.readline().split()
    if directive[0].lower() == 'processcount' and directive[1].isdecimal() >= 0:
        processcount = int(directive[1])
    else:
        print('Error: Missing parameter "processcount"')

    directive = file.readline().split()
    if directive[0].lower() == 'runfor' and directive[1].isdecimal() >= 0:
        runfor = int(directive[1])
    else:
        print('Error: Missing parameter "runfor"')

    directive = file.readline().split()
    if directive[0].lower() == 'use' and directive[1] in validAlgos:
        use = directive[1]
        if use == 'rr':
            directive = file.readline().split()
            if directive[0].lower() == 'quantum' and directive[1].isdecimal() >= 0:
                quantum = int(directive[1])
            else:
                print('Error: Missing quantum parameter when use is rr')
    else:
        print('Error: Missing parameter "use"')

    for directive in range(processcount):
        directive = file.readline().split()
        if directive[0].lower() == 'process' and directive[1].lower() == 'name' and directive[3].lower() == 'arrival' and directive[4].isdecimal() >= 0 and directive[5].lower() == 'burst' and directive[6].isdecimal() >= 0:
            processes.append(Process(directive[2], int(
                directive[4]), int(directive[6])))
        else:
            print('Error: Missing parameter "process"')

    match use:
        case 'fcfs':
            fifo_schedular(processes, runfor)

    directive = file.readline().split()
    if directive[0] == 'end':
        file.close
        for process in processes:
            print(f'{process.name} wait\t{process.waiting_time} turnaround\t{process.turnaround_time} response\t{process.response_time}')
    else:
        print('Error: Missing parameter end')


def calculate_metrics(processes):
    processes.sort(key=lambda x: x.name)
    for process in processes:
        process.turnaround_time = process.finish_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = process.start_time - process.arrival_time


def fifo_schedular(processes, time_units):
    print('Using First-Come First-Served')
    is_process_running = False
    time_in_queue = 0
    processes.sort(key=lambda x: x.burst_time)
    fifo_queue = []

    for current_time in range(time_units):
        for process in processes:
            if current_time == process.arrival_time:
                print(f'Time \t {current_time} : {process.name} arrived')
                fifo_queue.append(process)
                if is_process_running == False:
                    print(f'Time \t {current_time} : {process.name} selected (burst   {process.burst_time})')
                    process.start_time = current_time
                    process.finish_time = process.start_time + process.burst_time
                    is_process_running = True
            elif current_time == process.finish_time > 0:
                print(f'Time \t {current_time} : {process.name} finished')
                process.status = "finished"
                fifo_queue.pop(0)
                is_process_running = False
                if is_process_running == False and fifo_queue != []:
                    print(f'Time \t {current_time} : {fifo_queue[0].name} selected (burst   {fifo_queue[0].burst_time})')
                    fifo_queue[0].start_time = current_time
                    fifo_queue[0].finish_time = fifo_queue[0].start_time + fifo_queue[0].burst_time
                    is_process_running = True
        if is_process_running == False:
            print(f'Time \t {current_time} : Idle')

    print(f'Finished  at time {time_units}\n')
    calculate_metrics(processes)


if __name__ == "__main__":
    main(sys.argv[1:])
