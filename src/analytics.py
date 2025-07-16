import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

sla_log = []
incident_log = []

def log_incident(start_time, end_time, role_assigned, sla_threshold):
    duration = end_time - start_time
    met_sla = duration <= sla_threshold
    sla_log.append((role_assigned, met_sla))
    incident_log.append({
        "start": start_time,
        "end": end_time,
        "duration": duration,
        "role": role_assigned,
        "sla_met": met_sla
    })

def log_results(csv_path='results/baseline_run.csv', plot_path='results/sla_plot.png'):
    # Write CSV of incidents
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ["start", "end", "duration", "role", "sla_met"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in incident_log:
            writer.writerow(row)

    # Calculate SLA % by role
    sla_stats = defaultdict(lambda: {"met": 0, "total": 0})
    for role, met in sla_log:
        sla_stats[role]["total"] += 1
        if met:
            sla_stats[role]["met"] += 1

    roles = []
    percentages = []
    for role, stats in sla_stats.items():
        roles.append(role)
        percentages.append(round(100 * stats["met"] / stats["total"], 2))

    # Plot SLA % by role
    plt.figure(figsize=(6, 4))
    plt.bar(roles, percentages, color="steelblue")
    plt.ylim(0, 100)
    plt.ylabel("SLA Coverage (%)")
    plt.title("SLA Coverage by Role")
    plt.tight_layout()
    plt.savefig(plot_path)

    print(f"[{datetime.now()}] Results logged to {csv_path} and {plot_path}")
