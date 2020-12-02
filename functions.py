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


def checkMyNums(check, numbers, winningNums, highest):
    d = date.today()
    msg = "Date: {}\n".format(d)
    msg += "Winning {} numbers: {}\n".format(check, winningNums)

    # my numbers:
    for picks in numbers:
        msg += "\n{}: ".format(picks)

        # powerball: [1, 2, 3, 4, 5, 6]
        for game in numbers[picks]:
            matched = 0
            if game.lower().find(check) != -1:
                msg += "\n    {}: {}".format(game, numbers[picks][game])
                for n in numbers[picks][game]:
                    if n in winningNums:
                        matched += 1
                msg += "\n    {} numbers matched\n".format(matched)

            if matched:
                if matched > highest:
                    highest = matched

    return msg, matched, highest


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
