import os
from dotenv import load_dotenv

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage
)


load_dotenv()


CHANNEL_ACCESS_TOKEN = os.getenv(
    "LINE_CHANNEL_ACCESS_TOKEN"
)

USER_ID = os.getenv(
    "LINE_USER_ID"
)


configuration = Configuration(
    access_token=CHANNEL_ACCESS_TOKEN
)


def send_line_message(message):

    with ApiClient(configuration) as api_client:

        line_bot_api = MessagingApi(api_client)

        line_bot_api.push_message(
            PushMessageRequest(
                to=USER_ID,
                messages=[
                    TextMessage(
                        text=message
                    )
                ]
            )
        )

    print("✅ LINE送信成功")