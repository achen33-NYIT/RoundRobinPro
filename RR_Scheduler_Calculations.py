import csv
from optparse import OptionParser

PROCESSES = []

with open('csv.txt') as file_handle_csv:
    file_content = csv.reader(file_handle_csv)

    for idx, process in enumerate(file_content):
        if idx == 0:
            continue
        pid, arrive, burst = process
        PROCESSES.append((int(pid), int(arrive), int(burst)))

class Process:
    def __init__(self, pid, arrive, burst):
        self.pid = pid
        self.arrive = arrive
        self.burst = burst
        self.remaining_burst = burst
        self.cpu = 0
        self.context = 0
        self.response = -1
        self.completion = 0
        self.wait = 0
        self.turnaround = 0
        
    def __str__(self):
        return (f"PID: {self.pid}, Arrive: {self.arrive}, Burst: {self.burst}, "
               f"Wait: {self.wait}, CPU: {self.cpu}, Turnaround: {self.turnaround}, "
               f"Completion: {self.completion}, Context: {self.context}, Response: {self.response}")   
        
class Scheduler:

    def __init__(self, processes=PROCESSES, quantum=1):
        self.processes = [Process(*p) for p in processes]
        self.quantum = quantum
        self.waiting_queue = sorted(self.processes, key=lambda process: process.arrive)
        self.ready_queue = []
        self.done_queue = []
        self.clock = 0
                
    def run(self):
        
        while self.ready_queue or self.waiting_queue:
            while self.waiting_queue and self.waiting_queue[0].arrive <= self.clock:
                self.ready_queue.append(self.waiting_queue.pop(0))
                  
            if self.ready_queue:
                curr_process = self.ready_queue.pop(0)
            
                if curr_process.response == -1:
                    curr_process.response = self.clock - curr_process.arrive

                runtime = min(curr_process.remaining_burst, self.quantum)
                curr_process.remaining_burst -= runtime
                self.clock += runtime

                if curr_process.remaining_burst > 0:
                    self.ready_queue.append(curr_process) # goes to the back of ready queue upon preemption
                    curr_process.context += 1
                else:
                    curr_process.completion = self.clock
                    curr_process.turnaround = curr_process.completion - curr_process.arrive
                    curr_process.wait = curr_process.turnaround - curr_process.burst
                    self.done_queue.append(curr_process)
            else:
                self.clock += 1
          
    def print_stats(self):
        print('Here is the job list, with the run time of each job: ')
        print('\n Execution trace:')

        # print turnaround time, wait time, and response time per job
        for process in self.done_queue:
            print(f"Process {process.pid}: Turnaround Time: {process.turnaround}, Wait Time: {process.wait}, Response Time: {process.response}")
     
        # Summary Stats
        CONTEXT_SWITCH_TIME = self.quantum * 0.1
        context_switches = sum([process.context for process in self.done_queue])
        CPU_UTILIZATION = context_switches * CONTEXT_SWITCH_TIME

        JOBS_LENGTH = len(self.done_queue)
        total_time = sum([process.burst for process in self.done_queue]) # 20
        THROUGHPUT =  JOBS_LENGTH / total_time

        AVERAGE_WAITING_TIME = sum([process.wait for process in self.done_queue]) / JOBS_LENGTH

        AVERAGE_TURNAROUND_TIME = sum([process.turnaround for process in self.done_queue]) / JOBS_LENGTH
    
        AVERAGE_RESPONSE_TIME = sum([process.response for process in self.done_queue]) / JOBS_LENGTH

          

        print(f"Round Robin CPU Scheduler with Time Quantum: {self.quantum} Summary Stats")
        print(f"CPU Utilization: {CPU_UTILIZATION:.2f}")
        print(f"Throughput: {THROUGHPUT:.2f}")
        print(f"Average Waiting Time: {AVERAGE_WAITING_TIME:.2f}")
        print(f"Average Turnaround Time: {AVERAGE_TURNAROUND_TIME:.2f}")
        print(f"Average Response Time: {AVERAGE_RESPONSE_TIME:.2f}")


            

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-q", "--quantum", help="length of time slice", default=1, action="store", type="int", dest="quantum")      

    options, args = parser.parse_args()  
                
    RR_Scheduler = Scheduler(quantum=options.quantum)
        
    print("Running Scheduler...")
    RR_Scheduler.run()
    RR_Scheduler.print_stats()

