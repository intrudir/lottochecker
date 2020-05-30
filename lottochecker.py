import argparse
from functions import *
from datetime import date

parser = argparse.ArgumentParser(
description="This script is used to check for lotto numbers and see if you won."
)
parser.add_argument('--powerball', action="store_true", default=False, dest='powerball',
	help="check Powerball numbers")
parser.add_argument('--megamillions', action="store_true", default=False, dest='megamillions',
	help="check Megamillions numbers")
parser.add_argument('--cash4life', action="store_true", default=False, dest='cash4life',
	help="check Cash 4 Life numbers")
parser.add_argument('--lotto', action="store_true", default=False, dest='lotto',
	help="check Lotto numbers")

args = parser.parse_args()

today = date.today()
ballName = ['Powerball', 'Megaball', 'Cashball', 'Lotto']
url = [
    "http://floridalottery.com/site/powerball",
    "http://floridalottery.com/site/megaMillions",
    "http://floridalottery.com/cash4Life",
    "http://floridalottery.com/site/lotto"
]
bigBallPath = [
    '//span[@class="balls pbBall"]/text()',
    '//span[@class="balls mMillBall"]/text()',
    '//span[@class="balls c4lCBBall"]/text()'
]
myPicks = {
    'powerball': {'balls': ['6', '8', '10', '28', '49'], 'bigBall': '7'},
    'megaMills': {'balls': ['6', '8', '10', '28', '49'], 'bigBall': '7'},
    'megaMills2': {'balls': ['7', '12', '21', '36', '51'], 'bigBall': '20'},
    'cash4Life': {'balls': ['6', '8', '10', '28', '49'], 'bigBall': '4'},
    'lotto': {'balls': ['6', '8', '10', '14', '28', '49']},
    'Mom\'s powerball': {'balls': ['10', '17', '25', '26', '40'], 'bigBall': '7'},
    'Mom\'s powerball2': {'balls': ['3', '17', '21', '58', '63'], 'bigBall': '5'},
    'Mom\'s powerball3': {'balls': ['7', '12', '21', '36', '51'], 'bigBall': '20'},
    'Mom\'s megaMills': {'balls': ['3', '17', '21', '58', '63'], 'bigBall': '5'},
    'Mom\'s lotto': {'balls': ['10', '13', '25', '26', '30', '40']},
    'Mom\'s lotto2': {'balls': ['7', '31', '37', '40', '42', '50']}
}

if args.powerball:
    mailSubject = "Powerball"
    balls, bigBall, winningNumsMsg = getWinningNums(args, url[0], bigBallPath[0], ballName[0])
    finalResults = winningNumsMsg
    for game,picks in myPicks.items():
        if 'powerball' in game:
            resultsMsg = checkWin(args, balls, bigBall, ballName[0], picks)
            finalResults += resultsMsg

elif args.megamillions:
    mailSubject = "Megamillions"
    balls, bigBall, winningNumsMsg = getWinningNums(args, url[1], bigBallPath[1], ballName[1])
    finalResults = winningNumsMsg
    for game,picks in myPicks.items():
        if 'megaMills' in game:
            resultsMsg = checkWin(args, balls, bigBall, ballName[1], picks)
            finalResults += resultsMsg

elif args.cash4life:
    mailSubject = "Cash 4 Life"
    balls, bigBall, winningNumsMsg = getWinningNums(args, url[2], bigBallPath[2], ballName[2])
    finalResults = winningNumsMsg
    for game,picks in myPicks.items():
        if 'cash4Life' in game:
            resultsMsg = checkWin(args, balls, bigBall, ballName[2], picks)
            finalResults += resultsMsg

elif args.lotto:
    mailSubject = "Lotto"
    balls, bigBall, winningNumsMsg = getWinningNums(args, url[3], bigBallPath, ballName[3])
    finalResults = winningNumsMsg
    for game,picks in myPicks.items():
        if 'lotto' in game:
            resultsMsg = checkWin(args, balls, bigBall, ballName[3], picks)
            finalResults += resultsMsg

else:
    parser.print_help()
    print()
    exit()

print (finalResults)

# send the results by email
try:
    from secrets import creds
except:
    print("You need to configure your email credentials. \
    \nAn example 'secrets.py' file has been created. Please add your email creds.")
    createSecrets()
    exit()
try:
    sendMail(creds, mailSubject, finalResults)
except smtplib.SMTPAuthenticationError:
    print("Invalid email credentials. \
    \nPlease revise secrets.py")
