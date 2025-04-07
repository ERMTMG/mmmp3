import inquirer
from pprint import pprint


questions = [
    inquirer.Confirm("continue", message="Should I continue"),
    inquirer.Confirm("stop", message="Should I stop", default=True),
    inquirer.List('q3', 'select an option',
                  choices = [('Option1', 1), ('Option2', 2), ('option3',3)])
]

answers = inquirer.prompt(questions)

pprint(answers)