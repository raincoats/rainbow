#!/usr/bin/env python
#--> you know what i hate? when i’m doing unicoding: utf-8 <--#
import sys
import getopt
# from optparse import OptionParser

def to_stdout(string):
	sys.stdout.write(str(string))
	sys.stdout.flush()

def to_stderr(string):
	sys.stderr.write(str(string))
	sys.stderr.flush()

# remove all colours etc, reset terminal to default state.
def ansi_reset():
	to_stdout ("\033[0m\n")

#similar to bye() but no debug and no exit, used to debug when colours go strange
def my_pain(string):
	to_stdout ("\033[0m")
	to_stdout	("\033[7m" + string)
	to_stdout ("\033[0m")

# death function. writes some debug stuff to stderr in reverse video mode, and exits 1.
def bye(eulogy):
	ansi_reset()
	to_strerr("\033[0m" + "\033[7m" + 
		' ruh roh: --> ' + str(eulogy) + ' <-- ' +
		"\033[0m" + "\n")
	ansi_reset()
	sys.exit(1)


################## functions that deal with the program start here #########################

def is_newline(character):
	if character == "\n":
			return True
	else:
		return False

def change_direction(colour):
	if colour >= colour_max:
		return -1
	elif colour <= colour_min:
		return 1

def rainbows_constructor(colour, mode, character):
	if (colour < 0 or colour > 255):
		if debug:
			my_pain(character)
			return
		else:
			colour = 255 if colour > 255 else colour
			colour =   0 if colour <   0 else colour

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
		bye ( 'h='+str(h)+
					' colour=' + str(colour)+
					' mode='+str(mode)+
					' character='+character)
	
	to_stdout (ansi_code + str(character))

########################################################
def version():
	to_stdout("""\
rainbow.py v0.1
30 july 2015
by @reptar-xl - https://github.com/raincoats/rainbow
license: zf0 anti-copyright pledge
""")
	sys.exit(2)

def usage():
	helptext = """\
Usage: rainbow.py [OPTION...] [FILE]...
Make text all rainbowy.
If -f is not given, read from stdin.

  -f, --file <file>  Read from file instead of stdin
  -r, --rate <rate>  Rate that it cycles through colours (from 0 to 255, default 4)
  -b, --bg           Background colour mode
      --fg           Foreground colour mode (default)
  -s, --start        Colour to start at (0 to 255) [NOT IMPLEMENTED YET]
      --noreset      Don’t reset colour on newlines
      --debug        Debug mode (instead of chars, it prints the colour codes)
  -h, --help         You know what this does (displays this help text)
  -q, --quiet        Hide error messages
  -t, --test         Tests your terminal’s colour capability
  -v, --verbose      Does nothing (in case you assumed it meant verbose, which is default)
  -V, --version      Display license & version info

Examples:
    rainbow < /etc/passwd
    dmesg | rainbow -r1
    rainbow -f /etc/resolv.conf -r 12
    dd if=/dev/sda | rainbow | dd of=/dev/sda (NO DON’T)
"""
	to_stdout(helptext)
	sys.exit(2)

###################################################################################################

debug=False
colour=0
direction=1 #1=increment, -1=decrement
rate=4
colour_min=(  0 + rate)
colour_max=(255 - rate)
mode=38 #38 for foreground, 48 for background
reset_on_newlines=True
quiet=False #by default anyway

###################################################################################################
#getting options
try:
	opts, args = getopt.gnu_getopt(sys.argv[1:], 'f:r:bnqhvVts',
									['file=', 'rate=', 'bg', 'fg', 'noreset', 'quiet', 'help',
									'verbose', 'version', 'test', 'start', 'debug'])

	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage()
		if opt in ('-V', '--version'):
			version()
		elif opt in ('-b', '--bg'):
			mode = 48
		elif opt in ('--fg'):
			mode = 38
		elif opt in ('-s', '--start'):
			colour = int(arg)
		elif opt in ('-f', '--file'):
			infile = arg
		elif opt in ('-r', '--rate'):
			rate = int(arg)
			colour_min=(  0 + rate)
			colour_max=(255 - rate)

		elif opt in ('-v', '--verbose'):
			quiet = False
		elif opt in ('-q', '--quiet'):
			quiet = True
		elif opt in ('--noreset'):
			reset_on_newlines = False
		elif opt in ('--debug'):
			debug = True
		else:
			usage()

except getopt.GetoptError:
	'err on opts'
	sys.exit(2)

###################################################################################################

try:
	while True:
		character = sys.stdin.read(1)
		if not character:
			if debug:
				to_stderr("----------------------------------------------\n")
				to_stderr("rate: %-5s min: %-5s max: %-5s" % (rate, colour_min, colour_max))
			ansi_reset()
			break

		# first check if it's outside the 0-255 range
		# if it is, then decrement/increment it
		if (colour <= colour_min) or (colour >= colour_max):
			direction = change_direction(colour)

		# incrementing the colour
		colour = (colour + rate) if (direction == 1) else (colour - rate)


		if debug:
			if character == "\n":
				to_stdout ("\n")
			else:
				rainbows_constructor(colour, mode, str(colour)+" " )

		elif is_newline(character):
			colour=0 if reset_on_newlines else colour
			ansi_reset()
		else:
			rainbows_constructor(colour, mode, character) 			#print colour and character

except KeyboardInterrupt:
	ansi_reset()
	sys.exit(0)
