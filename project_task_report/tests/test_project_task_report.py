# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo.tests.common import TransactionCase


class TestProjectTaskReport(TransactionCase):

    def setUp(self):
        super().setUp()
        self.task_report_id = self.env["project.task.report"].create(
            {
                "start_date": datetime(2024, 2, 2),
                "end_date": datetime(2024, 6, 1),
                "project_ids": self.env.ref("project.project_project_1").ids,
            }
        )
        line_ids = self.task_report_id._create_line_ids()
        self.line_ids = line_ids.sorted(lambda l: l.task_id.name)

        self.stage_new = self.env.ref("project.project_stage_0")
        self.stage_in_progress = self.env.ref("project.project_stage_1")
        self.stage_canceled = self.env.ref("project.project_stage_3")

    def test_task_report_no_stage_change(self):
        task_line_id = self.line_ids[0]
        self.assertEqual(task_line_id.task_id.name, "Task 1")
        self.assertEqual(task_line_id.hours_spent, 1)
        self.assertEqual(task_line_id.start_stage_id, self.stage_new)
        self.assertEqual(task_line_id.end_stage_id, self.stage_new)

    def test_task_report_with_stage_change(self):
        task_line_id = self.line_ids[1]
        self.assertEqual(task_line_id.task_id.name, "Task 2")
        self.assertEqual(task_line_id.hours_spent, 12)
        self.assertEqual(task_line_id.start_stage_id, self.stage_in_progress)
        self.assertEqual(task_line_id.end_stage_id, self.stage_canceled)
