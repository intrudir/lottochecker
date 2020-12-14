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


def get_game_data(game):
    """ Fetch game data like:
    jackpot numbers,
    next jackpot date & amount,
    winnings table that describes what you get when you win X of X numbers.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}

    url = "https://www.flalottery.com:443/{}".format(game)
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.content, 'html.parser')

    # get winning jackpot numbers
    game_page_balls = soup.find_all("div", {"class": "gamePageBalls"})

    # get next jackpot date and amount
    jackpotDiv = soup.find("div", {"class": "nextJackpot"}).find_all("p")
    jDate = jackpotDiv[1].text
    jPot = soup.find("p", {"class": "gameJackpot"}).text
    jackpot = {"Next Jackpot: ": jDate, "Jackpot amount: ": jPot}

    # get winnings table
    winTable = soup.find("table", {"class": "style1 games"})

    return game_page_balls, jackpot, winTable


def get_jackpot_nums(game_page_balls, index):
    balls = game_page_balls[index].find_all("span", {"class": "balls"})

    winners = []
    for ball in balls:
        try:
            winners.append(int(ball.text))
        except ValueError:
            pass

    return winners


def check_win(game_name, my_numbers, winners):
    msg_body = ""
    highest = 0
    highest_PB = None
    # my numbers:
    for picks in my_numbers:
        msg_body += "\n{}: ".format(picks)

        # powerball: [1, 2, 3, 4, 5, 6]
        for game in my_numbers[picks]:
            matched = 0
            pb_matched = False
            if game.lower().find(game_name) != -1:
                msg_body += "\n    {}: {}\n".format(game, my_numbers[picks][game])

                if game_name == "lotto":
                    for n in my_numbers[picks][game]:
                        if n in winners:
                            matched += 1
                    msg_body += "    {} numbers matched\n".format(matched)

                if game_name == "powerball" or game_name == "megamillions":
                    for n in my_numbers[picks][game][:5]:
                        if n in winners[:5]:
                            matched += 1
                    msg_body += "    {} numbers matched\n".format(matched)

                    if my_numbers[picks][game][-1] == winners[-1]:
                        pb_matched = True

                    msg_body += "    ball matched: {}\n".format(pb_matched)

            if matched:
                if matched > highest:
                    highest = matched
                    # If checking Lotto this should be False
                    highest_PB = pb_matched

    return msg_body, highest, highest_PB


def prep_msg(game_name, game_type, winners, jackpot_info, msg_body):
    d = date.today()
    if game_type == "double play":
        jackpot_info["Jackpot amount: "] = "Check double play table"

    msg_head = """\
Game: {} {}
Date: {}
Winning numbers: {}

Next draw date: {}
Jackpot amount: {}
""".format(game_type, game_name, d, winners, jackpot_info["Next Jackpot: "], jackpot_info["Jackpot amount: "])

    msg = msg_head + msg_body

    return msg


def get_history(page):
    url = "https://www.flalottery.com/exptkt/{}".format(page)
    drawDate = ""
    history_winners = {}
    numList = []
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
                    if drawDate in history_winners:
                        history_winners[drawDate + " DP"] = numList
                        numList = []
                        drawDate = ""
                    else:
                        history_winners[drawDate] = numList
                        numList = []
                        drawDate = ""

    return history_winners


def check_history(game_name, my_numbers, history_winners):
    # my numbers:
    for picks in my_numbers:
        print("\n{}: ".format(picks))

        for game in my_numbers[picks]:
            if game.lower().find(game_name) != -1:
                # powerball: [1, 2, 3, 4, 5, 6]
                print("    {}: {}\n".format(game, my_numbers[picks][game]))

                for drawDate, hNumbers in history_winners.items():
                    matched = 0
                    pb_matched = False

                    if game_name == "lotto":
                        for n in my_numbers[picks][game]:
                            if str(n) in hNumbers:
                                matched += 1

                        if matched == 6:
                            print("ALL 6 NUMBERS MATCHED: {}: {}".format(drawDate, hNumbers))
                            print()

                        if matched >= 4:
                            print("4 or more numbers matched: {}: {}".format(drawDate, hNumbers))
                            print()

                    if game_name == "powerball" or game_name == "megamillions":
                        for n in my_numbers[picks][game][:5]:
                            if str(n) in hNumbers[:5]:
                                matched += 1
                        if str(my_numbers[picks][game][-1]) == hNumbers[-1]:
                            pb_matched = True

                        if matched == 5 and pb_matched is True:
                            print("    ALL 6 NUMBERS MATCHED: {}: {}".format(drawDate, hNumbers))
                            print()

                        if matched >= 3:
                            print("    3 or more numbers matched: {}: {}".format(drawDate, hNumbers))
                            print("    {} ball matched?: {}".format(game_name, pb_matched))
                            print()

    exit()


class Game:
    """ Do stuff for a particular lottery game."""

    def __init__(self, game, game_type):
        self.game = game
        self.game_type = game_type

    def get_win_data(self):
        """Get winning numbers."""

        game_page_balls, jackpot_info, win_table = get_game_data(self.game)
        self.game = self.game.lower()

        if self.game_type == "double play":
            winners = get_jackpot_nums(game_page_balls, 1)
        else:
            winners = get_jackpot_nums(game_page_balls, 0)

        return winners, jackpot_info, win_table

    def check_win(self, my_numbers, winners):
        """Check your provided numbers against winning nums."""

        msg_body, highest, highest_PB = check_win(self.game, my_numbers, winners)

        return msg_body, highest, highest_PB

    def prep_msg(self, winners, jackpot_info, msg_body):
        """Prepare final results message for print and email."""

        msg = prep_msg(self.game, self.game_type, winners, jackpot_info, msg_body)

        return msg

    def check_historical_data(self, my_numbers):
        """check against historical win data for a specified game."""

        if self.game == "powerball":
            history_winners = get_history("pb.htm")

        elif self.game == "megamillions":
            history_winners = get_history("mmil.htm")

        elif self.game == "lotto":
            history_winners = get_history("l6.htm")

        check_history(self.game, my_numbers, history_winners)


def send_mail(user, password, subject, finalResults):
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
