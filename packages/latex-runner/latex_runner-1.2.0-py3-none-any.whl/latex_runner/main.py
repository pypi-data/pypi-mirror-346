#!./runmodule.sh

import os
import sys
import shutil
import argparse
import subprocess
import glob
import enum
from collections.abc import Iterator
from typing import IO


from confattr import Config, DictConfig, Message, NotificationLevel
from confattr.quickstart import ConfigManager
from confattr.formatters import List, Primitive
from confattr.types import Regex, SubprocessCommandWithAlternatives as Command

from .about import APP_NAME, __version__, __doc__
from .config_types import Color, color_none


# ========== App ==========

class App:

	pdf_viewer = Config("pdf-viewer", Command(f'rifle {Command.WC_FILE_NAME} || xdg-open {Command.WC_FILE_NAME}'), help="The program used to open a pdf file.")

	def __init__(self, config_manager: ConfigManager) -> None:
		self.cfg = config_manager
		self.ui_notifier = self.cfg.ui_notifier
		self.cfg.load()

	def main(self, filename: 'str|None', options: 'list[str]', build_pdf: bool = False, open_pdf: bool = False, get_pdf: bool = False, get_log: bool = False, get_root: bool = False, get_root_dir: bool = False, max_runs: 'int|None' = None) -> None:
		if not open_pdf and not get_pdf and not get_log and not get_root and not get_root_dir:
			build_pdf = True

		self.cfg.set_ui_callback(self.show_message)
		latex = LatexWrapper(filename, options, max_runs=max_runs)
		if build_pdf:
			latex.compile()
		if get_pdf:
			print(os.path.abspath(latex.get_pdf()))
		if get_log:
			print(os.path.abspath(latex.get_log()))
		if get_root:
			print(os.path.abspath(latex.get_root()))
		if get_root_dir:
			print(os.path.abspath(os.path.dirname(latex.get_root())))
		if open_pdf:
			self.pdf_viewer.replace(Command.WC_FILE_NAME, os.path.abspath(latex.get_pdf())).run(context=None)


	def show_message(self, msg: Message) -> None:
		if msg.notification_level is NotificationLevel.ERROR:
			color = LatexWrapper.color.get(LatexWrapper.MODE.ERROR, color_none)
		else:  # pragma: no cover
			color = color_none
		color.print(msg, file=sys.stderr)


