import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from services.report_service import create_weekly_report
from services.line_service import send_line_message


def run():

    print("🚀 Weekly notification start")

    message = create_weekly_report()

    print(message)

    send_line_message(message)

    print("✅ Weekly notification finished")


if __name__ == "__main__":
    run()