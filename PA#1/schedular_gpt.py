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
        processes, results = fifo_scheduler(processes, runfor)
        calculate_metrics(processes)
    elif use == 'sjf':
        processes, results = sjf_scheduler(processes, runfor)
        calculate_metrics(processes)
    elif use == 'rr':
        processes, results = rr_scheduler(processes, quantum, runfor)
        calculate_metrics(processes)
        # Handle other cases here
        pass

    directive = file.readline().split()
    if directive[0] == 'end':
        file.close
        with open(outputFile, "w") as f:
            for result in results:
                print(result, file=f)
            for process in processes:
                if process.status != "Finished":
                    print(f"{process.name} did not finish", file=f)
                else:
                    print(f"{process.name} wait\t{process.waiting_time} turnaround\t{process.turnaround_time} response\t{process.response_time}", file=f)
    else:
        print('Error: Missing parameter end')


def calculate_metrics(processes):
    processes.sort(key=lambda x: x.name)
    for process in processes:
        process.turnaround_time = process.finish_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = process.start_time - process.arrival_time


def fifo_scheduler(processes, runfor):
    results = []
    results.append(f'{len(processes)} processes')
    results.append('Using First-Come First-Served')
    processes.sort(key=lambda x: x.arrival_time)
    fifo_queue = processes.copy()
    current_time = 0
    i = 0
    queue = []

    
    while processes or queue:
        # Check for arriving processes at this time and queue them
        while processes and processes[0].arrival_time <= current_time and processes[0].status == 'Waiting':
            arriving_process = processes.pop(0)
            queue.append(arriving_process)
            results.append(f"Time {current_time:3} : {arriving_process.name} arrived")
            arriving_process.status = 'Arrived'

        if queue and queue[0].status == 'Arrived':
            # If there's a process to run, select and run it
            current_process = queue.pop(0)
            results.append(f"Time {current_time:3} : {current_process.name} selected (burst {current_process.burst_time:3})")
            current_process.start_time = current_time
            for _ in range(current_process.burst_time):
                # Check for process arrivals during the burst time
                current_time += 1
                for i in range(len(processes)):
                    if processes and processes[i].arrival_time == current_time:
                        arriving_process = processes.pop(i)
                        queue.append(arriving_process)
                        results.append(f"Time {current_time:3} : {arriving_process.name} arrived")
                        arriving_process.status = 'Arrived'
                        break  # Process the next time step

            results.append(f"Time {current_time:3} : {current_process.name} finished")
            arriving_process.status = 'Finished'
            current_process.finish_time = current_process.start_time + current_process.burst_time
        else:
            # If no process is running and there are processes yet to arrive
            if processes:
                results.append(f"Time {current_time:3} : Idle")
                current_time += 1  # Increment time until the next process arrives      
    
    # After all processes are finished
    for x in range(current_time, runfor):
        results.append(f'Time {current_time:3} : Idle')
        current_time = current_time + 1
        
    results.append(f"Finished at time {runfor}\n")
    processes = fifo_queue.copy()
    return processes, results