class LatexWrapper:

	EXIT_CODE_NO_FILE = 1
	EXIT_CODE_MULTIPLE_FILES = 1
	EXIT_CODE_INVALID_PATH = 1
	EXIT_CODE_UNKNOWN_PROGRAM = 2

	# ------- encodings -------

	file_encoding = Config('encoding.file', "utf8", help="The encoding of the LaTeX file. This encoding is used for reading magic comments.")

	tex_encoding = Config('encoding.tex-program', {
		#https://stackoverflow.com/questions/56734934/unicodedecodeerror-with-0xc3-in-python-subprocess-stdout-in-macos/56735278#comment100033782_56735278
		"pdflatex" : "ISO-8859-2",
	}, help="The encoding of the output of the TeX program written to stdout, e.g. errors, warnings, etc.")
	tex_encoding_default = Config('encoding.tex-program-default', "utf8", help="The encoding to use if %encoding.tex-program% does not contain a value for the current TeX program.")


	# ------- output -------

	class MODE(enum.Enum):
		NORMAL  = 0
		ERROR   = 1
		WARNING = 2
		BOX     = 3
		TRACING = 4
		SHOW    = 5
		PROMPT  = 6

	# positive numbers: number of lines
	# negative numbers: number of paragraphs
	number_context_lines = DictConfig('context-lines', {
		MODE.ERROR   : -2,
		MODE.WARNING : -1,
		MODE.BOX     :  2,
		MODE.SHOW    : -1,
		MODE.PROMPT  : -1,
	}, unit='', help="The number of lines to be printed after a regex has matched. Positive numbers count lines, negative numbers count paragraphs.")

	color = DictConfig('color', {
		MODE.ERROR   : Color('red'),
		MODE.WARNING : Color('yellow'),
		MODE.BOX     : Color('blue'),
		MODE.TRACING : Color('green'),
		MODE.SHOW    : Color('green'),
		MODE.PROMPT  : Color('cyan'),
	})

	reo_mode = DictConfig('regex', {
		MODE.ERROR   : Regex(r"^!"),
		MODE.WARNING : Regex(r"(?i)^[^#].*[^\\]\bWarning\b.*:"),
		MODE.BOX     : Regex(r"full .*box"),
		MODE.SHOW    : Regex(r"^> "),
		MODE.PROMPT  : Regex(r"\? $"),
	}, help="The regular expressions used to detect interesting information printed to stdout.")

	reo_mode_tracing_start = Config('regex.tracing.start', Regex(r"(?i)tracing[A-Za-z]*\s*=?\s*1"), help="First line of tracing output.")
	reo_mode_tracing_end   = Config('regex.tracing.stop',  Regex(r"(?i)tracing[A-Za-z]*\s*=?\s*0"), help="Last line of tracing output.")

	hide = Config('hide', [], type=List(Primitive(MODE)), help="Do not print these types of messages.")
	hide_context = Config('hide-context', [], type=List(Primitive(MODE)), help="Do not print context lines for these types of messages.")


	# ------- magic comments -------

	program = Config('tex-program', "pdflatex", help="The default program used to build the file if there is no magic comment `% !TeX program = pdflatex` in the file.")

	reo_magic_comment_root = Config('magic-comment.root', Regex(r"^%\s*!TeX root\s*=\s*(?P<root>.+)"), help="The regular expression used to detect the magic comment specifying the main TeX file to be built.")
	reo_magic_comment_program = Config('magic-comment.program', Regex(r"^%\s*!TeX program\s*=\s*(?P<program>\S+)"), help="The regular expression used to detect the magic comment specifying the TeX program to be used.")
	reo_magic_comment_option = Config('magic-comment.option', Regex(r"^%\s*!TeX option\s*=\s*(?P<option>\S+)"), help="The regular expression used to detect the magic comment specifying the options to be passed to the TeX program (one option per line, this comment can be used several times).")
	reo_magic_comment_jobname = Config('magic-comment.jobname', Regex(r"^%\s*!TeX jobname\s*=\s*(?P<jobname>\S+)"), help="The regular expression used to detect the magic comment specifying the jobname (one pattern per line but this comment can be used several times to aggregate several jobnames).")
	reo_magic_comment_new_jobname = Config('magic-comment.jobname-new', Regex(r"^%\s*!TeX new jobname\s*=\s*(?P<jobname>\S+)"), help="The regular expression used to detect the magic comment specifying the jobname(s), clearing all previously encountered jobnames.")

	allowed_programs = Config('allowed-tex-programs', ["pdflatex", "xelatex", "lualatex", "latex", "tex", "pdftex"], help="The TeX programs which are allowed to be set in magic comments. For security reasons other programs set in a magic comment will not be executed.")
	allowed_options = Config('allowed-tex-options', ["--shell-escape", "--8bit",
		"--interaction=batchmode", "--interaction=nonstopmode", "--interaction=scrollmode", "--interaction=errorstopmode"],
		help="The options which can be enabled in magic comments. For security reasons other options set in magic comments will not be passed to the TeX program. All options in this list must start with --. They apply to the synonymous options with only one - as well.")
	default_options = Config('default-tex-options', [], type=List(Primitive(str)), help="Options which are passed by default.")


	# ------- biber and makeglossaries -------

	reo_rerun_biber = Config('rerun.biber', Regex(r"(?i).*Please \(re\)run biber on the file"), help="If a warning matches this regular expression biber is run after the build.")
	reo_bibtex_file = Config('bibtex.file-name', Regex(r"\(biblatex\)\s+(?P<fn>[A-Za-z0-9_-]+)$"), help="The regex to get the name of the .bib file from the line after %rerun.biber%.")

	reo_rerun_makeglossaries = Config('rerun.makeglossaries', Regex(r"(?i).*\(dest\): name\{glo:.*"), help="If a warning matches this regular expression makeglossaries is run after the build.")
	# reo_rerun_warning is probably pretty useless since I am checking the aux file but it may be useful if someone uses \include instead of \input
	reo_rerun_warning = Config('rerun.tex', Regex(r".*rerun"), help=r"If a warning matches this regular expression or if the root aux file has changed the TeX program is run again after the build up to %max-runs% times. Changes to the aux file should cover most necessary reruns but if you are using \include instead of \input the root aux file check might fail. Please note that LaTeX does not give a rerun warning if the \tableofcontents changes. Reruns are not performed if a prompt or tracing output is detected.")

	max_runs = Config("max-runs", 1, unit="", help="The maximum number of builds. If this is greater than 1 automatically rerun LaTeX if the root aux file has changed or if %rerun.tex% has matched. Reruns are not performed if a prompt or tracing output is detected.")


	# ------- init -------

	def __init__(self, filename: 'str|None', options: 'list[str]', max_runs: 'int|None' = None) -> None:
		self.waiting_for_bibtex_file = False
		if max_runs is not None:
			self.max_runs = max_runs
		self.run_counter = 0

		if filename is None:
			filename = self.find_tex_file('.')
		else:
			filename = self.add_extension_if_necessary(filename)
		if not os.path.exists(filename):
			self.print_error("no such file: %s" % filename)
			sys.exit(self.EXIT_CODE_INVALID_PATH)
		self.mainfilename = filename
		self.options = list(self.default_options)
		self.jobnames: 'list[str]' = []
		self.find_program_and_options(filename)
		if self.is_empty(self.mainfilename):
			# Trying to run LaTeX/TeX would drop the user to an invisible prompt
			# where they would be expected to insert LaTeX/TeX code
			# (e.g. \end{document}/\bye to quit).
			# Making the prompt visible would be difficult because it consists of a single *
			# and so trying to detect the prompt would have false positives.
			# But I don't think a user would want to get to the prompt, anyway.
			# So let's exit with an error message.
			self.print_error("the file is empty: %s" % self.mainfilename)
			sys.exit(self.EXIT_CODE_INVALID_PATH)
		self.options += options

		path, self.mainfilename = os.path.split(self.mainfilename)
		path = os.path.normpath(path)
		if path != '.':
			print("cd %s" % path, file=sys.stderr)
			os.chdir(path)

	def reset(self) -> None:
		self.run_counter += 1

		# biber
		self.bibtex_file: 'str|None' = None

		# makeglossaries
		self.rerun_makeglossaries = False

	def find_tex_file(self, path: str) -> str:
		filenames = [fn for fn in os.listdir(path) if fn.lower().endswith('.tex')]
		if len(filenames) == 1:
			if path == '.':
				return filenames[0]
			return os.path.join(path, filenames[0])
		if filenames:
			filenames.sort()
			root_filenames = []
			for fn in filenames:
				if path != '.':
					fn = os.path.join(path, fn)
				mainfilename = self.find_root_file(fn)
				if mainfilename not in root_filenames:
					root_filenames.append(mainfilename)
					if len(root_filenames) > 1:
						self.print_error("multiple tex files found in %r:" % os.path.abspath(path))
						for fn in filenames:
							self.print_error_line("- %s" % fn)
						self.print_error_line("pointing to different root files:")
						for fn in root_filenames:
							if os.path.isfile(fn):
								self.print_error_line("- %s" % fn)
							else:
								self.print_error_line("- %s  (does not exist)" % fn)
						self.print_error_line("please pass the file you want to build as command line argument")
						sys.exit(self.EXIT_CODE_MULTIPLE_FILES)

			return root_filenames[0]

		self.print_error("no tex file found in %r" % os.path.abspath(path))
		sys.exit(self.EXIT_CODE_NO_FILE)


	def add_extension_if_necessary(self, filename: str) -> str:
		if os.path.isfile(filename):
			return filename
		elif os.path.isdir(filename):
			return self.find_tex_file(filename)
		elif filename.endswith(os.path.extsep):
			return filename + 'tex'
		elif not filename.lower().endswith('.tex'):
			return filename + '.tex'

		return filename

	def iter_magic_comment_lines(self, fn: str) -> 'Iterator[str]':
		with open(fn, "rt", encoding=self.file_encoding) as f:
			for ln in f:
				ln = ln.strip()
				if ln and ln[0] != '%':
					break
				yield ln

	def is_empty(self, fn: str) -> bool:
		with open(fn, "rt", encoding=self.file_encoding) as f:
			for ln in f:
				ln = ln.strip()
				if ln and ln[0] != '%':
					return False
		return True

	def find_root_file(self, fn: str) -> str:
		if not os.path.exists(fn):
			return fn
		for ln in self.iter_magic_comment_lines(fn):
			m = self.reo_magic_comment_root.search(ln)
			if m:
				root = m.group("root")
				return self.find_root_file(os.path.join(os.path.dirname(fn), root))

		return fn

	def find_program_and_options(self, fn: str) -> None:
		for ln in self.iter_magic_comment_lines(fn):
			m = self.reo_magic_comment_program.search(ln)
			if m:
				program = m.group("program")
				if not self.is_allowed_program(program):
					self.print_error("%r is not a program I know, I am not running it for security reasons." % program)
					self.print_error_line("Please edit the magic comment in %s" % fn)
					self.print_error_line("or run `latex-runner --edit-config` and add %s to allowed-tex-programs." % program)
					sys.exit(self.EXIT_CODE_UNKNOWN_PROGRAM)

				self.program = program
				continue

			m = self.reo_magic_comment_option.search(ln)
			if m:
				option = m.group("option")
				if not self.is_allowed_option(option):
					if option.startswith('--'):
						option_with_double_dash = option
					else:
						option_with_double_dash = '-' + option
					self.print_error("%s is not a tex option which I know is safe to use, I am ignoring it for security reasons." % option)
					self.print_error_line("Please edit the magic comment in %s" % fn)
					self.print_error_line("or run `latex-runner --edit-config` and add %s to allowed-tex-options." % option_with_double_dash)
					continue

				self.options.append(option)
				continue

			m = self.reo_magic_comment_root.search(ln)
			if m:
				root = m.group("root")
				self.mainfilename = os.path.join(os.path.dirname(fn), root)
				self.find_program_and_options(self.mainfilename)
				continue

			m = self.reo_magic_comment_jobname.search(ln)
			if m:
				jobname = m.group("jobname")
				self.jobnames.extend(self.expand_jobnames(fn, jobname))
				continue

			m = self.reo_magic_comment_new_jobname.search(ln)
			if m:
				jobname = m.group("jobname")
				self.jobnames.clear()
				self.jobnames.extend(self.expand_jobnames(fn, jobname))
				continue

	def expand_jobnames(self, fn: str, jobname: str) -> 'list[str]':
		if jobname == '%':
			jobname = os.path.split(fn)[1]
		rootdir = os.path.split(fn)[0]
		if ':' in jobname:
			path, jobname = jobname.split(':')
			path = os.path.join(rootdir, path)
		else:
			path = rootdir
		out = glob.glob(jobname, root_dir=path)
		out.sort()
		if out:
			return [os.path.splitext(fn)[0] for fn in out]
		else:
			return [jobname]

	def is_allowed_program(self, name: str) -> bool:
		return name in self.allowed_programs

	def is_allowed_option(self, name: str) -> bool:
		if not name.startswith("--"):
			name = "-" + name
		return name in self.allowed_options


	# ------- getter -------

	def get_root(self) -> str:
		return self.mainfilename

	def get_pdf(self) -> str:
		if self.jobnames:
			return os.path.join(os.path.split(self.mainfilename)[0], self.jobnames[0] + os.extsep + 'pdf')
		return os.path.splitext(self.mainfilename)[0] + os.extsep + 'pdf'

	def get_log(self) -> str:
		return os.path.splitext(self.get_pdf())[0] + os.extsep + 'log'


	# ------- compile -------

	def compile(self) -> None:
		if self.jobnames:
			options = list(self.options)
			for jobname in self.jobnames:
				self.options = options + ['-jobname=' + jobname]
				self.compile_once()
		else:
			self.compile_once()

	def compile_once(self) -> None:
		self.cmd = [self.program] + self.options + [self.mainfilename]
		print("running: %s" % " ".join(self.cmd), file=sys.stderr)
		self.reset()
		needs_rerun = False
		dont_rerun = False

		aux_file = os.path.splitext(self.mainfilename)[0] + ".aux"
		if os.path.isfile(aux_file):
			with open(aux_file, 'rb') as f:
				old_aux = f.read()
		else:
			old_aux = b''

		encoding = self.tex_encoding.get(self.program, self.tex_encoding_default)
		p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, encoding=encoding)

		current_mode = self.MODE.NORMAL
		prev_mode = current_mode
		line_counter = 0

		assert p.stdout is not None
		for ln in self.read_lines_from_stream(p.stdout):
			if self.reo_mode_tracing_start.search(ln):
				#note that TeX usually does not write tracing to stdout
				#if you want that, set \tracingonline=1
				#although that may produce way too much output
				#and if you call this wrapper from vim you can't scroll up
				current_mode = self.MODE.TRACING
				prev_mode = self.MODE.TRACING
				dont_rerun = True
				self.print_first(current_mode, ln)
				continue
			elif current_mode == self.MODE.TRACING:
				#TODO: I believe errors would not be highlighted appropriately in tracing mode
				self.print_cont(current_mode, ln)
				if self.reo_mode_tracing_end.search(ln):
					current_mode = self.MODE.NORMAL
					prev_mode = self.MODE.NORMAL
				continue

			for mode, reo in self.reo_mode.items():
				if reo.search(ln):
					current_mode = mode
					line_counter = 0
					self.print_first(mode, ln)
					if current_mode is self.MODE.WARNING and self.reo_rerun_warning.match(ln):
						needs_rerun = True
					elif current_mode is self.MODE.PROMPT:
						dont_rerun = True
					break
			else:
				if current_mode != self.MODE.NORMAL:
					n = self.number_context_lines[current_mode]

					if n < 0:
						if not ln or ln.isspace():
							line_counter += 1
							if line_counter >= -n:
								self.print_sep(current_mode)
								current_mode = prev_mode
								continue
					else:
						line_counter += 1
						if line_counter > n:
							self.print_sep(current_mode)
							current_mode = prev_mode
							continue

					self.print_cont(current_mode, ln)

		p.wait()

		if os.path.isfile(aux_file):
			with open(aux_file, 'rb') as f:
				new_aux = f.read()
		else:
			new_aux = b''

		if new_aux != old_aux:
			self.print_first(self.MODE.NORMAL, "aux file has changed")
			needs_rerun = True

		if self.bibtex_file:
			cmd = ["biber", self.bibtex_file]
			self.print_first(self.MODE.WARNING, "running `%s`" % " ".join(cmd))
			p_biber = subprocess.run(cmd, stdout=sys.stderr)
			if p_biber.returncode != 0:
				dont_rerun = True
			needs_rerun = True

		if self.rerun_makeglossaries:
			cmd = ["makeglossaries", os.path.splitext(self.mainfilename)[0]]
			self.print_first(self.MODE.WARNING, "running `%s`" % " ".join(cmd))
			subprocess.run(cmd, stdout=sys.stderr)
			needs_rerun = True

		if needs_rerun and not dont_rerun:
			if self.run_counter < self.max_runs:
				self.print_first(self.MODE.NORMAL, "========== rerun %s ==========" % self.run_counter)
				self.compile()
				return

		if p.returncode:
			exit(p.returncode)

	def read_lines_from_stream(self, stream: 'IO[str]') -> 'Iterator[str]':
		ln: 'list[str]' = []
		asking_for_input = list("? ")
		while True:
			c = stream.read(1)

			if not c:
				yield "".join(ln)
				return

			if c == "\n":
				yield "".join(ln)
				ln = []
				continue

			ln.append(c)

			if ln == asking_for_input:
				yield "".join(ln)
				ln = []
				continue

	def print_first(self, mode: MODE, ln: str) -> None:
		if mode in self.hide:
			return
		color = self.color.get(mode, color_none)

		if mode == self.MODE.PROMPT:
			end = ""
		else:
			end = None

		color.print(ln, end=end, flush=True, file=sys.stderr)

		if mode == self.MODE.WARNING and self.reo_rerun_biber.match(ln):
			self.waiting_for_bibtex_file = True
		if mode == self.MODE.WARNING and self.reo_rerun_makeglossaries.match(ln):
			self.rerun_makeglossaries = True

	def print_cont(self, mode: MODE, ln: str) -> None:
		if mode in self.hide or mode in self.hide_context:
			return
		print(ln, file=sys.stderr)

		if self.waiting_for_bibtex_file:
			self.waiting_for_bibtex_file = False
			m = self.reo_bibtex_file.match(ln)
			if not m:  # pragma: no cover
				self.print_error(r"expected the name of the bibtex file but got %r" % ln)
			else:
				self.bibtex_file = m.group("fn")

	def print_sep(self, mode: MODE) -> None:
		if mode in self.hide or mode in self.hide_context:
			return
		print("", file=sys.stderr)


	# wrapper for convenience

	def print_error(self, msg: str) -> None:
		self.print_first(self.MODE.ERROR, msg)

	def print_error_line(self, msg: str) -> None:
		self.print_cont(self.MODE.ERROR, msg)


