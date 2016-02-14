#!/usr/bin/env zsh
LC_ALL=C
trap 'printf -- "\033[m\n"; exit' SIGINT SIGSTOP SIGQUIT

name=$(basename "$0")

function rainbows_constructor {
	local h=$[ $1 / 43 ]
	local f=$[ $1 - 43 * $h ]
	local t=$[ $f * 255 / 43 ]
	local q=$[ 255 - $t ]
	[ $2 ] && rainbow_mode=$2
	local assembled=$'\033['"${rainbow_mode:-38}"';2;'

	case $h in
		0)	printf -- "%s" "${assembled}""255;${t};0m" ;;
		1)	printf -- "%s" "${assembled}""${q};255;0m" ;;
		2)	printf -- "%s" "${assembled}""0;255;${t}m" ;;
		3)	printf -- "%s" "${assembled}""0;${q};255m" ;;
		4)	printf -- "%s" "${assembled}""${t};0;255m" ;;
		5)	printf -- "%s" "${assembled}""255;0;${q}m" ;;
		*)	die 'what? h in rainbows_constructor was '"${h}" ;;
		esac

}

# draws a rainbow line to test 24bit colour capability
function rainbow-test {
	# find the terminal's column count, so the line isn't too big
	if   [ $COLUMNS -ge 255 ]; then local rate=1
	elif [ $COLUMNS -ge 128 ]; then local rate=2
	elif [ $COLUMNS -ge  86 ]; then local rate=3
	elif [ $COLUMNS -ge  64 ]; then local rate=4
	else local rate=5
	fi
	for colour in {0..255..$rate}; do
		rainbows_constructor $colour 48
		printf -- ' '
	done
	printf -- "%s\n%s\n" $'\033[m' "can you see a rainbow line above? if so, you have 24 bit colour! wahay!"
	exit 0
}

function reset_colour_counter {
	# why a function for this?
	#	1. because i can
	#	2. because if the flag -n is passed, the getopts loop makes this
	#      an empty function, which imo looks slightly cleaner but is very
	#      confusing and i cba fixing it and goddamn i used to program strangely
	colour=0
}

function error die {  #error messages to stdout, like "rainbow: file not found", optionally die
	printf -- "%s: \033[m%s\n" "$name" "$@" >&2
	[ "$0" = 'die' ] && exit 1
}

function main_char_loop {
	# zsh version of read -rn1 (or so stack overflow says...)
 	while read -rku0 char; do

 		#fix for background colours, reset colour before newline
 		if [ ${char} = $'\n' ]; then printf -- $'\033[m\n'; return; fi

 		#print ansi colour code itself
		rainbows_constructor $colour || { die "invalid colour: $colour" }

		#print colour
		printf -- "%s" "${char}"

		#if the colour is 255, then start decrementing.
		#if the colour is 0, start incrementing.
		if [ $colourdirection -eq 0 ]; then
			colour=$[ colour + $rate ]
			[ $colour -ge $max ] && { colour=$max; colourdirection=1 }
		else
			colour=$[ colour - $rate ]
			[ $colour -le $min ] && { colour=$min; colourdirection=0 }
		fi
	done
}

function check_file {
	# i feel this is pretty self explanatory
	[  ! "$1" ] && die '-f needs an argument, eg. “-f /etc/passwd”'
	[ -d "$1" ] && die      'is a directory: '"$1"
	[ -e "$1" ] || die      'file not found: '"$1"
	[ -r "$1" ] || die 'could not read file: '"$1"
	[ -s "$1" ] || error 'warning! file is empty: '"$1"
	return 0
}

