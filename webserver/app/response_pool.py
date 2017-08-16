from random import randint
#response pools
welcome_messages = ["Hello beautiful", "I see you're checing yourself out, wanna talk?", "Like what you see?", "Your presence makes me feel cuddly."]

#source: http://www.jokes4us.com/pickuplines/cutepickuplines.html]

def randomResponse():
	value = randint(0,(len(welcome_messages)-1))
	return welcome_messages[value]
