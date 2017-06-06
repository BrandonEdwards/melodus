import math

def timeToString(time):
	mins = time * 5;
	hours = math.floor(mins / 60)
	days = math.floor(hours / 24)

	string = "Day " + (days + 1) + " at time " + (hours - (days * 24)) + ":" + (mins - (hours * 60))

	return string