# ========== clear ==========

def clear(path: 'str|None') -> None:
	if not path:
		path = '.'

	if not os.path.isdir(path):
		prefix = os.path.splitext(path)[0] + os.path.extsep
		path  = os.path.split(path)[0]
		if not path:
			path = '.'
		elif not os.path.isdir(path):
			print_error("No such directory: %s" % path)
			sys.exit(LatexWrapper.EXIT_CODE_INVALID_PATH)
	else:
		prefix = ''

	root = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=path, text=True, stdout=subprocess.PIPE).stdout.rstrip('\n')
	cmd = ['git', 'status', '--porcelain', '--ignored', '-z']
	p = subprocess.run(cmd, cwd=path, text=True, stdout=subprocess.PIPE)
	IGNORED = '!! '
	N = len(IGNORED)
	if os.path.isabs(path):
		def fmtpath(path: str) -> str:
			return os.path.join(root, path)
	else:
		def fmtpath(path: str) -> str:
			return os.path.relpath(os.path.join(root, path))
	files_to_be_deleted = [fmtpath(ln[N:]) for ln in p.stdout.split('\0') if ln.startswith(IGNORED) and not ln.lower().endswith('.pdf')]
	if prefix:
		prefix = fmtpath(os.path.relpath(prefix, root))
		files_to_be_deleted = [fn for fn in files_to_be_deleted if fn.startswith(prefix)]

	if files_to_be_deleted:
		print("The following files/directories will be deleted:", file=sys.stderr)
		for fn in sorted(files_to_be_deleted):
			if os.path.isdir(fn):
				print("- %s%s*" % (fn.rstrip(os.path.sep), os.path.sep), file=sys.stderr)
			else:
				print("- %s" % fn, file=sys.stderr)
		if read_yes_no("Do you want to continue?"):
			for fn in files_to_be_deleted:
				if os.path.isdir(fn):
					try:
						shutil.rmtree(fn)
					except:  # pragma: no cover
						print("Failed to remove directory %s" % fn, file=sys.stderr)
				else:
					try:
						os.remove(fn)
					except:  # pragma: no cover
						print("Failed to remove file %s" % fn, file=sys.stderr)
	else:
		print("There are no files to be deleted.", file=sys.stderr)

