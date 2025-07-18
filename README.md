# Data Center Staffing Optimization Simulator
In critical infrastructure environments like data centers, incident response performance directly impacts system reliability, uptime, and contract compliance. Staffing decisions — including how many engineers are on shift, what roles they fill, and how incidents are escalated — significantly influence SLA adherence and operational efficiency. But testing these decisions in live systems carries risk.

This simulator provides a safe and configurable environment to evaluate those tradeoffs. It uses discrete-event simulation to model real-world conditions: incoming incidents, SLA windows, shift schedules, and triage rules. By simulating thousands of incidents across different staffing strategies, teams can analyze the impact on key metrics before making operational changes.

**Key Use Cases**:
- Determine the minimum staffing needed to meet SLA targets
- Compare L1/L2/L3 staffing ratios under different incident loads
- Test how escalation rules affect resolution time and backlog
- Explore cost-saving strategies without compromising service reliability

## Overview
The simulator models a continuous stream of incidents, each defined by severity, SLA deadline, and required engineer tier. Incidents are routed to available engineers based on:
- Engineer headcount by level (L1-L3) and shift
- SLA thresholds by severity
- Routing and escalation logic
- Incident arrival patterns and volume distributions

At the end of each simulation run, the tool outputs:
- SLA compliance rates by severity level
- Average resolution time by incident type
- Engineer utilization rates
- Queue backlog at shift boundaries
- Visualizations of system performance over time

By simulating thousands of incidents under different staffing models, teams can assess the operational impact of proposed changes before implementation, helping avoid SLA breaches, reduce excess headcount, and improve reliability.

## Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/KatavinaNguyen/datacenter-simulator.git
   cd datacenter-simulator
   ```
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv\Scripts\activate  # venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Verify the install**
   ```bash
   python run_simulation.py
   ```
   This project uses Python 3.9+ and has no external database or cloud dependencies. All logs and metrics are generated locally.

## Configuration Guide
Before running a simulation, you can adjust the input parameters to match your environment and test goals. All configuration settings are stored in the `config/` directory using `.yaml` files.

**← KEY CONFIGURABLE PARAMETERS →**

Each config file defines how incidents are generated, how engineers are scheduled, and how routing decisions are made.

`engineers:`
Number of L1, L2, and L3 engineers per shift.
 ```yaml
 engineers:
   L1: [3, 3, 2]  # Number per shift (day, swing, night)
   L2: [2, 2, 2]
   L3: [1, 1, 1]
 ```

`shifts:`
Shift names, start times, and end times (24-hour format).
 ```yaml
 shifts:
   - name: Day
     start: 8
     end: 16
   - name: Swing
     start: 16
     end: 0
   - name: Night
     start: 0
     end: 8
 ```

`sla_by_severity:`
SLA time limits (in minutes) for each severity level.
 ```yaml
 sla_by_severity:
   low: 180
   medium: 60
   high: 30
 ```

`incident_volume:`
Total incidents to simulate and the distribution of their arrival.
 ```yaml
 incident_volume:
   total: 10000
   rate: poisson  # Options: poisson, uniform, or custom
 ```

`routing_rules:`
Triage and escalation paths by severity.
 ```yaml
 routing_rules:
   low: L1_only
   medium: L1_then_L2
   high: L2_then_L3
 ```

**← RUNNING WITH A CUSTOM CONFIG →**

To run a simulation with a specific config file:
 ```bash
 python run_simulation.py --config config/midshift_optimized.yaml
 ```

**← CREATING A NEW CONFIGS →**

To create your own scenario:
 ```bash
 cp config/default.yaml config/night_heavy.yaml
 ```
Edit the copied configuration file to change how many engineers are scheduled, when shifts begin and end, how incidents escalate between roles, and how much time each severity level has to meet its SLA. 

## Running Simulations
Once your environment is set up and a configuration file is ready, you can launch simulation runs directly from the command line.

**← BASIC RUN →**

To start a simulation using the default config:
 ```bash
 python run_simulation.py
 ```
This will run the simulation using `config/default.yaml` and output performance metrics to the console and plots to the `output/` directory.

**← RUNNING WITH A CUSTOM CONFIG →**

To simulate with your own configuration file:
 ```bash
 python run_simulation.py --config config/my_custom.yaml
 ```
You can create different config files to compare staffing strategies, escalation logic, shift overlaps, and SLA policies.

**← OUTPUT →**

Each simulation run generates:
- A summary of SLA compliance by severity level
- Average resolution time for each incident type
- Engineer utilization percentages (L1, L2, L3)
- Final backlog of unresolved incidents
- Visual plots of resolution trends and queue sizes over time

## Output and Metrics
After each simulation run, the simulator produces both quantitative metrics and visualizations to help comprehensively assess operational performance under the tested staffing configuration.

Key Metrics: 
- **SLA Compliance**: Percentage of incidents resolved within SLA time, broken down by severity level.
- **Average Resolution Time**: Mean time taken to resolve incidents, per severity and engineer level.
- **Engineer Utilization**: Percentage of time each engineer tier (L1, L2, L3) was actively working during their shift.
- **Incident Backlog**: Number of unresolved incidents left at each shift handoff.
- **Queue Dynamics**: Fluctuations in queue sizes and wait times over time.

Visualizations (generates performance plots in `output/`): 
- `sla_coverage.png`: SLA compliance by severity level
- `utilization.png`: Engineer utilization across the simulation
- `queue_timeline.png`: Queue size and incident accumulation over time
- `resolution_times.png`: Distribution of resolution durations by severity

## Scenario Examples
The simulator is designed to support a wide range of operational scenarios. By modifying the config file, you can explore how different staffing models, routing strategies, and incident volumes affect service performance.

| Scenario 1        | **Shift Rebalancing to Improve SLA**                                            |
|--------------------|------------------------------------------------------------------------------|
| **Goal**            | Shift more L2 engineers to evening and night hours to reduce SLA breaches   |
| **Changes**         | - Increase L2 count in `night` shift  <br> - Reduce L2 count in `day` shift <br> - Keep incident volume constant |
| **Expected Outcome**| Higher SLA compliance during late hours without increasing total headcount  |

| Scenario 2        | **Evaluating Impact of Understaffing**                                        |
|--------------------|------------------------------------------------------------------------------|
| **Goal**            | Analyze how reduced staffing affects SLA and backlog growth                 |
| **Changes**         | - Decrease total engineer count by 20% <br> - Maintain same incident volume and routing logic |
| **Expected Outcome**| Drop in SLA compliance and increase in unresolved incident backlog          |

| Scenario 3        | **Escalation Logic Optimization**                                             |
|--------------------|------------------------------------------------------------------------------|
| **Goal**            | Test whether faster escalation improves resolution time for high severity tickets |
| **Changes**         | - Reduce escalation timeout from 15 to 5 minutes <br> - Keep engineer counts and shift times constant |
| **Expected Outcome**| Faster resolution of high-severity incidents, with slight increase in L2/L3 utilization |

| Scenario 4        | **Skill Mix Adjustment**                                                      |
|--------------------|------------------------------------------------------------------------------|
| **Goal**            | Explore effects of replacing L3 engineers with cross-trained L2s            |
| **Changes**         | - Reduce L3 headcount <br> - Increase L2 headcount <br> - Enable L2s to handle more high-priority incidents |
| **Expected Outcome**| Similar SLA performance with lower cost, depending on training effectiveness |

| Scenario 5        | **Incident Volume Spike Stress Test**                                        |
|--------------------|------------------------------------------------------------------------------|
| **Goal**            | Simulate a 2x spike in incident volume to assess queue management and handoff impact |
| **Changes**         | - Double incident arrival rate <br> - Keep staffing and shifts fixed        |
| **Expected Outcome**| Longer queues, increased SLA breaches, and useful stress data to inform resource scaling strategies |

## Key Results
After testing variations in staffing levels, shift timing, and escalation logic, the simulator surfaced strategic tradeoffs between SLA performance, engineer workload, and incident backlog, offering a data-backed foundation for workforce decisions in high-volume data center environments.

- **SLA Optimization**: Rebalancing L2 engineers across shifts improved SLA compliance for critical incidents by up to **12%** without increasing total headcount.
- **Cost vs. Coverage Tradeoffs**: Simulating a 20% staff reduction revealed a **25% increase in backlog** and a **17% drop in SLA adherence**, highlighting the operational risks of aggressive cost cuts.
- **Escalation Tuning**: Reducing escalation timeout from 15 to 5 minutes decreased resolution time for high-priority incidents by **9%**, but increased L2/L3 load by **14%**.
- **Skill Distribution**: Swapping out L3s for cross-trained L2s maintained SLA performance within a **2% margin**, suggesting cost-effective staffing alternatives under the right triage logic.
- **Incident Surge Readiness**: Doubling incident volume without adjusting staffing caused SLA compliance to fall below **80%**, emphasizing the need for dynamic resourcing strategies during peak load events.

## Customizing Roles and Logic
After reviewing your first simulation with the default settings, you can start tailoring the simulator to reflect your specific operating conditions or test alternative strategies.

To customize a scenario:
1. Duplicate the config file
    ```bash
    cp configs/default.yaml configs/my_custom_run.yaml
    ```
2. Modify `my_custom_run.yaml`.
3. Adjust the parameters
    - `staffing`: Specify how many L1, L2, and L3 engineers are assigned per shift.
    - `shifts`: Modify shift start/end times and define overlaps (e.g., between day and evening).
    - `routing_rules`: Change escalation paths for each severity (e.g., `low: L1_only`, `high: L2_then_L3`).
    - `sla_deadlines`: Set new SLA thresholds (in minutes) by severity.
4. Save and run the simulation
   ```bash
    python simulate.py --config configs/my_custom_run.yaml
    ```
5. Review the outputs
    - Check the `results/` folder for updated metrics and visualizations.
    - Compare them to previous runs to evaluate tradeoffs.
    - Test how different staffing distributions affect SLA performance
    - Explore the impact of tighter SLAs or adjusted escalation logic
    - Simulate cost-cutting scenarios without reducing reliability

## Assumptions and Constraints
Modeled Assumptions:
- Incidents arrive as a Poisson process, meaning they are randomly distributed over time but follow a defined average arrival rate.
- Each incident has a fixed severity, SLA deadline, and skill requirement (L1, L2, or L3) upon creation.
- Engineers work in defined shifts and are only available during their scheduled hours.
- Routing logic is deterministic, based on severity and escalation rules (e.g., L1 → L2 if timeout).
- Engineers resolve one incident at a time, and once assigned, are occupied until resolution is complete.
- Resolution time is drawn from a distribution, optionally varying by severity or skill level.

Not Modeled (Constraints):
- No real-time multitasking or concurrent ticket handling by a single engineer.
- No consideration of soft skills, experience, or learning curves between engineers.
- No cost model for labor, missed SLAs, or overtime; output must be manually mapped to cost.
- No interdependencies between incidents (e.g., cascading failures or linked root causes).
- No external factors like tool outages, alert noise, or false positives.

## Future Improvements
This project began as a way to explore how simulation can support smarter, data-backed workforce planning in critical infrastructure environments. While the current version lays a solid foundation, there’s meaningful opportunity to increase both realism and usability in future iterations.

Some areas I’m actively considering expanding:

- **Cost Modeling**: Integrate labor rates and SLA penalties to tie operational decisions to financial outcomes. Each simulation run could log cumulative staffing costs and quantify the financial impact of SLA breaches for a more business-aligned view.
- **Smarter Escalation Logic**: Make routing decisions responsive to real-time conditions like queue length or engineer availability. Instead of static escalation paths, this would introduce dynamic decision-making based on simulated system pressure.
- **Skill Variance and Growth**: Account for differing experience levels among engineers and how that affects performance. Resolution times could vary by role seniority and improve over time to reflect training, learning curves, or tenure.
- **Concurrent Task Handling**: Allow more experienced engineers to juggle multiple lower-priority tasks at once. This would involve extending the simulation engine to model multitasking behavior and partial time allocations.
- **Web-Based Interface**: Build an interactive UI for configuring simulations, running tests, and viewing results visually. With my background in web development, I’d likely use something like React or Streamlit to make experimentation faster and more intuitive.

These improvements aim to make the simulator not just more powerful, but more usable for real-world planning and experimentation. I’m excited to continue building toward that.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
