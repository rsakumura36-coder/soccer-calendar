from services.report_service import create_weekly_report
from services.line_service import send_line_message

report = create_weekly_report()

print(report)

send_line_message(report)