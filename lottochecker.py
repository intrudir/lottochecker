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
    choices=("powerball", "megamillions", "lotto", "lotto DP"),
    help="check winning numbers for specified game")

parser.add_argument(
    '-H', '--history',
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
        my_numbers = yaml.load(s, Loader=yaml.FullLoader)
except FileNotFoundError:
    print("You need to add your picks to 'numbers.yaml'. A template has been \
created for you.")
    createNumbers(scriptDir)
    sys.exit(1)


if args.check == "lotto":
    if args.history:
        Lotto = Game("lotto", None)
        Lotto.check_historical_data(my_numbers)
    else:
        Lotto = Game("lotto", "regular")
        winners, jackpot_info, win_table = Lotto.get_win_data()
        msg_body, highest = Lotto.check_win(my_numbers, winners)
        msg = Lotto.prep_msg(winners, jackpot_info, msg_body)
        print(msg)

elif args.check == "lotto DP":
    if args.history:
        Lotto = Game("lotto", None)
        Lotto.check_historical_data(my_numbers)
    else:
        Lotto_DP = Game("lotto", "double play")
        winners, jackpot_info, win_table = Lotto_DP.get_win_data()
        msg_body, highest = Lotto_DP.check_win(my_numbers, winners)
        msg = Lotto_DP.prep_msg(winners, jackpot_info, msg_body)
        print(msg)

elif args.check == "powerball":
    if args.history:
        Powerball = Game("powerball", None)
        Powerball.check_historical_data(my_numbers)
    else:
        Powerball = Game("powerball", "regular")
        winners, jackpot_info, win_table = Powerball.get_win_data()
        msg_body, highest = Powerball.check_win(my_numbers, winners)
        msg = Powerball.prep_msg(winners, jackpot_info, msg_body)
        print(msg)

elif args.check == "megamillions":
    if args.history:
        Megamillions = Game("megamillions", None)
        Megamillions.check_historical_data(my_numbers)
    else:  # Needs to be spelled like megaMillions
        Megamillions = Game("megaMillions", "regular")
        winners, jackpot_info, win_table = Megamillions.get_win_data()
        msg_body, highest = Megamillions.check_win(my_numbers, winners)
        msg = Megamillions.prep_msg(winners, jackpot_info, msg_body)
        print(msg)

# Send email with results
mailSubject = "{}: highest numbers matched: {}".format(args.check, highest)
try:
    send_mail(user, password, mailSubject, msg)
except smtplib.SMTPAuthenticationError:
    print("Invalid email credentials.")

sys.exit(0)
