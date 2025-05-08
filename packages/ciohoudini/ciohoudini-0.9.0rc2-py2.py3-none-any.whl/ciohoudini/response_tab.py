from ciohoudini.components.notice_grp import NoticeGrp
from ciohoudini.components.buttoned_scroll_panel import ButtonedScrollPanel
from ciocore import config
import urllib.parse

CONFIG = config.get()


class ResponseTab(ButtonedScrollPanel):
    def __init__(self, dialog):
        super(ResponseTab, self).__init__(dialog, buttons=[("close", "Close")])
        self.dialog = dialog
        self.configure_signals()

    def configure_signals(self):
        """Connect signals to slots."""
        self.buttons["close"].clicked.connect(self.dialog.on_close)

    def hydrate(self, responses):
        """Hydrate the tab with the responses.

        Currently there are 2 possible response statuses:

        Success = {
            "body": "job submitted.",
            "jobid": "00636",
            "status": "success",
            "uri": "/jobs/00636",
            "job_title": "My Houdini Job",
            "response_code": 201,
        }
        Errored = {
            "body": "job submission failed.",
            "exception": "Some exception",
            "traceback": "Some traceback",
            "exception_type": "SomeException",
            "job_title": "The job title",
            "status": "error",
            "response_code": 500,
        }
        """
        print("Showing responses...")
        self.clear()
        for res in responses:
            severity = self._get_severity(res)
            message = self._get_message(res)
            url = self._get_url(res)
            details = self._get_details(res)

            widget = NoticeGrp(message, severity=severity, url=url, details=details)
            self.layout.addWidget(widget)
        self.layout.addStretch()
        # print("Showing responses is complete.")

    @staticmethod
    def _get_severity(response):
        status = response["status"]
        if response["status"] == "error" and response["exception_type"] == "UserCanceledError":
            status = "warning"
        return status

    @staticmethod
    def _get_message(response):
        message = response["body"].capitalize().strip(".")
        if "exception_type" in response:
            message += " - {}".format(response["exception_type"])
        if "job_title" in response:
            message += " - {}".format(response["job_title"])
        jobid = "jobid" in response and response["jobid"]
        if jobid:
            message += " ({})".format(jobid)
        return message

    @staticmethod
    def _get_url(response):
        widget_url = None
        if response["status"] == "success" and response["uri"]:
            label = "Go to dashboard"
            url = urllib.parse.urljoin(
                CONFIG["url"], response["uri"].replace("jobs", "job")
            )
            widget_url = (label, url)
        return widget_url

    @staticmethod
    def _get_details(response):
        if not response["status"] == "error":
            return
        if not ("exception_type" in response and "traceback" in response and "exception" in response):
            return
        ex_type = response["exception_type"]
        ex_msg = response["exception"]
        ex_trace = response["traceback"]
        return f"{ex_type}: {ex_msg}\nTraceback:\n{ex_trace}"

    def on_close_button(self):
        """When someone clicks on Close"""

        self.dialog.on_close()
