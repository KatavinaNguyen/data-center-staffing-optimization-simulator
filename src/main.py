from simulator import run_simulation
import yaml
import sys

if __name__ == "__main__":
    config_path = sys.argv[1]
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    run_simulation(config)
