import argparse, yaml, sys
from functions import *

# creds to send email with results
user = "some@gmail.com"
password = ""

parser = argparse.ArgumentParser(
description="This script is used to check for lotto numbers and see if you won."
)
parser.add_argument(
    '-c', '--check',
    action="store", default=False, dest='check',
    choices=("powerball", "megamillions", "lotto"),
    help="check winning numbers for specified game")

args = parser.parse_args()

# if no args print help() and exit
if len(sys.argv) <= 1:
    parser.print_help()
    print()
    sys.exit(0)

# Get numbers from numbers.yaml
try:
    with open("numbers.yaml") as s:
        numbers = yaml.load(s, Loader=yaml.FullLoader)
except FileNotFoundError:
    print("You need to add your picks to 'numbers.yaml'. A template has been \
created for you.")
    createNumbers()
    sys.exit(1)

# Get winning numbers
highest = 0
winners = getWinningNumbers(args.check)
msg, matched, highest = checkMyNums(args.check, numbers, winners, highest)
print(msg)

# send the results by email
mailSubject = "{}: highest numbers matched: {}".format(args.check, highest)
try:
    sendMail(user, password, mailSubject, msg)
except smtplib.SMTPAuthenticationError:
    print("Invalid email credentials.")
