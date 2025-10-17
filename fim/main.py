# main.py
import yaml
import logging
import argparse
from pathlib import Path
from fim.utils import load_baseline, save_baseline, compute_hash
from fim.watcher import FileIntegrityMonitor

def load_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def setup_logger(log_file):
    logger = logging.getLogger("FIM")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--init-baseline", action="store_true", help="Initialize baseline")
    args = parser.parse_args()

    config = load_config(args.config)

    log_file = config.get("log_file", "fim.log")
    logger = setup_logger(log_file)

    # Initialize baseline
    baseline_file = config.get("baseline_file", "baseline.json")
    if args.init_baseline:
        store = {}  # Replace with your hash store logic
        save_baseline(store, baseline_file)
        print("[*] Baseline initialized successfully.")
        return

    # Load baseline
    store = load_baseline(baseline_file)

    print("[*] Starting File Integrity Monitor...")
    monitor = FileIntegrityMonitor(config, store, logger)
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
