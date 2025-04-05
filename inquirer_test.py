import inquirer
from pprint import pprint

questions = [
    inquirer.Confirm("continue", message="Should I continue"),
    inquirer.Confirm("stop", message="Should I stop", default=True),
]

answers = inquirer.prompt(questions)

pprint(answers)