def sjf_scheduler(processes, time_units):
    # Initialize remaining burst time for each process
    remaining_burst_times = [process.burst_time for process in processes]
    
    # Initialize variables
    time = 0
    selected_process = None
    results = []
    
    results.append("Using preemptive Shortest Job First")
    
    # Main simulation loop
    while time < time_units:
        # 1. Check for arrived processes and append arrival statement to results accordingly
        arrived_processes = [process for process in processes if process.arrival_time == time]
        for process in arrived_processes:
            results.append(f"Time {time:4} : {process.name} arrived")
        
        # 2. Check if the currently selected process has a status of finished
        if selected_process and selected_process.status == "Finished":
            selected_process.finish_time = time  # Set finish time
            results.append(f"Time {time:4} : {selected_process.name} finished")
            selected_process = None  # Reset selected process
        
        # 3. Determine the shortest remaining burst time
        shortest_burst = float('inf') if not selected_process else remaining_burst_times[processes.index(selected_process)]
        
        # 4. Loop through all processes to select the next process
        for process in processes:
            if process.status in ["Waiting", "Running"] and process.arrival_time <= time and process.burst_time < shortest_burst:
                selected_process = process
                shortest_burst = remaining_burst_times[processes.index(selected_process)]
        
        # 5. Set start time if a new process is selected
        if selected_process and remaining_burst_times[processes.index(selected_process)] == selected_process.burst_time:
            selected_process.start_time = time
        
        # 6. If selected process is not None and it has status of waiting, append the selection statement to the results array and give it a status of running
        if selected_process and selected_process.status == "Waiting":
            results.append(f"Time {time:4} : {selected_process.name} selected (burst {remaining_burst_times[processes.index(selected_process)]})")
            selected_process.status = "Running"
        
        # 7. Decrement remaining burst time if a process is running
        if selected_process:
            remaining_burst_times[processes.index(selected_process)] -= 1
        
        # 8. If selected process is not None and its remaining burst time is zero, set status to Finished
        if selected_process and remaining_burst_times[processes.index(selected_process)] == 0:
            selected_process.status = "Finished"
        
        # 9. Check if any processes have Running status and are not the selected process. If so, set their statuses to Waiting
        for process in processes:
            if process != selected_process and process.status == "Running":
                process.status = "Waiting"
        
        # 10. If selected process is None, append an Idle statement to results
        if not selected_process:
            results.append(f"Time {time:4} : Idle")
        
        time += 1  # Increment time
    
    results.append(f"Finished at time {time}\n")
    
    return processes, results


def rr_scheduler(processes, quantum, runfor):
    time = 0
    output = []
    ready_queue = []
    processes.sort(key=lambda x: x.arrival_time)
    finished_processes = 0
    running_process = None
    running_process_start_time = 0
    arrival_before_finish = False
    rr_queue = processes.copy()
    results = []
    
    results.append(f'  {len(processes)} processes')
    results.append('Using Round-Robin')
    results.append(f'Quantum {quantum:3}\n')
    while time < runfor:
        # Check for new arrivals
        for process in processes:
            if process.arrival_time == time:
                ready_queue.append(process)
                results.append(f"Time {time:3} : {process.name} arrived")
        
        if arrival_before_finish == True:
            time += 1
            arrival_before_finish = False

        # Check if current process finishes or quantum expires
        if running_process and (time == running_process_start_time + quantum or running_process.remaining_time == 0):
            if running_process.remaining_time == 0:
                results.append(f"Time {time:3} : {running_process.name} finished")
                finished_processes += 1
                running_process.status = "Finished"
                running_process = None
            else:
                ready_queue.append(running_process)  # Re-queue the running process
                running_process = None

        # Select next process to run
        if not running_process and ready_queue:
            running_process = ready_queue.pop(0)
            running_process_start_time = time
            results.append(f"Time {time:3} : {running_process.name} selected (burst {running_process.remaining_time:3})")
            if running_process.remaining_time == running_process.burst_time:
                    running_process.start_time = time

        # Execute process
        if running_process:
            running_process.remaining_time -= 1
            if running_process.remaining_time == 0:
                for process in processes:
                    if process.arrival_time == time + 1:
                        ready_queue.append(process)
                        results.append(f"Time {time + 1:3} : {process.name} arrived")
                        arrival_before_finish = True
                results.append(f"Time {time + 1:3} : {running_process.name} finished")
                running_process.finish_time = time + 1
                finished_processes += 1
                running_process.status = "Finished"
                running_process = None
                
        if arrival_before_finish == False:
            time += 1  # Move to the next time unit

        # Check if simulation should idle
        if not running_process and not any(p.arrival_time == time for p in processes) and ready_queue == [] and time < runfor:
            results.append(f"Time {time:3} : Idle")

    results.append(f"Finished at time {time:3}\n")
    processes = rr_queue.copy()
    return processes, results
    

if __name__ == "__main__":
    main(sys.argv[1:])
