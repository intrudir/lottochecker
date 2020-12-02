# lottochecker
Check lotto, powerball, megamillions numbers

# Usage:
Run with no args or -h to see usage.

```bash
% python3 lottochecker.py
usage: lottochecker.py [-h] [-c {powerball,megamillions,lotto}]

This script is used to check for lotto numbers and see if you won.

optional arguments:
  -h, --help            show this help message and exit
  -c {powerball,megamillions,lotto}, --check {powerball,megamillions,lotto}
                        check winning numbers for specified game
```
<br>

## Add the numbers you want to check in numbers.yaml
![image](https://user-images.githubusercontent.com/24526564/100815324-9ee79e80-3411-11eb-9879-040fa7bb6ece.png)

The first names can be whatever you want. eg. "my numbers", "my dogs numbers", whatever. <br>
The game names have at least "powerball", "megamillions", or "lotto". So you may call it "powerball2" or "powerball 2" etc.
<br>

## Send results via email
Currently configured for use with gmail.
<br> 
Fill in your credentials at the top of lottochecker.py
**hint** use an app password!
<br> 

You should be able to easily add a cron-job / scheduled task to run this script automatically :)
