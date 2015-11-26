import requests
baseUrl = "http://api-usa3.akinator.com/ws/"
tmpdatas = None
consts = {
	'MAX_QUESTIONS': 79,
	'QUESTION_PROP_WHATEVER': 5,
	'QUESTIONS_BAD_WHATEVER': 25,
	'PROG_LIST': 97
}
def shouldPropose(si):
	if si["step"] == consts["MAX_QUESTIONS"]:
		return True
	else:
		if int(si["step"]) - tmpdatas["solp"] < consts['QUESTION_PROP_WHATEVER']:
			return False
		else:
			if float(si["progression"]) > consts["PROG_LIST"] or int(si["step"]) - tmpdatas["solp"] == consts["QUESTIONS_BAD_WHATEVER"]:
				if si["step"] == 75:
					return False
				else:
					return True
			else:
				return False
nsr = requests.get(baseUrl+"new_session", {
	'player': "desktopPlayer",
	'partner': 1
});
j = nsr.json()
tmpdatas = j["parameters"]["identification"]
tmpdatas["solp"] = 0
si = j["parameters"]["step_information"]
while True:
	if shouldPropose(si):
		tmpdatas["solp"] = int(si["step"])
		pr = requests.get(baseUrl+"list", {
			'session': tmpdatas["session"],
			'signature': tmpdatas["signature"],
			'step': si["step"],
			'size': 2,
			'mode_question': 0
		});
		tj = pr.json()
		things = tj["parameters"]["elements"]
		thing = things[0]["element"]
		print("===============")
		print("I have a guess.")
		print("===============")
		print()
		print(thing["name"])
		print(thing["description"])
		print()
		print("0: Yes")
		print("1: No")
		ans = int(input("Answer: "))
		if ans == 0:
			print("Yay!")
			break
	print("Question "+str(int(si["step"])+1)+" ("+si["progression"]+"% confidence)")
	print(si["question"])
	for i in range(0, len(si["answers"])):
		a = si["answers"][i]
		print(str(i)+": "+a["answer"])
	ans = int(input("Answer: "))
	ar = requests.get(baseUrl+"answer", {
		'session': tmpdatas["session"],
		'signature': tmpdatas["signature"],
		'step': si["step"],
		'answer': ans
	});
	j = ar.json()
	si = j["parameters"]
