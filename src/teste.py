import inquirer
questions = [
  inquirer.List('WebScraper',
    message="Qual método de coleta você deseja?",
    choices=['Selenium', 'Request'],
  ),
]
answers = inquirer.prompt(questions)
print(answers["WebScraper"])