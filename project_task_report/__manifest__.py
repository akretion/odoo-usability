# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Project Task Report",
    "summary": """Task wizard to sum up the progress between two dates""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion",
    "website": "http://akretion.com",
    "depends": ["project", "hr_timesheet"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/project_task_report.xml",
    ],
    "demo": ["data/project_task_report_demo.xml"],
}
