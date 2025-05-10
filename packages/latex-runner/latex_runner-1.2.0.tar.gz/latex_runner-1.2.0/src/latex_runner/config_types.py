#!/usr/bin/env python3

import typing

from colorama import Fore, Style, just_fix_windows_console
just_fix_windows_console()

class Color:

	color_codes = {
		'red'    : Fore.RED,
		'green'  : Fore.GREEN,
		'yellow' : Fore.YELLOW,
		'blue'   : Fore.BLUE,
		'magenta': Fore.MAGENTA,
		'cyan'   : Fore.CYAN,
		'reset'  : Style.RESET_ALL,
		'none'   : '',
	}

	type_name = 'color'
	help = 'one of %s' % ', '.join(color_codes.keys())

	def __init__(self, name: str) -> None:
		self.name = name
		self.code = self.color_codes[name]

	def __str__(self) -> str:
		return self.name

	def __repr__(self) -> str:
		return f'{type(self).__name__}({self.name!r})'


	def print(self, *l: object, sep: 'str|None' = None, end: 'str|None' = None, flush: bool = False, file: 'typing.TextIO|None' = None) -> None:
		print(self.code, end='', file=file)
		print(*l, sep=sep, end='', file=file)
		print(self.color_codes['reset'], end=end, flush=flush, file=file)

color_none = Color('none')
