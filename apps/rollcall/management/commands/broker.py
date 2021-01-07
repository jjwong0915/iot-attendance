import linebot
import linebot.models
import os
import time
from django.core.management import base
from ... import models
from . import _mcs as mcs


class Command(base.BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = mcs.Device(
            device_id=os.getenv("MCS_DEVICE_ID"),
            device_key=os.getenv("MCS_DEVICE_KEY"),
        )
        self.line_api = linebot.LineBotApi(os.getenv("LINE_ACCESS_TOKEN"))

    def update_student(self):
        dev1_student = set(
            self.device.retrieve_values("dev1_student")["value"].split()
        )
        dev2_student = set(
            self.device.retrieve_values("dev2_student")["value"].split()
        )
        merged_student = dev1_student | dev2_student
        #
        for student_id in merged_student:
            _, created = models.Attendance.objects.get_or_create(
                student_id=student_id,
                confirmed=False,
            )
            if created:
                self.line_api.broadcast(
                    linebot.models.TextSendMessage(
                        f"[{student_id}] arrived classroom"
                    )
                )

    def handle(self, *args, **kwargs):
        print("message broker has started...")
        while True:
            try:
                self.update_student()
                time.sleep(1)
            except KeyboardInterrupt:
                break
