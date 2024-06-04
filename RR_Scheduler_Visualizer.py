# Define constants

STATE_READY = "READY"
STATE_WAITING = "WAITING"
STATE_RUNNING = "RUNNING"
STATE_DONE = "DONE"

DO_COMPUTE = "COMPUTE"
DO_IO = "IO"

TIME_QUANTUM = 2
# Implement the process class

class Process:
    def __init__(self, pid, instructions):
        self.pid = pid
        self.instructions = instructions
        self.curr_state = STATE_READY
        self.pc = 0

    def next_instruction(self):
        if self.pc < len(self.instructions):
            return self.instructions[self.pc]
        return None

    def execute_instruction(self):
        if self.pc < len(self.instructions):
            self.pc += 1 # processing
            if self.pc == len(self.instructions):
                self.curr_state = STATE_DONE

# Implement the scheduler class

class Scheduler:
    def __init__(self, processes):
        self.processes = processes
        self.curr_process_idx = 0
        self.time_elapsed = 0

    def run(self):
        clock = 0
        while self.curr_process_idx < len(self.processes):
            clock += 1
            self.execute_current_process(clock)

    def execute_current_process(self, clock):
        process = self.processes[self.curr_process_idx]

        if self.time_elapsed >= TIME_QUANTUM: # checking for time quantum limit and current state
        
            self.curr_process_idx = (self.curr_process_idx + 1) % len(self.processes) # circular queue so moves to end of queue
            self.time_elapsed = 0 # exceeded time quantum so reset, start with new process
            process = self.processes[self.curr_process_idx]

        if process.curr_state != STATE_DONE: # non done state  
            instruction = process.next_instruction()
        
            if instruction == DO_COMPUTE:
                print(f"Time {clock}, process {process.pid} is computing")
                process.execute_instruction()
               
            elif instruction == DO_IO:
                print(f"Time {clock}, process {process.pid} is waiting for IO")
                process.execute_instruction()
                
            self.time_elapsed += 1

            if process.curr_state == STATE_DONE: # after execution of instruction, check for potential state change 
                print(f"Time {clock}, process {process.pid} is finished")

                self.processes.pop(self.curr_process_idx) 
                if self.curr_process_idx >= len(self.processes): # surpass length so circles around
                    self.curr_process_idx = 0
                
                self.time_elapsed = 0 # reset time quantum when processes finishes or time quantum expires
# Create processes from descriptions
        else: # done state
            self.curr_process_idx = (self.curr_process_idx + 1) % len(self.processes)
            self.time_elapese = 0

def create_processes(descriptions):
    processes = []
    for pid, desc in enumerate(descriptions):
        instructions = []
        instruction_count, cpu_operation = map(int, desc.split(":"))
        
        if cpu_operation == 100:
            instructions = [DO_COMPUTE] * instruction_count
        elif cpu_operation == 0:
            instructions = [DO_IO] * instruction_count

        processes.append(Process(pid, instructions))
    return processes

if __name__ == "__main__":
    descriptions = ["5:100", "3:0", "4:100"]
    processes = create_processes(descriptions)
    scheduler = Scheduler(processes)
    scheduler.run()

            
