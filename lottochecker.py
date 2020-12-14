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
    '-s', '--single',
    action="store", default=None, dest='single',
    help="Check numbers you specify")

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

if args.single:
    nums = args.single.split(',')
    if len(nums) != 6:
        print("You need to specify 6 numbers. \
If checking MM or PB, that ball should be #6.")
        sys.exit(1)
    else:
        # need to turn nums into ints
        try:
            to_int = map(int, nums)
            my_numbers = {"single": {args.check: list(to_int)}}
        except ValueError:
            print("Something wrong with one of your specified numbers.")
            sys.exit(1)

if args.check == "lotto":
    Lotto = Game("lotto", "regular")
    if args.history:
        Lotto.check_historical_data(my_numbers)
    else:
        winners, jackpot_info, win_table = Lotto.get_win_data()
        msg_body, highest, highest_PB = Lotto.check_win(my_numbers, winners)
        msg = Lotto.prep_msg(winners, jackpot_info, msg_body)
        print(msg)

elif args.check == "lotto DP":
    Lotto_DP = Game("lotto", "double play")
    if args.history:
        Lotto.check_historical_data(my_numbers)
    else:
        winners, jackpot_info, win_table = Lotto_DP.get_win_data()
        msg_body, highest, highest_PB = Lotto_DP.check_win(my_numbers, winners)
        msg = Lotto_DP.prep_msg(winners, jackpot_info, msg_body)
        print(msg)

elif args.check == "powerball":
    Powerball = Game("powerball", "regular")
    if args.history:
        Powerball.check_historical_data(my_numbers)
    else:
        winners, jackpot_info, win_table = Powerball.get_win_data()
        msg_body, highest, highest_PB = Powerball.check_win(my_numbers, winners)
        msg = Powerball.prep_msg(winners, jackpot_info, msg_body)
        print(msg)

elif args.check == "megamillions":
    Megamillions = Game("megaMillions", "regular")
    if args.history:
        Megamillions.check_historical_data(my_numbers)
    else:  # Needs to be spelled like megaMillions
        winners, jackpot_info, win_table = Megamillions.get_win_data()
        msg_body, highest, highest_PB = Megamillions.check_win(my_numbers, winners)
        msg = Megamillions.prep_msg(winners, jackpot_info, msg_body)
        print(msg)

# Send email with results
if highest_PB:
    if highest == 5:
        mailSubject = "{}: YOU WON!!! CHECK NOW".format(args.check)
    elif highest < 5:
        mailSubject = "{}: highest numbers matched: {} and PB Match!".format(args.check, highest)
elif highest == 6:
    mailSubject = "{}: YOU WON!!! CHECK NOW".format(args.check)
else:
    mailSubject = "{}: highest numbers matched: {}".format(args.check, highest)

if args.single:
    print(mailSubject)
else:
    try:
        send_mail(user, password, mailSubject, msg)
        print(mailSubject)
    except smtplib.SMTPAuthenticationError:
        print("Invalid email credentials.")

sys.exit(0)
