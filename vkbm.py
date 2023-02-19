'''
The MIT License (MIT)
Copyright © 2023 Kasyanov Nikolay Alexeyevich (Unbewohnte)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import vk_api
from vk_api import VkUpload
from datetime import datetime
from time import sleep, time
from argparse import ArgumentParser


def main(token: str, date: str, id: int, is_group_chat: bool, message: str, image: str):
    year, month, day, hour, minute = date.split("_")
    year = int(year)
    month = int(month)
    day = int(day)
    hour = int(hour)
    minute = int(minute)

    try:
        vk = vk_api.VkApi(token=token)
        api = vk.get_api()

        uploaded_img = None
        if len(image) != 0:
            upload = VkUpload(api)
            uploaded_img = upload.photo_messages(photos=image)[0]

        while True:
            sleep(1)
            now = datetime.now()
            print(
                f"[{now.date()}] {datetime(year, month, day, hour, minute)-now} until message"
            )

            if int(now.year) == year and int(now.month) == month and int(now.day) == day and int(now.hour) == hour and int(now.minute) == minute:
                if is_group_chat:
                    if uploaded_img != None:
                        api.messages.send(
                            chat_id=id, message=message, attachment=f"photo{uploaded_img['owner_id']}_{uploaded_img['id']}", random_id=0)
                    else:
                        api.messages.send(
                            chat_id=id, message=message, random_id=0)
                else:
                    if uploaded_img != None:
                        api.messages.send(
                            user_id=id, message=message, attachment=f"photo{uploaded_img['owner_id']}_{uploaded_img['id']}", random_id=0)
                    else:
                        api.messages.send(
                            user_id=id, message=message, random_id=0)

                print("Message has been sent")
                break
    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == '__main__':
    now = datetime.now()

    parser = ArgumentParser(
        prog="vkbm",
        description="Send scheduled usual|birthday message with an image to a vk chat",
    )

    parser.add_argument("--token", "-t", required=True,
                        type=str, help="Your VK app token")
    parser.add_argument("--date-year", "-dy", required=False,
                        type=int, default=now.year, help="Year to send message at")
    parser.add_argument("--date-month", "-dm", required=False,
                        type=int, default=now.month, help="Month number to send message at")
    parser.add_argument("--date-day", "-dd", required=False,
                        type=int, default=now.day, help="Day number to send message at")
    parser.add_argument("--date-hour", "-dh", required=False,
                        type=int, default=now.hour, help="An hour of a day to send message at")
    parser.add_argument("--date-minute", "-dmt", required=False,
                        type=int, default=now.minute, help="A minute of an hour to send message at")
    parser.add_argument("--id", "-id",
                        required=True, type=str, help="Chat ID")
    parser.add_argument("--is_group_chat", "-igc",
                        required=False, type=bool, default=False, help="Is ID pointing to group chat or a person")
    parser.add_argument("--message", "-m", required=True,
                        type=str, help="Message to be sent")
    parser.add_argument("--image", "-i", required=False,
                        type=str, default="", help="Path to the image to send")
    args = parser.parse_args()

    year = args.date_year
    month = args.date_month
    day = args.date_day
    hour = args.date_hour
    minute = args.date_minute

    if datetime(year, month, day, hour, minute) < datetime.now():
        print("Can't send into the past !")
        exit(1)

    date = f"{year}_{month}_{day}_{hour}_{minute}"
    main(args.token, date, int(args.id),
         args.is_group_chat, args.message, args.image)
    pass