def read_yes_no(prompt: str) -> bool:
	prompt += " [Yn] "
	while True:
		print(prompt, file=sys.stderr, end='')
		inp = input()
		inp = inp.strip().lower()
		if not inp:
			return True
		elif inp == "y":
			return True
		elif inp == "n":
			return False
		print("Invalid input %r. Should be either y for yes or n for no." % inp, file=sys.stderr)

def print_error(ln: str) -> None:
		color = LatexWrapper.color.get(LatexWrapper.MODE.ERROR, color_none)
		color.print(ln, flush=True, file=sys.stderr)


# ========== start app ==========

class PassThroughAction(argparse.Action):

	def __init__(self, option_strings: 'list[str]', dest: str, help: 'str|None' = None, arg: 'str|None' = None) -> None:
		nargs = None if arg else 0
		option_strings.append('-' + option_strings[0])
		argparse.Action.__init__(self, option_strings, dest='options', nargs=nargs, metavar=arg, help=help)

	def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: object, option_string: 'str|None' = None) -> None:
		assert option_string is not None
		if values == []:
			namespace.options.append(option_string)
		else:
			namespace.options.append("%s=%s" % (option_string, values))


def main(largs: 'list[str]|None' = None) -> None:
	cfg = ConfigManager(APP_NAME, __version__, __doc__)
	p = cfg.create_argument_parser()
	p.add_argument('path', nargs='?', help="the tex file to build or the directory where it is located (default: current working directory)")
	p.add_argument('-n', type=int, default=None, help="max number of builds, if this is greater than 1 automatically rerun LaTeX if a rerun warning was printed")
	p.add_argument('-b', '--build-pdf', action='store_true', help="build the pdf file, this is assumed if none of --open-pdf and --get-* are passed")
	p.add_argument('-o', '--open-pdf', action='store_true', help="open the pdf file")
	p.add_argument('--get-pdf', action='store_true', help="print the absolute path of the pdf file to stdout")
	p.add_argument('--get-log', action='store_true', help="print the absolute path of the log file to stdout")
	p.add_argument('--get-root', action='store_true', help="print the absolute path of the root file to stdout")
	p.add_argument('--get-root-dir', action='store_true', help="print the absolute path of the directory where the root file is located")
	p.add_argument('-O', '--option', dest='options', action='append', default=[], help="additional command line options to be passed to the TeX program, you must not leave a space in between otherwise the option will not be recognized as argument to this option, e.g. -o=-synctex=1")
	p.add_argument('--clear', action='store_true', help="delete all ignored files in the current git repository or only those with the same base name if a path is given")

	pass_through_group = p.add_argument_group('pass through', description="The following options are passed through to the TeX program.")
	def add_pass_through_option(*opt: str, arg: 'str|None' = None) -> None:
		pass_through_group.add_argument(*opt, action=PassThroughAction, arg=arg)
	add_pass_through_option('-8bit')
	add_pass_through_option('-synctex', arg="NUMBER")
	add_pass_through_option('-shell-escape')
	add_pass_through_option('-no-shell-escape')
	add_pass_through_option('-shell-restricted')
	add_pass_through_option('-interaction', arg="MODE")
	add_pass_through_option('-jobname', arg="NAME")

	args = p.parse_args(largs)
	if args.clear:
		clear(args.path)
		return

	app = App(cfg)
	app.main(args.path, args.options,
		build_pdf = args.build_pdf,
		open_pdf = args.open_pdf,
		get_pdf = args.get_pdf,
		get_log = args.get_log,
		get_root = args.get_root,
		get_root_dir = args.get_root_dir,
		max_runs = args.n,
	)
