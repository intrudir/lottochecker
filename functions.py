import requests, smtplib
from datetime import date
from bs4 import BeautifulSoup
from email.message import EmailMessage

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}

def createNumbers(scriptDir):
    content = """\
my numbers:
  powerball:
    - 1
    - 2
    - 3
    - 4
    - 5
    - 6

  powerball2:
    - 1
    - 2
    - 3
    - 4
    - 5
    - 6

moms numbers:
  megamillions:
    - 1
    - 2
    - 3
    - 4
    - 5
    - 6
"""
    with open(scriptDir + '/numbers.yaml', 'w') as nf:
        nf.write(content)
    return True


def getWinningNumbers(check):
    # For some reason megaMillions has to be spelled this way
    if check == "megamillions":
        check = "megaMillions"

    url = "https://www.flalottery.com:443/{}".format(check)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    gamePageBalls = soup.find("div", {"class": "gamePageBalls"})
    balls = gamePageBalls.find_all("span", {"class": "balls"})
    winnerBalls = []
    for b in balls:
        try:
            winnerBalls.append(int(b.text))
        except ValueError:
            pass

    return winnerBalls


def checkMyNums(check, myNumbers, winningNums, highest):
    d = date.today()
    msg = "Date: {}\n".format(d)
    msg += "Winning {} numbers: {}\n".format(check, winningNums)

    # my numbers:
    for picks in myNumbers:
        msg += "\n{}: ".format(picks)

        # powerball: [1, 2, 3, 4, 5, 6]
        for game in myNumbers[picks]:
            matched = 0
            if game.lower().find(check) != -1:
                msg += "\n    {}: {}".format(game, myNumbers[picks][game])
                for n in myNumbers[picks][game]:
                    if n in winningNums:
                        matched += 1
                msg += "\n    {} numbers matched\n".format(matched)

            if matched:
                if matched > highest:
                    highest = matched

    return msg, matched, highest


def getHistory(check):
    if check == "powerball":
        check = "pb.htm"
    elif check == "megamillions":
        check = "mmil.htm"
    elif check == "lotto":
        check = "l6.htm"

    drawDate = ""
    historyWinners = {}
    numList = []
    url = "https://www.flalottery.com/exptkt/{}".format(check)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all("table")
    for a in tables:
        # tr_top == every <tr valign="top">
        tr_top = a.find_all("tr", {"valign": "top"})
        for b in tr_top:
            fonts = b.find_all("font", {"face": "helvetica"})
            for c in fonts:
                text = c.text

                # get draw date
                if '/' in text:
                    drawDate = text

                # append numbers to list
                # need to check if drawDate has been set in order to avoid
                # appending page numbers for each table.
                try:
                    int(text)
                except ValueError:
                    pass
                else:
                    if drawDate:
                        numList.append(text)

                # add numbers to a dictionary with draw date
                # then reset number list
                if len(numList) == 6:
                    if drawDate in historyWinners:
                        historyWinners[drawDate + " DP"] = numList
                        numList = []
                        drawDate = ""
                    else:
                        historyWinners[drawDate] = numList
                        numList = []
                        drawDate = ""
    return historyWinners


def checkHistory(check, myNumbers, historyWinners):
    msg = ""
    # my numbers:
    for picks in myNumbers:
        print("\n{}: ".format(picks))

        for game in myNumbers[picks]:
            if game.lower().find(check) != -1:
                # powerball: [1, 2, 3, 4, 5, 6]
                print("    {}: {}\n".format(game, myNumbers[picks][game]))

                for drawDate, hNumbers in historyWinners.items():
                    matched = 0
                    pbMatched = False

                    if check == "powerball" or check == "megamillions":
                        for n in myNumbers[picks][game][:5]:
                            if str(n) in hNumbers:
                                matched += 1
                        if str(myNumbers[picks][game][-1]) == hNumbers[-1]:
                            pbMatched = True

                        if matched == 5 and pbMatched is True:
                            print("ALL 6 NUMBERS MATCHED: {}: {}".format(drawDate, hNumbers))
                            print()

                        if matched >= 3:
                            print("3 or more numbers matched: {}: {}".format(drawDate, hNumbers))
                            print("{} ball matched?: {}".format(check, pbMatched))
                            print()

                    if check == "lotto":
                        for n in myNumbers[picks][game]:
                            if str(n) in hNumbers:
                                matched += 1

                        if matched == 6:
                            print("ALL 6 NUMBERS MATCHED: {}: {}".format(drawDate, hNumbers))
                            print()

                        if matched >= 4:
                            print("4 or more numbers matched: {}: {}".format(drawDate, hNumbers))
                            print()
    exit()


def sendMail(user, password, subject, finalResults):
    to_email = "lottoscript1@gmail.com"
    from_email = "lottoscript1@gmail.com"
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    msg = EmailMessage()
    msg.set_content(finalResults)

    msg['To'] = to_email
    msg['From'] = from_email
    msg['Subject'] = subject
    server.login(user, password)
    server.send_message(msg)
