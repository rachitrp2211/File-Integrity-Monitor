# watcher.py
import os
import time
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .alerter import send_email
from .utils import compute_hash, load_baseline, save_baseline
import logging

class FIMHandler(FileSystemEventHandler):
    def __init__(self, config, store, logger):
        self.config = config
        self.store = store  # baseline dictionary
        self.logger = logger
        self.email_cfg = config.get("email", {})
        self.daily_events = []

    def on_created(self, event):
        if not event.is_directory:
            self._process("created", event.src_path)
            self._update_baseline(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self._process("modified", event.src_path)
            self._update_baseline(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self._process("deleted", event.src_path)
            self._remove_from_baseline(event.src_path)

    def _process(self, event_type, path):
        """Process file events and send alerts if needed."""
        try:
            log_msg = f"{event_type.upper()}: {path}"
            self.logger.info(log_msg)
            self.daily_events.append(log_msg)

            # Dynamic email subject
            subject = f"FIM Alert: {event_type.upper()}"
            body = f"<html><body><h2>{subject}</h2><p>File: {path}</p></body></html>"
            attachments = [self.config.get("log_file", "fim.log")]

            # Send email for all events (optional: remove if you only want deletions)
            send_email(self.email_cfg, subject, body, attachments=attachments, html=True)

        except Exception as e:
            self.logger.error(f"Error processing file {path}: {e}")

    def _update_baseline(self, path):
        """Add or update file hash in baseline."""
        try:
            file_hash = compute_hash(path, self.config.get("hash_algorithm", "sha256"))
            self.store[path] = file_hash
            save_baseline(self.store, self.config.get("baseline_file", "baseline.json"))
            self.logger.info(f"Baseline updated for {path}")
        except Exception as e:
            self.logger.error(f"Failed to update baseline for {path}: {e}")

    def _remove_from_baseline(self, path):
        """Remove deleted file from baseline."""
        try:
            if path in self.store:
                del self.store[path]
                save_baseline(self.store, self.config.get("baseline_file", "baseline.json"))
                self.logger.info(f"Removed {path} from baseline")
        except Exception as e:
            self.logger.error(f"Failed to remove {path} from baseline: {e}")

    def send_daily_digest(self):
        """Send a daily digest email with all events."""
        if not self.daily_events:
            return
        html_content = "<html><body>"
        html_content += f"<h2>FIM Daily Digest - {time.strftime('%Y-%m-%d')}</h2><ul>"
        for event in self.daily_events:
            html_content += f"<li>{event}</li>"
        html_content += "</ul></body></html>"

        attachments = [self.config.get("log_file", "fim.log")]

        try:
            send_email(self.email_cfg, f"FIM Daily Digest - {time.strftime('%Y-%m-%d')}", html_content, attachments=attachments, html=True)
            self.logger.info("Daily digest email sent successfully.")
            self.daily_events.clear()
        except Exception as e:
            self.logger.error(f"Failed to send daily digest: {e}")

# Main FIM class
class FileIntegrityMonitor:
    def __init__(self, config, store, logger):
        self.config = config
        self.store = store
        self.logger = logger
        self.handler = FIMHandler(config, store, logger)
        self.observer = Observer()

    def start_monitoring(self):
        paths = self.config.get("paths", [])
        for folder in paths:
            if os.path.exists(folder):
                self.observer.schedule(self.handler, folder, recursive=True)
                self.logger.info(f"Monitoring started on {folder}")
            else:
                self.logger.warning(f"Path not found: {folder}")

        self.observer.start()
        self.handler.start_daily_digest_timer(hour=18, minute=0)  # Example: 6 PM daily

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

# Daily digest timer functions
def start_daily_digest_timer(self, hour=18, minute=0):
    from datetime import datetime, timedelta
    now = datetime.now()
    next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if next_run < now:
        next_run += timedelta(days=1)
    delay = (next_run - now).total_seconds()
    threading.Timer(delay, self._daily_digest_job).start()

def _daily_digest_job(self):
    self.send_daily_digest()
    threading.Timer(24*3600, self._daily_digest_job).start()

# Bind timer functions to FIMHandler
FIMHandler.start_daily_digest_timer = start_daily_digest_timer
FIMHandler._daily_digest_job = _daily_digest_job
