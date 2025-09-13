# BPO Challenge 2025  
My solution is based on a Genetic Algorithm for constructing initial admission schedules, combined with Simulated Annealing for local refinement. To improve accuracy, Process Mining calibration was integrated so that task durations in the simulation reflect statistics extracted from event logs.

This approach was designed to minimize the four KPIs defined in the project:
* Waiting time for admission (WTA)
* Waiting time in hospital (WTH)
* Nervousness (NERV)
* Personnel cost (COST)


### Genetic Algorithm (Initial Scheduling)
I used a Genetic Algorithm to create candidate admission schedules by mapping patients to time slots. It evolves schedules through selection, crossover, and mutation, with each candidate evaluated in the simulator against the four KPIs.

### Simulated Annealing (Local Refinement)
I applied Simulated Annealing to refine GA-generated admission plans by exploring local variations. It accepts better changes directly and occasionally worse ones to escape local optima.

### Process Mining Calibration
I calibrated task durations in the simulator using event log data. For each activity, mean and variance were extracted and used to replace default values with fitted distributions. This made the simulation more realistic and closer to actual hospital operations.

---

### OR Planner (Custom Scheduling Heuristic)
The OR planner that maximizes admission throughput while avoiding bottlenecks. It sets high capacities for operating rooms, intake staff, Emergency Room (ER) practitioners, and beds, then admits patients in six fixed waves starting at 08:00 each day.
Daily admission quotas are computed from intake, ER, and bed availability, with adjustments for backlog and early simulation warmup. Quotas are bounded between 48 to 72 patients/day and split across waves by fixed proportions. Patients are scheduled only once to keep nervousness low.

*This approach lowers admission waiting times by draining backlogs quickly, though it can increase in hospital waiting due to aggressive intake.*

---

### Simplified Reinforcement Learning Planner (Daily Operating Room Capacity Control)
My RL-based planner that adjusts next-day operating room (OR) capacity once per day at 18:00. The policy observes weekday, backlog level, and overtime, then selects an OR level between 2 and 5 using an ε-greedy rule. The reward function balances shorter admission and in-hospital waiting times with penalties for higher personnel cost. Scheduling rules require admissions ≥24h ahead, decisions ≥14h ahead, and near-term OR levels to only increase, capped at 5 ORs.

*This approach adapts OR capacity day by day, but outcomes were unstable and often led to higher personnel costs compared to heuristic planners.*


## Conclusion
I compared multiple approaches for hospital admission scheduling:
* GA → SA improved performance by refining admission plans.
*	GA → SA + Process Mining added realistic activity times and gave the most balanced results.
*	OR Planner used fixed daily quotas and admission waves to reduce admission waiting but often increased in hospital waiting.
*	RL Planner adjusted daily OR capacity, but outcomes were unstable and with high resource cost.

### **Therefore the combination of GA, SA, and process mining was the most effective.**
