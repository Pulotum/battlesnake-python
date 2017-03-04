import bottle
import os
import random
import math


def getTaunt():
	taunts = [	'This is a test taunt. If you see this please contact your internet provider.',
				'My data structure is better than your data structure',
				'My dad works at nintendo',
				'I AM A BABY',
				'I love to eat food, for I am a baby',
				'I Think, Therefore I Am Baby',
				'BRING ME MY BROWN PANTS',
				'Did you know that I am indeed a Baby?']
				
	return random.choice(taunts)


def isSnakeClose(data):
	uid = data["you"]
	snakes = data["snakes"]
	
	for snek in snakes:
		if(snek["id"] == uid):
			me = snek
		
	meX = me["coords"][0][0]
	meY = me["coords"][0][1]
	
	possible = []
	range = 3
	
	x = meX - range
	while (x <= meX + range):
		y = meY - range
		while (y <= meY + range):
			possible.append([x,y])
			y = y + 1
		x = x + 1
		
	print "possible -", possible	
	
	for snek in snakes:
		if(snek["id"] != uid):
			if (snek["coords"][0] in possible):
				lin = len(snek["coords"])
				print "----Snake of length", lin, " is in our range"
	
	
def isDangerSquare(data, next):
	dangers = []
	
	snakes = data["snakes"]
	
	for snake in snakes:
		curds = snake["coords"]
		for cord in curds:
			dangers.append(cord)
        #area around enemy snake head
        if(snake["id"] != data["you"]):
            head = snake["coords"][0]
            #right
            dangers.append([head[0] + 1, head[1]])
            #left
            dangers.append([head[0] - 1, head[1]])
            #up
            dangers.append([head[0], head[1] - 1])
            #down
            dangers.append([head[0], head[1] + 1])
        print "danger -", dangers
        if(snake["id"] == data["you"]):
            if((next[0] < 0) or (next[0] > data["width"])):
                print "Wall on x plane"
                return True
            if((next[1] < 0) or (next[1] > data["height"])):
                print "Wall on y plane"
                return True
	
	if( next in dangers):
		print "--Square taken"
		return True
	else:
		print "--Square is good"
		return False
		

@bottle.route('/static/<path:path>')
def static(path):
	return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():

	data = bottle.request.json
	game_id = data['game_id']
	board_width = data['width']
	board_height = data['height']

	head_url = 'https://thumb1.shutterstock.com/display_pic_with_logo/88356/107460737/stock-photo-beautiful-expressive-adorable-happy-cute-laughing-smiling-baby-infant-face-showing-tongue-isolated-107460737.jpg'
	
	# TODO: Do things with data

	return {
		'color': '#ff6666',
		'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
		'head_url': head_url,
		'name': 'Baby Face',
		'head_type': 'safe',
		'tail_type': 'pixel'
	}

	

@bottle.post('/move')
def move():
	global closeFood
	
	data = bottle.request.json
	
	uid = data["you"]
	snakes = data["snakes"]
	
	for snek in snakes:
		if(snek["id"] == uid):
			me = snek
		
	meX = me["coords"][0][0]
	meY = me["coords"][0][1]
	
	closestCord = []
	closestDist = 100
	
	for item in data["food"]:
		currentX = abs(meX - item[0])
		currentY = abs(meY - item[1])
		
		currentDist = currentX + currentY
		
		if(currentDist < closestDist):
			closestDist = currentDist
			closestCord = item
		
	print "me -", meX, meY
	print "closestCord -", closestCord
	
	isSnakeClose(data)
	
	if((closestCord[0] < meX)):
		movement = 'left'
		wantedSquare = [meX - 1, meY]
	elif((closestCord[0] > meX)):
		movement = 'right'
		wantedSquare = [meX + 1, meY]
	elif((closestCord[1] > meY)):
		movement = 'down'
		wantedSquare = [meX, meY + 1]
	elif((closestCord[1] < meY)):
		movement = 'up'
		wantedSquare = [meX, meY - 1]

	print "wanted movement -", movement
	
	isGood = isDangerSquare(data, wantedSquare)
	
	if(isGood):
		#----
		if(movement == 'right'):
			if(isDangerSquare(data, [meX, meY - 1])):
				if(isDangerSquare(data, [meX, meY + 1])):
					if(isDangerSquare(data, [meX - 1, meY])):
						movement = 'right'
					else:
						movement = 'left'
				else:
					movement = 'down'
			else:
				movement = 'up'
		#----
		elif(movement == 'left'):
			if(isDangerSquare(data, [meX, meY - 1])):
				if(isDangerSquare(data, [meX, meY + 1])):
					if(isDangerSquare(data, [meX + 1, meY])):
						movement = 'left'
					else:
						movement = 'right'
				else:
					movement = 'down'
			else:
				movement = 'up'
		#---
		elif(movement == 'down'):
			if(isDangerSquare(data, [meX, meY - 1])):
				if(isDangerSquare(data, [meX - 1, meY])):
					if(isDangerSquare(data, [meX + 1, meY])):
						movement = 'down'
					else:
						movement = 'right'
				else:
					movement = 'left'
			else:
				movement = 'up'
		#---
		elif(movement == 'up'):
			if(isDangerSquare(data, [meX, meY + 1])):
				if(isDangerSquare(data, [meX - 1, meY])):
					if(isDangerSquare(data, [meX + 1, meY])):
						movement = 'up'
					else:
						movement = 'right'
				else:
					movement = 'left'
			else:
				movement = 'down'
		#---
	
	print "Next Check -------"
		
	
	# TODO: Do things with data	
	
	return {
		'move': movement,
		'taunt': getTaunt()
	}
	
@bottle.post('/end')
def end():
	data = bottle.request.json

	# TODO: Do things with data

	return {
		'taunt': 'BABY FACE!'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
