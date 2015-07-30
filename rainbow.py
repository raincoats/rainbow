#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
	if character == "\n" and reset_on_newlines == True:
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
      --noreset      Don’t reset colour on newlines
      --debug        Debug messages (instead of printing characters, it prints colour codes)
  -q, --quiet        Hide error messages
  -h, --help         You know what this does (displays this help text)
  -v, --verbose      Does nothing (in case you assumed it meant verbose, which is default)
  -V, --version      Display license & version info
  -t, --test         Tests your terminal’s colour capability

Examples:
    rainbow < /etc/passwd
    dmesg | rainbow -r1
    rainbow -f /etc/resolv.conf -r 12
    dd if=/dev/sda | rainbow | dd of=/dev/sda (NO DON’T)
"""
	to_stdout(helptext)
	sys.exit(2)

###################################################################################################

debug=0
colour=0
direction=1 #1=increment, -1=decrement
rate=2
colour_min = 0
colour_max = 255
mode=38 #38 for foreground, 48 for background
reset_on_newlines=True
quiet = False #by default anyway

###################################################################################################
#getting options
try:
	opts, args = getopt.gnu_getopt(sys.argv[1:], 'f:r:bnqhvVt',
									['file=', 'rate=', 'bg', 'fg', 'noreset', 'quiet', 'help',
									'verbose', 'version', 'test'])

	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage()
		if opt in ('-V', '--version'):
			version()
		elif opt in ('-b', '--bg'):
			mode = 48
		elif opt in ('--fg'):
			mode = 38
		elif opt in ('-f', '--file'):
			infile = arg
		elif opt in ('-r', '--rate'):
			rate = arg
		elif opt in ('-v', '--verbose'):
			quiet = False
		elif opt in ('-q', '--quiet'):
			quiet = True
		elif opt in ('--noreset'):
			reset_on_newlines = False
		elif opt in ('--debug'):
			debug = 1

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
				rainbows_constructor(colour, mode, str(colour)+" " )
		else:

			if is_newline(character):
				colour = 0
			else:
				#print colour and character
				rainbows_constructor(colour, mode, character)

except KeyboardInterrupt:
	sys.exit(0)

