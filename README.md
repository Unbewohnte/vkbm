# VKBM - VKontakte Birthday Message
### Send a scheduled message at any specified time

### Usage

Grab your token and an ID of either group chat or a chat with a person, then specify time and a message with an optional path to a local image as an attachment.

Example:

`python vkbm.py -t 'token' -m "message to send" -id 123456 --image Cat.png -dm 1 -dd 1 -dh 0 -dmt 0` - send "message to send" with an image of a cat to 123456 at (current year) January 1st, 00h:00m 

### Dependencies
- `vk_api`