# lottochecker
Check lotto numbers

<h1> Usage: </h1>
Run with no args or -h to see usage.

```
% python3 lottochecker.py
usage: lottochecker.py [-h] [--powerball] [--megamillions] [--cash4life]
                       [--lotto]

This script is used to check for lotto numbers and see if you won.

optional arguments:
  -h, --help      show this help message and exit
  --powerball     check Powerball numbers
  --megamillions  check Megamillions numbers
  --cash4life     check Cash 4 Life numbers
  --lotto         check Lotto numbers
```

<h3> Add the numbers you want to check in lottochecker.py </h3>

![image](https://user-images.githubusercontent.com/24526564/83340441-03c90d00-a2a6-11ea-88cd-63bcb633278f.png)

<h3> Send results via email </h3>
Currently configured for use with gmail.
<br> Create a secrets.py file in the following format and fill in your credentials.
<br> If you run the script without configuring this, it will add a template for you.

![image](https://user-images.githubusercontent.com/24526564/83340472-9f5a7d80-a2a6-11ea-87f0-26fe4ac271ba.png)

```
# Change email and password values
creds = {
'user': "xxxxx@gmail.com",
'passwd': "xxxxxx"
}
```

You should be able to easily add a cron-job / scheduled task to run this automatically :)
