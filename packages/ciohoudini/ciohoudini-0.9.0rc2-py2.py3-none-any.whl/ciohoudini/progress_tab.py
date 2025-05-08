""" Progress bar """


from ciohoudini import payload
from ciohoudini.buttoned_scroll_panel import ButtonedScrollPanel

from ciohoudini.progress.md5_progress_widget import MD5ProgressWidget
from ciohoudini.progress.upload_progress_widget import UploadProgressWidget
from ciohoudini.progress.jobs_progress_widget import JobsProgressWidget

from ciohoudini.progress.file_status_panel import FileStatusPanel
from ciohoudini.progress.submission_worker import SubmissionWorker, SubmissionWorkerBase

import logging
from PySide2 import QtCore
from PySide2.QtCore import QThreadPool

from PySide2.QtCore import Qt
import threading
import time



logger = logging.getLogger(__name__)


class ProgressTab(ButtonedScrollPanel):
    """The progress tab.

    Shows the progress of the submissions with 4 elements:

    1. Jobs progress: Shows the progress of the entire batch of jobs.
    2. MD5 progress: Shows the progress of the MD5 generation for the current job.
    3. Upload progress: Shows the progress of the upload for the current job.
    4. File status: Shows detailed progress for each file.

    """

    def __init__(self, dialog):
        super(ProgressTab, self).__init__(
            dialog, buttons=[("cancel", "Cancel")]
        )
        self.dialog = dialog
        self.progress_list = []
        self.responses = []
        self.submissions = []
        self.worker = None
        self.worker_thread = None

        self.jobs_widget = JobsProgressWidget()
        self.md5_widget = MD5ProgressWidget()
        self.upload_widget = UploadProgressWidget()
        self.file_status_panel = FileStatusPanel()

        self.layout.addWidget(self.jobs_widget)
        self.layout.addWidget(self.md5_widget)
        self.layout.addWidget(self.upload_widget)
        self.layout.addWidget(self.file_status_panel)

        self.buttons["cancel"].clicked.connect(self.on_cancel_button)
        # self.buttons["cancel"].clicked.connect(self.dialog.on_close())

    def get_submission_payload(self, node):
        """Get the submission payload for the given node."""
        kwargs = {}
        kwargs["do_asset_scan"] = True
        kwargs["task_limit"] = -1
        submission_payload = payload.resolve_payload(node, **kwargs)
        return submission_payload

    def submit(self, node):
        """Submits the jobs.

        Send the submission generator to the worker.
        """

        self.jobs_widget.reset()
        self.md5_widget.reset()
        self.upload_widget.reset()
        self.file_status_panel.reset()

        self.responses = []


        self.submissions = self.get_submission_payload(node)


        if not self.submissions:
            logger.info("No submissions found")
            return

        job_count = len(self.submissions)

        #self.threadpool = QThreadPool()
        self.worker = SubmissionWorkerBase.create(self.submissions, job_count, )

        self.connect_worker_signals()

        self.worker_thread = threading.Thread(target=self.start_worker)
        self.worker_thread.start()

        #self.threadpool.start(self.worker)

    def start_worker(self):
        self.worker.run()
    def create_worker(self):
        job_count = len(self.submissions)
        self.worker = SubmissionWorker(self.submissions, job_count)

    def connect_worker_signals(self):
        self.worker.signals.on_start.connect(self.jobs_widget.reset, Qt.QueuedConnection)
        self.worker.signals.on_job_start.connect(self.md5_widget.reset, Qt.QueuedConnection)
        self.worker.signals.on_job_start.connect(self.upload_widget.reset, Qt.QueuedConnection)
        self.worker.signals.on_progress.connect(self.md5_widget.set_progress, Qt.QueuedConnection)
        self.worker.signals.on_progress.connect(self.upload_widget.set_progress, Qt.QueuedConnection)
        self.worker.signals.on_progress.connect(self.jobs_widget.set_progress, Qt.QueuedConnection)
        self.worker.signals.on_progress.connect(self.file_status_panel.set_progress, Qt.QueuedConnection)
        self.worker.signals.on_response.connect(self.handle_response, Qt.QueuedConnection)
        self.worker.signals.on_done.connect(self.handle_done, Qt.QueuedConnection)
        self.worker.signals.on_error.connect(self.handle_error, Qt.QueuedConnection)


    def handle_response(self, response):
        """Handle the job submitted response.

        We add in some extra information to help identify the job within the batch.
        """
        self.responses.append(response)

    def handle_error(self, error):
        """Make an error string from the exception and push it onto the responses."""
        self.responses.append(error)

    def on_cancel_button(self):
        if self.worker:
            self.worker.cancel()
        self.dialog.on_close()


    def handle_done(self):
        print("Jobs are completed...")

        # Enable response tab and disable validation and progress tabs
        self.dialog.show_response_tab()
        

        print("Showing the response ...")
        self.dialog.response_tab.hydrate(self.responses)
        print("Showing the response on the response tab is done...")

