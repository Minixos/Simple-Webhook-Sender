# made by Minixos

import requests
from os.path import exists
from sys import exit
from colorama import Fore, Style

# Create the file 'webhook.txt' if there is none
if not(exists("webhook.txt")):
	with open("webhook.txt", "w") as none:
		pass

# Display the available commandes
print(f"• {Fore.YELLOW}'{Style.RESET_ALL}{Fore.CYAN}§exit{Style.RESET_ALL}{Fore.YELLOW}' to exit the program{Style.RESET_ALL}")
print(f"• {Fore.YELLOW}'{Style.RESET_ALL}{Fore.CYAN}§home{Style.RESET_ALL}{Fore.YELLOW}' to return to the home screen{Style.RESET_ALL}")

def commandes(msg):
	"""
	Detect if the input is a command and execute the command.
	:Param msg: str
	:Out None:
	"""

	# All commands should start with '§'
	if not(msg[0] == "§"):
			return None
	else:
		msg = msg[1:]

	if msg == "home":
		main()
		return None

	if msg == "exit":
		print(f"• {Fore.YELLOW}See you soon !{Style.RESET_ALL}")
		exit()
		return None

	return None


def add():
	"""
	Add a webhook to the webhooks list.
	:Param None:
	:Out webhook_link, name: str
	"""

	invalid_answer = True
	while invalid_answer:
		webhook_link = input(f"‣ {Fore.YELLOW}Webhook link: {Style.RESET_ALL}")
		commandes(webhook_link) 
		if webhook_link[:33] != "https://discord.com/api/webhooks/" or requests.get(webhook_link).status_code != 200:
			print(f"{Fore.RED}Incorrect webhook link{Style.RESET_ALL}")
		else:
			invalid_answer = False

	default_name = requests.get(webhook_link).json()['name']
	name = input(f"‣ {Fore.YELLOW}Webhook name (by default '{default_name}'): {Style.RESET_ALL}")
	commandes(name)
	if not(len(name) > 0):
		name = default_name

	with open("webhook.txt", "a") as file:
		file.write(f"{webhook_link}|{name}\n")
	print(f"{Fore.GREEN}-> Webhook '{name}' saved with succes ✅{Style.RESET_ALL}")

	return webhook_link, name

def choose():
	"""
	'Home menu' of the program.
	:Param None:
	:Out lien, name: str
	"""

	with open("webhook.txt", "r") as file:
		ls_lien = file.readlines()

	name, lien = [], []
	for ligne in ls_lien:
		tmp_l, tmp_n = ligne.split("|")
		name.append(tmp_n.strip('\n'))
		lien.append(tmp_l)

	print(f"• {Fore.YELLOW}You have {Style.RESET_ALL}{Fore.WHITE}{len(name)}{Style.RESET_ALL}{Fore.YELLOW} webhooks saved.{Style.RESET_ALL}")

	# display the list of options
	for i in range(len(name)):
		print(f"{Fore.CYAN}{i}{Style.RESET_ALL}. {name[i]}")
	print(f"{Fore.CYAN}{len(name)}{Style.RESET_ALL}. add a webhook")

	invalid_answer = True
	while invalid_answer:
		action = input(f"‣ {Fore.YELLOW}Action: {Style.RESET_ALL}")
		commandes(action)
		if not(action.isnumeric()) or int(action) > len(name):
			print(f"{Fore.RED}-> There are no option '{action}'{Style.RESET_ALL}")
		elif int(action) == len(name):
			return add()
		else:
			return lien[int(action)], name[int(action)].strip('\n')

	return None

def main():
	"""
	Main function.
	:Param None:
	:Out None:
	"""

	webhook_link, name = choose()

	print(f"• {Fore.YELLOW}The session with the webhook '{name}' started.{Style.RESET_ALL}")

	while True:
		msg = input(f"‣ {Fore.YELLOW}Message:{Style.RESET_ALL} ")
		commandes(msg)
		code = requests.post(webhook_link, headers={"Content-Type": "application/json"}, json={"username": f"{name}", "content": f"{msg}"})
		if code.status_code == 204:
			print(f"{Fore.GREEN}-> Message sent ✅{Style.RESET_ALL}")
		else:
			print(f"{Fore.RED}-> Sending failure ❌{Style.RESET_ALL}")

	return None

main()
