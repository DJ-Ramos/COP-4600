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
    inputFile = sys.argv[1]

    # Get the base filename (without extension)
    base_filename = os.path.splitext(inputFile)[0]

    # Create the new filename with the desired extension
    outputFile = base_filename + ".out"

    validAlgos = {
        'fcfs': 'First-Come First-Served',
        'sjf': 'Preemptive Shortest Job First',
        'rr': "Round Robin"
    }

    file = open(
        rf"{os.path.dirname(os.path.realpath(__file__))}/pa1-testfiles/{inputFile}", 'r')
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

    if use == 'fcfs':
        fifo_scheduler(processes, runfor)
    else:
        # Handle other cases here
        pass

    directive = file.readline().split()
    if directive[0] == 'end':
        file.close
        with open(outputFile, "w") as f:
            for process in processes:
                print(f"{process.name} wait\t{process.waiting_time} turnaround\t{process.turnaround_time} response\t{process.response_time}", file=f)

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
        print(f'{process.name} wait {process.waiting_time:3} turnaround {process.turnaround_time:3} response {process.response_time:3}')


def fifo_scheduler(processes, runfor):
    
    print(f'{len(processes)} processes')
    print('Using First-Come First-Served')
    processes.sort(key=lambda x: x.arrival_time)
    fifo_queue = processes.copy()
    current_time = 0
    i = 0
    queue = []
    
    while processes or queue:
        # Check for arriving processes at this time and queue them
        while processes and processes[0].arrival_time <= current_time:
            arriving_process = processes.pop(0)
            queue.append(arriving_process)
            print(f"Time {current_time:3} : {arriving_process.name} arrived")

        if queue:
            # If there's a process to run, select and run it
            current_process = queue.pop(0)
            print(f"Time {current_time:3} : {current_process.name} selected (burst {current_process.burst_time:3})")
            current_process.start_time = current_time
            for _ in range(current_process.burst_time):
                # Check for process arrivals during the burst time
                current_time += 1
                for i in range(len(processes)):
                    if processes and processes[i].arrival_time == current_time:
                        arriving_process = processes.pop(i)
                        queue.append(arriving_process)
                        print(f"Time {current_time:3} : {arriving_process.name} arrived")
                        break  # Process the next time step

            print(f"Time {current_time:3} : {current_process.name} finished")
            current_process.finish_time = current_process.start_time + current_process.burst_time
        else:
            # If no process is running and there are processes yet to arrive
            if processes:
                print(f"Time {current_time:3} : Idle")
                current_time += 1  # Increment time until the next process arrives      
    
    # After all processes are finished
    for x in range(current_time, runfor):
        print(f'Time {current_time:3} : Idle')
        current_time = current_time + 1
        
    print(f"Finished at time {runfor}\n")
    calculate_metrics(fifo_queue)
    

if __name__ == "__main__":
    main(sys.argv[1:])
