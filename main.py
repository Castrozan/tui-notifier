
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Label
from textual.containers import Container
import subprocess
import datetime
import time
import threading

class NotificationApp(App):
    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Container():
            yield Label("Enter notification time (e.g., '5m', '1h', '2025-12-25 10:00') and message:")
            yield Input(placeholder="Time", id="time_input")
            yield Input(placeholder="Message", id="message_input")
            yield Button("Schedule Notification", id="schedule_button", variant="primary")
            yield Label("Scheduled Notifications:", id="scheduled_label")
            yield Container(id="notifications_container")

    def action_quit(self) -> None:
        self.exit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "schedule_button":
            self.schedule_notification()

    def schedule_notification(self) -> None:
        time_str = self.query_one("#time_input").value
        message = self.query_one("#message_input").value

        if not time_str or not message:
            self.query_one("#scheduled_label").update("Scheduled Notifications: Please enter both time and message.")
            return

        try:
            # Parse time string
            delay_seconds = self.parse_time_string(time_str)
            if delay_seconds is None:
                self.query_one("#scheduled_label").update("Scheduled Notifications: Invalid time format.")
                return

            schedule_time = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)

            # Display scheduled notification
            notification_text = f"Notification scheduled for {schedule_time.strftime('%Y-%m-%d %H:%M:%S')}: {message}"
            self.query_one("#notifications_container").mount(Label(notification_text))

            # Schedule the notification in a separate thread
            threading.Thread(target=self._run_notification, args=(delay_seconds, message), daemon=True).start()

            self.query_one("#time_input").value = ""
            self.query_one("#message_input").value = ""
            self.query_one("#scheduled_label").update("Scheduled Notifications:")

        except Exception as e:
            self.query_one("#scheduled_label").update(f"Scheduled Notifications: Error - {e}")

    def parse_time_string(self, time_str: str) -> int | None:
        # Relative time parsing (e.g., 5m, 1h, 1d)
        if time_str.endswith('m'):
            return int(time_str[:-1]) * 60
        elif time_str.endswith('h'):
            return int(time_str[:-1]) * 3600
        elif time_str.endswith('d'):
            return int(time_str[:-1]) * 86400
        else:
            # Absolute time parsing (e.g., 2025-12-25 10:00)
            try:
                dt_object = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
                delay = (dt_object - datetime.datetime.now()).total_seconds()
                return int(delay) if delay > 0 else None
            except ValueError:
                return None

    def _run_notification(self, delay_seconds: int, message: str) -> None:
        time.sleep(delay_seconds)
        # Use notify-send for desktop notifications and disown the process        
        subprocess.Popen(['notify-send', 'TUI Notifier', message], preexec_fn=subprocess.os.setsid)

if __name__ == "__main__":
    app = NotificationApp()
    app.run()


