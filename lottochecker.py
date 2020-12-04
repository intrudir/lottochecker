import argparse, yaml, sys, os
from functions import *

# creds to send email with results
user = "some@gmail.com"
password = ""

parser = argparse.ArgumentParser(
description="This script is used to check for lotto numbers and see if you won."
)
parser.add_argument(
    '-c', '--check',
    action="store", default=None, dest='check',
    choices=("powerball", "megamillions", "lotto"),
    help="check winning numbers for specified game")

parser.add_argument(
    '--history',
    action="store_true", default=False, dest='history',
    help="check your numbers against historical data for a game")

args = parser.parse_args()

# if no args print help() and exit
if len(sys.argv) <= 1:
    parser.print_help()
    print()
    sys.exit(0)

# Get numbers from numbers.yaml
scriptDir = os.path.dirname(os.path.abspath(__file__))
try:
    with open(scriptDir + "/numbers.yaml") as s:
        myNumbers = yaml.load(s, Loader=yaml.FullLoader)
except FileNotFoundError:
    print("You need to add your picks to 'numbers.yaml'. A template has been \
created for you.")
    createNumbers(scriptDir)
    sys.exit(1)

if args.check and args.history:
    # get historical data
    historyWinners = getHistory(args.check)
    #print(historyWinners["05/19/15"])

    checkHistory(args.check, myNumbers, historyWinners)

elif args.check and not args.history:
    # Get winning numbers
    winners = getWinningNumbers(args.check)

    highest = 0
    msg, matched, highest = checkMyNums(args.check, myNumbers, winners, highest)
    print(msg)

    # send the results by email
    mailSubject = "{}: highest numbers matched: {}".format(args.check, highest)
    try:
        print()
        sendMail(user, password, mailSubject, msg)
    except smtplib.SMTPAuthenticationError:
        print("Invalid email credentials.")
