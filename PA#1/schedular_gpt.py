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
        self.remaining_time = burst_time
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0


def main(argv):
    #inputFile = sys.argv[1]

    # Get the base filename (without extension)
    #base_filename = os.path.splitext(inputFile)[0]

    # Create the new filename with the desired extension
    #outputFile = base_filename + ".out"

    validAlgos = {
        'fcfs': 'First-Come First-Served',
        'sjf': 'Preemptive Shortest Job First',
        'rr': "Round Robin"
    }

    file = open(
        rf"{os.path.dirname(os.path.realpath(__file__))}/pa1-testfiles/c2-sjf.in", 'r')
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
        processes = fifo_scheduler(processes, runfor)
        calculate_metrics(processes)
    elif use == 'sjf':
        processes = sjf_scheduler(processes, runfor)
        calculate_metrics(processes)
        # Handle other cases here
        pass

    directive = file.readline().split()
    if directive[0] == 'end':
        file.close
        # with open(outputFile, "w") as f:
        #     for process in processes:
        #         print(f"{process.name} wait\t{process.waiting_time} turnaround\t{process.turnaround_time} response\t{process.response_time}", file=f)

        for process in processes:
            print(f'{process.name} wait {process.waiting_time:3} turnaround {process.turnaround_time:3} response {process.response_time:3}')
    else:
        print('Error: Missing parameter end')


def calculate_metrics(processes):
    processes.sort(key=lambda x: x.name)
    for process in processes:
        process.turnaround_time = process.finish_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = process.start_time - process.arrival_time


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
    processes = fifo_queue.copy()
    return processes
    
def sjf_scheduler(processes, time_units):
    remaining_burst_times = [process.burst_time for process in processes]
    total_processes = len(processes)
    time = 0
    selected_process = None
    print("Using preemptive Shortest Job First")
    
    while time < time_units and total_processes >= 0:
        # Track arriving processes
        arrived_processes = [process for process in processes if process.arrival_time == time]
        
        # Print arriving processes
        for process in arrived_processes:
            print(f"Time {time:4} : {process.name} arrived")
            if selected_process is None:
                selected_process = process
        
        # Check if the selected process has finished
        if selected_process is not None and selected_process.status == "Finished":
            selected_process.finish_time = time  # Update finish time
            print(f"Time {time:4} : {selected_process.name} finished")
            selected_process = None
        
        # Select process with shortest burst time
        shortest_burst = float('inf') if selected_process is None else remaining_burst_times[processes.index(selected_process)]
        for process in processes:
            if process.status == "Waiting" and process.arrival_time <= time and remaining_burst_times[processes.index(process)] < shortest_burst:
                shortest_burst = remaining_burst_times[processes.index(process)]
                selected_process = process
        
        # Print selected process if not already running
        if selected_process is not None and selected_process.status != "Running":
            print(f"Time {time:4} : {selected_process.name} selected (burst {remaining_burst_times[processes.index(selected_process)]})")
        
        if selected_process is not None:
            if remaining_burst_times[processes.index(selected_process)] == selected_process.burst_time:
                selected_process.start_time = time
            selected_process.status = "Running"
            remaining_burst_times[processes.index(selected_process)] -= 1
            if remaining_burst_times[processes.index(selected_process)] == 0:
                selected_process.status = "Finished"
                total_processes -= 1
            else:
                for process in processes:
                    if process != selected_process and process.status == "Running":
                        process.status = "Waiting"
        
        # Print idle if no process is running
        if selected_process is None:
            print(f"Time {time:4} : Idle")
        
        time += 1
    
    # Print remaining idle time if any
    while time < time_units:
        if any(process.status == "Running" for process in processes):
            break
        print(f"Time {time:4} : Idle")
        time += 1
    
    print(f"Finished at time {time:4}\n")
    return processes

if __name__ == "__main__":
    main(sys.argv[1:])
