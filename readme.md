RoundRobinPro implements a Round Robin CPU scheduling algorithm demonstrating its effectiveness on time-sharing systems, ensuring fairness and preventing any single process from monopolizing the CPU. The Round Robin (RR) scheduling algorithm is a preemptive scheduling approach that allocates CPU time to each process in equal-sized time slices, or quanta. Unlike FIFO, where processes might suffer from long waiting times if longer processes arrive first, RR ensures equitable CPU time distribution. In this project the Round Robin scheduling algorithm is implemented, managing the ready queue, executing processes, and handling context switches.

Key Features

    Fair Allocation: Ensures each process gets an equal share of the CPU.

    Preemption: If a process's burst time exceeds the time quantum, it is preempted and moved to the back of the ready queue.

    Context Switching: Handles context switching to ensure smooth execution of processes.

Setup Instructions
Prerequisites

    Python 3.x

Set Up Virtual Environment (Windows):

    py -3 -m venv env
    .\env\Scripts\activate

Set Up Virtual Environment (Mac/Linux):

    python3 -m venv env
    source env/bin/activate

Running the Scheduler

To run the scheduler, use the following command:

    python scheduler.py --quantum <time_quantum>

Replace <time_quantum> with the desired time quantum value.



Example outputs wth the following time quantum values: 1, 3, 5, 6, 7


![Alt text](<scheduler_screenshots/quanta1.png> "trial 1")

With the smallest time quantum, the CPU utilization is high, but the average waiting time and turnaround time are also high due to the frequent context switches.


![Alt text](<scheduler_screenshots/quanta3.png> "trial 2")

![Alt text](<scheduler_screenshots/quanta5.png> "trial 3")

With a time quantum of 5, the waiting and turnaround times remain stable, but the response time increases slightly.

![Alt text](<scheduler_screenshots/quanta6.png> "trial 4")

![Alt text](<scheduler_screenshots/quanta7.png> "trial 5")

With the largest time quantum, the CPU utilization is minimal leading to a FIFO implementation. The average waiting time and turnaround time improve, but the response time is higher compared to smaller quanta. 


The size of the time quantum has a significant impact on the performance of the Round Robin scheduling algorithm. The tradeoff is made between higher CPU utilization and turnaround time, as a short time quantum leads to more context switches with longer turnaround times but short response times while a longer time quantum results in longer response times but shorter turnaround times / wait times. The optimal time quantum balances these factors to ensure efficient CPU utilization and responsive system performance.