while getopts f:r:bnqhV-t opt; do
	case $opt in
		f)
			input="${OPTARG}"
			check_file $input
			;;

		r)
			if ([ $OPTARG -ge 0 ] && [ $OPTARG -le 255 ]) 2>/dev/null
			then
				rate=$OPTARG
			else
				error "rate must be between 0 and 255, $OPTARG given"
				error "continuing with rate = 4"
				rate=4
			fi
			;;

		b)
			rainbow_mode=48 #background
			;;
		n)
			function reset_colour_counter {}
			;;
		q)
			function error {}
			;;
		h)  #'cool program title' just says 'rainbows \v by \v @reptar-xl', in rainbows
			# i mean i could just do like `echo 'rainbows by @reptar-xl | $0` but i don't trust it,
			# i can see that having problems on other's computers
			cool_program_title=$'\033[38;2;255;0;0mr\033[38;2;255;23;0ma\033[38;2;255;47;0mi'
			cool_program_title+=$'\033[38;2;255;71;0mn\033[38;2;255;94;0mb\033[38;2;255;118;0mo'
			cool_program_title+=$'\033[38;2;255;142;0mw\v\033[38;2;255;189;0mb\033[38;2;255;213;0my'
			cool_program_title+=$'\v\033[38;2;250;255;0m@\033[38;2;226;255;0mr\033[38;2;202;255;0me'
			cool_program_title+=$'\033[38;2;178;255;0mp\033[38;2;155;255;0mt\033[38;2;131;255;0ma'
			cool_program_title+=$'\033[38;2;107;255;0mr\033[38;2;84;255;0m_\033[38;2;60;255;0mx'
			cool_program_title+=$'\033[38;2;36;255;0ml\033[m'	
			{ sed 's/^\t*//'; exit 0 } << EOF
			${cool_program_title:---> rainbow by @reptar_xl <--}
			Usage: $0 [OPTIONS]...
			Make text all rainbowy.
			If -f is not given, read from stdin.

			    -f <file>   Read from file instead of stdin
			    -r <rate>   Rate that it cycles through colours (from 0 to 255, default 4)
			    -b          Background colour mode (default is foreground) (warning: shitty)
			    -n          Don’t reset colour on newlines
			    -q          Hide error messages
			    -h          You know what this does (displays this help text)
			    -v          Does nothing (in case you assumed it meant verbose, which is default)
			    -V          Display license & version info
			    -t          Tests your terminal’s colour capability

			Examples:
			    rainbow < /etc/passwd
			    dmesg | rainbow -r1
			    rainbow -f /etc/resolv.conf -r 12
			    dd if=/dev/sda | rainbow | dd of=/dev/sda (NO DON’T)
EOF
			;;
		V)
			{ sed 's/^\t*//'; exit 0 }  << EOF 
				rainbow v1.2
				Valentine’s Day, 14 feb 2016, 3:11 pm, still hungover slightly
				by Tom Shaddock <https://apricot.pictures>
				license: to kill
EOF
			exit 0
			;;
		t)
			rainbow-test
			;;
		-)
			# like -- to mean ‘end of options’
			break
			;;
	esac
done
# if the input file was not set using the flag -f, check the
# end of the args to see if there's a file... else, stdin

shift $(($OPTIND-1)) #so that the unparsed args are like $1 $2 etc etc

if ([ "$input"="" ] && [ "$1" ]); then
	input=${1// */} #remove everything after a space — i'm not clever enough
					#for multiple files just yet
	check_file ${input}
fi

input=${input:-/dev/stdin}       # if no file is set, then read from stdin
rainbow_mode=${rainbow_mode:-38} #38 = fg, 48 = bg
rate=${rate:-4}                  #rate=4 if the -r flag was not passed
integer min=$[   0 + $rate ]     #maximum colour number
integer max=$[ 255 - $rate ]     #minimum colour number
integer colour=0                 #0 to start off with
integer colourdirection=0        #0 = increment, 1 = decrement

# main loop, we’re looping over each line here
while read -ru0 line; do
	main_char_loop <<< "${line}"
	reset_colour_counter #unless -n was passed
done < "$input"
printf -- $'\033[m'
exit 0
