import csv

PROCESSES = []
TIME_QUANTUM = 2
CONTEXT_SWITCH_TIME = TIME_QUANTUM * 0.1

with open('csv.txt') as file_handle_csv:
    file_content = csv.reader(file_handle_csv)

    for idx, process in enumerate(file_content):
        if idx == 0:
            continue
        pid, arrive, burst = process
        PROCESSES.append((int(pid), int(arrive), int(burst)))

class Process:
    def __init__(self, pid, arrive, burst, wait=0, cpu=0, turnaround=0, completion=0, context=0, response=0):
        self.pid = pid
        self.arrive = arrive
        self.burst = burst
        self.wait = wait
        self.cpu = cpu
        self.completion = completion
        self.turnaround = turnaround
        self.context = context
        self.response = response
        
            
    def __str__(self):
        return (f"PID: {self.pid}, Arrive: {self.arrive}, Burst: {self.burst}, "
               f"Wait: {self.wait}, CPU: {self.cpu}, Turnaround: {self.turnaround}, "
               f"Completion: {self.completion}, Context: {self.context}, Response: {self.response}")
            
        
        
class Scheduler:
    WAITING_QUEUE = []
    READY_QUEUE = []
    DONE_QUEUE = []
  
    def __init__(self, processes=PROCESSES, time_quantum=TIME_QUANTUM):
        self.processes = processes
        self.time_quantum = time_quantum
    
    def load_waiting_queue(self):
        for process in self.processes:
            pid, arrive, burst = process
            Scheduler.WAITING_QUEUE.append(Process(pid, arrive, burst))
            
    def sort_queue(self):
         Scheduler.WAITING_QUEUE.sort(key=lambda process: process.arrive) # sort by arrival time
            
                
    def run_scheduler(self):
        clock = 0
        
        
        Scheduler.READY_QUEUE = [process for process in Scheduler.WAITING_QUEUE if process.arrive == clock]
        Scheduler.WAITING_QUEUE = [process for process in Scheduler.WAITING_QUEUE if process.arrive != clock]
                                    
        
        COMBINED_PROCESS_LIST = Scheduler.READY_QUEUE + Scheduler.WAITING_QUEUE
        

        original_burst_counts = []
        while len(COMBINED_PROCESS_LIST) > 0:
      
            curr_process = COMBINED_PROCESS_LIST.pop(0)
            burst_count = curr_process.burst
            original_burst_counts.append(burst_count)
            
            while burst_count > 0:  
        
                if curr_process.response == 0:
                    curr_process.response = clock - curr_process.arrive # set response time upon arrival
                    
                burst_count -= 1 ## Processing
                curr_process.cpu += 1 ### record CPU TIME
                clock += 1
                
                # finished process
                if burst_count == 0:
                    curr_process.completion = clock ### record completion time when burst exhausted
                    Scheduler.DONE_QUEUE.append(curr_process)
                    break

                # premempted process
                elif clock >= TIME_QUANTUM and clock % TIME_QUANTUM == 0:
                    curr_process.context += 1 # record switching process
                    curr_process.burst = burst_count
                    COMBINED_PROCESS_LIST.append(curr_process)
                    break
        # update with original burst counts
        for idx, process in enumerate(Scheduler.DONE_QUEUE):
            process.burst = original_burst_counts[idx] 
              
            
        print(Scheduler.DONE_QUEUE)   
        for process in Scheduler.DONE_QUEUE:
            print(process)
            

if __name__ == "__main__":         
                
    RR_Scheduler = Scheduler()
    RR_Scheduler.load_waiting_queue()
    RR_Scheduler.sort_queue()

    for process in RR_Scheduler.WAITING_QUEUE:
        print(process)
        
        
    print("Running Scheduler...")
    RR_Scheduler.run_scheduler()

    print("Calculating Stats per job")

    # set turnaround times
    for process in Scheduler.DONE_QUEUE:
        process.turnaround = process.completion - process.arrive

    # set wait time
    for process in Scheduler.DONE_QUEUE:
        process.wait = process.turnaround - process.cpu

    # Summary Stats
    context_switches = sum([process.context for process in Scheduler.DONE_QUEUE])
    CPU_UTILIZATION = context_switches * CONTEXT_SWITCH_TIME

    total_time = sum([process.burst for process in Scheduler.DONE_QUEUE]) # 20
    THROUGHPUT = len(Scheduler.DONE_QUEUE) / total_time

    AVERAGE_WAITING_TIME = sum([process.turnaround for process in Scheduler.DONE_QUEUE]) / len(Scheduler.DONE_QUEUE)

    AVERAGE_TURNAROUND_TIME = sum([process.turnaround for process in Scheduler.DONE_QUEUE]) / len(Scheduler.DONE_QUEUE)

    print(f"Round Robin CPU Scheduler with Time Quantum: {TIME_QUANTUM}: Process Stats")
    for process in Scheduler.DONE_QUEUE:
        print(f"Process: {process.pid}, Arrival Time: {process.arrive}, Burst Time: {process.burst}")
        print(f"Completion Time: {process.completion}, Turnaround Time: {process.turnaround}, Waiting Time: {process.wait}, Response Time: {process.response}")


    print(f"Round Robin CPU Scheduler with Time Quantum: {TIME_QUANTUM}: Summary Stats")
    print(f"CPU Utilization: {CPU_UTILIZATION}")
    print(f"Throughput: {THROUGHPUT}")
    print(f"Average Waiting Time: {AVERAGE_WAITING_TIME}")
    print(f"Average Turnaround Time: {AVERAGE_TURNAROUND_TIME}")

