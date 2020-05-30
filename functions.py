import requests, smtplib
from lxml import html
from email.message import EmailMessage

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def createSecrets():
    content = """# Change email and password values
creds = {
'user': "xxxxx@gmail.com",
'passwd': "xxxxxx"
}
"""
    with open('secrets.py', 'w') as fp:
        fp.write(content)
    return True


def getWinningNums(args, url, bigBallPath, ballName):
    page = requests.get(url, headers=headers)
    tree = html.fromstring(page.content)
    balls = tree.xpath('//span[@class="balls"]/text()')
    jackpotDate = tree.xpath('//div[@class="gamePageNumbers"]/p/text()')[1]

    if not args.lotto:
        balls = balls[:5]
        bigBall = tree.xpath(bigBallPath)
        bigBall = bigBall[0]
        bbMsg = "Today's {}: {}".format(ballName, bigBall)
    else:
        balls = balls[:6]
        bigBall = ''
        bbMsg = ''

    winningNumsMsg = (
"""
{0}
Jackpot Date: {1}
{2}
Today's numbers: {3}
{0}
""".format('*' * 40, jackpotDate, bbMsg, ','.join(balls)))

    return balls, bigBall, winningNumsMsg


def checkWin(args, balls, bigBall, ballName, picks):
    matched = []
    bbMsg = ''
    if not args.lotto:
        bbMsg = "Your {}: {}".format(ballName, picks['bigBall'])
        for ball in picks['balls']:
            if ball in balls[:5]:
                matched.append(ball)

        if picks['bigBall'] == bigBall:
            matchMsg = "{} matched!".format(ballName)
            matchBB = True
        else:
            matchMsg = "{} did not match.".format(ballName)
            matchBB = False
    else:
        for ball in picks['balls']:
            if ball in balls[:6]:
                matched.append(ball)

    if args.powerball or args.megamillions:
        if len(matched) == 5 and matchBB == True:
            result = "CHECK THEM NOW. YOU MIGHT HAVE WON THE JACKPOT."
        elif len(matched) >= 1 and matchBB == True:
            result = "You matched {} numbers and the {}! You may have won something, check online".format(len(matched), ballName)
        elif len(matched) == 0 and matchBB == True:
            result = "You matched {} numbers but got the {}! You may have won something (free ticket or ~10$). Check online.".format(len(matched), ballName)
        elif len(matched) >= 3 and matchBB == False:
            result = "You matched {} numbers but no {}. You may have won something, check online.".format(len(matched), ballName)
        else:
            result = "Nothing yet. Keep playing!"

    elif args.cash4life:
        if len(matched) == 5 and matchBB == True:
            result = "CHECK THEM NOW. YOU MIGHT HAVE WON THE JACKPOT."
        elif len(matched) >= 1 and matchBB == True:
            result = "You matched {} numbers and got the CB! You may have won something (free ticket or ~10$). Check online.".format(len(matched))
        elif len(matched) >= 2 and matchBB == False:
            result = "You matched {} numbers but no CB. You may have won something, check online.".format(len(matched))
        else:
            result = "Nothing yet. Keep playing!"

    elif args.lotto:
        if len(matched) == 6:
            result = "CHECK THEM NOW. YOU MIGHT HAVE WON THE JACKPOT."
        elif len(matched) >= 2:
            result = "You matched {} numbers! You may have won something, Check online".format(len(matched))
        else:
            result = "Nothing yet. Keep playing!"

    resultsMsg = (
"""
{}
Picks: {}

{} numbers matched: {}
{}
\n{}
""".format(bbMsg, ','.join(picks['balls']), len(matched), ','.join(matched), result, '*' * 40))

    return resultsMsg

def sendMail(creds, subject, finalResults):
    to_email = "lottoscript1@gmail.com"
    from_email = "lottoscript1@gmail.com"
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    msg = EmailMessage()
    msg.set_content(finalResults)

    msg['To'] = to_email
    msg['From'] = from_email
    msg['Subject'] = subject
    server.login(creds['user'], creds['passwd'])
    server.send_message(msg)
