#!/usr/bin/env python
import sys
import getopt

#reopen stdout unbuffered, stackoverflow 230751
#sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

def to_stdout(string):
	sys.stdout.write(str(string))
	sys.stdout.flush()

def to_stderr(string):
	sys.stderr.write(str(string))
	sys.stderr.flush()

def my_pain(eulogy):
	pain = "\n\033[0m\033[7m" + '<< '
	pain += str(eulogy)
	pain += ' >>' + "\033[0m\n"
	to_stderr(pain)
	sys.exit(1)

def ansi_reset():
	to_stdout ("\033[0m\n")

def rainbows_constructor(colour, mode, character):
	h = colour / 43
	f = colour - 43 * h
	t = f * 255 / 43
	q = 255 - t

	ansi_code = "\033[%s;2;" % str(mode)

	if h == 0:
		ansi_code += "255;%s;0m" % str(t)
	elif h == 1:
		ansi_code += "%s;255;0m" % str(q)
	elif h == 2:
		ansi_code += "0;255;%sm" % str(t)
	elif h == 3:
		ansi_code += "0;%s;255m" % str(q)
	elif h == 4:
		ansi_code += "%s;0;255m" % str(t)
	elif h == 5:
		ansi_code += "255;0;%sm" % str(q)
	else:
		my_pain ( 'h='+str(h)+' colour='+str(colour)+' mode='+str(mode)+' character='+character )

	ansi_code += str(character)
	to_stdout (ansi_code)

def is_newline(character):
	if character == "\n":
		ansi_reset()
		return True
	else:
		return False

def change_direction(colour):
	if colour >= colour_max:
		return -1
	elif colour <= colour_min:
		return 1


########################################################

"""
-f --file
-r --rate
-b --bg
-n --noreset
-q --quiet
-h --help
-v --verbose
-V --version
-t --test


try:
    opts, args = getopt.getopt(argv, 'f:r:bnqhvVt',
    								['file=', 'rate=', 'bg', 'noreset', 'quiet', 'help',
    								'verbose', 'version' 'test'])
except getopt.GetoptError:
    'err on opts'
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-m', '--miner'):
        miner_name = arg
    elif opt in ('-p', '--params'):
        params = arg
    else:
        usage()
        sys.exit(2)

"""
########################################################

debug=0
colour=0
direction=1 #1=increment, -1=decrement
rate=2
colour_min = 0
colour_max = 255

try:
	while True:
		character = sys.stdin.read(1)
		if not character:
			ansi_reset()
			break

		# first check if it's outside the 0-255 range
		if not (colour_min < colour <= colour_max):
			direction = change_direction(colour)

		# incrementing the colour
		if direction == 1:
			colour = colour + rate
		elif direction == -1:
			colour = colour - rate

		if debug:
			if character == "\n":
				to_stdout ("\n")
			else:
				rainbows_constructor(colour, 38, str(colour)+" " )
		else:

			if is_newline(character):
				colour = 0
			else:
				#print colour and character
				rainbows_constructor(colour, 38, character)

except KeyboardInterrupt:
	sys.exit(0)

