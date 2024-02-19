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
        self.remaining_time = burst_time


def main(argv):
    inputFile = sys.argv[1]
    import os

    # Get the base filename (without extension)
    base_filename = os.path.splitext(inputFile)[0]

    # Create the new filename with the desired extension
    outputFile = base_filename + ".out"

    validAlgos = {
        'fcfs': 'First In First Out',
        'sjf': 'Preemptive Shortest Job First',
        'rr': "Round Robin"
    }

    file = open(
        rf"{os.path.dirname(os.path.realpath(__file__))}/pa1-testfiles/c2-rr.in", 'r')
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
        fifo_schedular(processes, runfor)
    elif use == 'rr':
        rr_schedular(processes, runfor, quantum)
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

def execute(currentProcess, quantum):
        if currentProcess.remaining_time > quantum:
            print(f"Executing {currentProcess.name} for {quantum} units of time")
            currentProcess.remaining_time -= quantum
            return quantum
        else:
            print(f"Executing {currentProcess.name} for {currentProcess.remaining_time} units of time")
            time_executed = currentProcess.remaining_time
            currentProcess.remaining_time = 0
            return time_executed
    
def is_completed(currentProcess):
        return currentProcess.remaining_time == 0

def rr_schedular(processes, time_units, quantum):
    print(f"  {len(processes)} processes")
    print ("Using Round-Robin")
    print(f"Quantum   {quantum}\n")

    currentTime = 0
    
    # Sort the processes by arrival time
    processes.sort(key=lambda x: x.arrival_time)

    # Copy the processes into the queue
    queue = []

    # Run for amount of time aloted
    for currentTime in range(time_units):
        # Go through each process and add them to the queue if they have arrived
        for process in processes:
            if(process.arrival_time == currentTime):
                print(f"Time   {currentTime} : {process.name} arrived")
                queue.append(process)

        if queue:
            # Grab the first process to be processed
            currentProcess = queue.pop(0)
            
            # Now take that process and decrement it by one
            # If it finishes then move on to the next task
            # if it still needs more time after going over the time slice
            # readd to queue
            currentProcess.start_time = currentTime
            time_executed = min(quantum, currentProcess.remaining_time)
            currentProcess.remaining_time -= 1

            # After a time slice if process isn't completed add it back to the queue
            if not is_completed(currentProcess):
                queue.append(currentProcess)
            
        else:
            # If the queue is empty
            print(f"Time {currentTime} : Idle")

    print(f"\nFinished at time  {time_units}\n")
    calculate_metrics(processes)





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
