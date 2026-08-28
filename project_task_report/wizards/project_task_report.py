# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ProjectTaskReport(models.TransientModel):
    _name = "project.task.report"
    _description = "Task Report"

    start_date = fields.Date()
    end_date = fields.Date()
    project_ids = fields.Many2many("project.project", string="Projects")

    def _create_line_ids(self):
        line_vals = []
        task_ids = self.env["project.task"].search(
            [("project_id", "in", self.project_ids.ids)]
        )
        field_stage_id = self.env["ir.model.fields"].search(
            [("model", "=", "project.task"), ("name", "=", "stage_id")]
        )

        for task_id in task_ids:
            line_val = {"task_id": task_id.id, "timesheet_ids": []}

            # Catch the timesheets between the start and end dates
            for timesheet_id in task_id.timesheet_ids:
                if self.start_date < timesheet_id.date < self.end_date:
                    line_val["timesheet_ids"].append(timesheet_id.id)

            # Catch the historic stage changes between the start and end dates
            track_ids = task_id.message_ids.tracking_value_ids.filtered(
                lambda t: t.field == field_stage_id
                and self.start_date < t.mail_message_id.date.date() < self.end_date
            ).sorted(lambda t: t.mail_message_id.date)

            if track_ids:
                line_val.update(
                    {
                        "start_stage_id": track_ids[0].old_value_integer,
                        "end_stage_id": track_ids[-1].new_value_integer,
                    }
                )

            if line_val["timesheet_ids"] or line_val.get("start_stage_id"):
                # Fill stage fields in case there have been timesheets without stage change
                if not line_val.get("start_stage_id"):
                    line_val.update(
                        {
                            "start_stage_id": task_id.stage_id.id,
                            "end_stage_id": task_id.stage_id.id,
                        }
                    )
                line_vals.append(line_val)

        return self.env["project.task.report.line"].create(line_vals)

    def action_view_task_report(self):
        self.ensure_one()

        line_ids = self._create_line_ids()

        action_xml_id = "project_task_report.project_task_report_line_act_window"
        action = self.env["ir.actions.act_window"]._for_xml_id(action_xml_id)
        action.update({"domain": [("id", "in", line_ids.ids)]})
        return action


class ProjectTaskReportLine(models.TransientModel):
    _name = "project.task.report.line"
    _description = "Task Report Line"

    task_id = fields.Many2one("project.task", readonly=True)
    start_stage_id = fields.Many2one("project.task.type", readonly=True)
    end_stage_id = fields.Many2one("project.task.type", readonly=True)

    timesheet_ids = fields.Many2many("account.analytic.line", readonly=True)
    hours_spent = fields.Float(compute="_compute_hours_spent", store=True)

    @api.depends("timesheet_ids.unit_amount")
    def _compute_hours_spent(self):
        for rec in self:
            rec.hours_spent = sum(rec.timesheet_ids.mapped("unit_amount"))
