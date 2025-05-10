#!../venv/bin/pytest

import os
import re
import io
import sys
import subprocess
import tempfile
from pathlib import Path
from collections.abc import Sequence, Iterator

import pytest
from confattr import ConfigFile
from confattr.types import SubprocessCommand

from latex_runner.main import main
from latex_runner.about import APP_NAME, __version__


# ------- utils -------

mkdir = os.mkdir
def mkfile(fn: 'str|Path', *, content: 'str|None' = None) -> None:
	if content is None:
		content = str(fn)
	with open(fn, 'wt') as f:
		f.write(content)

def lsfiles(path: 'str|Path') -> 'list[str]':
	out: 'list[str]' = []
	for fn in os.listdir(path):
		ffn = os.path.join(path, fn)
		if fn != '.git' and os.path.isdir(ffn):
			out.extend(fn + '/' + fni for fni in lsfiles(ffn))
		else:
			out.append(fn)
	return out


@pytest.fixture(autouse=True)
def reset_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> 'Iterator[None]':
	# make sure no user config file is used
	monkeypatch.setenv('LATEX_RUNNER_CONFIG_DIRECTORY', str(tmp_path))

	# reset all settings after each test because magic comments change the settings
	cf = ConfigFile(appname=APP_NAME)
	cf.set_ui_callback(throw_errors)
	cf.save(comments=False)
	yield
	cf.load(env=False)

def throw_errors(msg: object) -> None:
	raise Exception(msg)

def tex_to_pdf(fn: str) -> str:
	return fn.rsplit(os.path.extsep, 1)[0] + '.pdf'

reo_color = re.compile('.*?m')
def strip_color(ln: str) -> str:
	return reo_color.sub('', ln)

class Colored:

	def __init__(self, ln: str) -> None:
		self.ln = ln

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, str):
			return False
		return strip_color(other) == self.ln

	def __repr__(self) -> str:
		return '%s(%r)' % (type(self).__name__, self.ln)

class RunMock:

	def __init__(self) -> None:
		self.calls: 'list[list[str]]' = []

	def __call__(self, cmd: 'Sequence[str]', **kw: object) -> None:
		self.calls.append(list(cmd))


# ------- tests -------

def test_main_module(tmp_path: Path, monkeypatch: 'pytest.MonkeyPatch') -> None:
	monkeypatch.chdir(tmp_path)
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	p = subprocess.run(['latex-runner'], capture_output=True, text=True)
	assert p.stdout == ""
	assert os.path.isfile(fn_pdf)

	lines = p.stderr.splitlines()
	assert lines[0] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert lines[1] == Colored("aux file has changed")
	assert len(lines) == 2

def test_default(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_add_extension_without_extsep(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_input = str(tmp_path / 'test.')
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main([fn_input])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_add_extsep_and_extension(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_input = str(tmp_path / 'test')
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main([fn_input])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_find_tex_file_in_directory(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main([str(tmp_path)])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0] == "cd %s" % tmp_path
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_find_tex_file_several_files_same_root(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	content_path = tmp_path / 'content'
	os.mkdir(content_path)
	fn_tex = str(tmp_path / 'main.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
\input{content/s1_intro}
\input{content/s2_main}
\input{content/s3_summary}
\end{document}
""")
	for i, name in enumerate(('intro', 'main', 'summary'), 1):
		with open(content_path / f's{i}_{name}.tex', 'wt') as f:
			f.write(r"""
% !TeX root = ../main.tex

\section{{name}}
""".replace('{name}', name.title()))
	main([str(content_path)])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0] == "cd %s" % tmp_path
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_find_tex_file_no_args(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.chdir(tmp_path)
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main([])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert lines[1] == Colored("aux file has changed")
	assert len(lines) == 2

def test_magic_comment_root(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	os.mkdir(tmp_path / 'content')
	fn_tex = str(tmp_path / 'content' / 'inner.tex')
	fn_pdf = str(tmp_path / 'test.pdf')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX root = ../test.tex
hello world
""")
	with open(tmp_path / 'test.tex', 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
\input{content/inner.tex}
\end{document}
""")
	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex test.tex"
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_comment_out_magic_comment(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = str(tmp_path / 'test.pdf')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
%% !TeX root = other-file.tex
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex test.tex"
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3


# ------- test getters -------

def test_get_pdf(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	os.mkdir(tmp_path / 'content')
	fn_tex = str(tmp_path / 'content' / 'inner.tex')
	fn_pdf = str(tmp_path / 'test.pdf')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX root = ../test.tex
hello world
""")
	with open(tmp_path / 'test.tex', 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
\input{content/inner.tex}
\end{document}
""")
	main(["--get-pdf", fn_tex])
	captured = capsys.readouterr()
	assert captured.out == fn_pdf + "\n"

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert len(lines) == 1

def test_get_pdf_with_jobname(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	os.mkdir(tmp_path / 'content')
	fn_tex = str(tmp_path / 'content' / 'inner.tex')
	fn_pdf = str(tmp_path / 'myjob.pdf')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX root = ../test.tex
hello world
""")
	with open(tmp_path / 'test.tex', 'wt') as f:
		f.write(r"""
% !TeX jobname = myjob
\documentclass{article}
\begin{document}
\input{content/inner.tex}
\end{document}
""")
	main(["--get-pdf", fn_tex])
	captured = capsys.readouterr()
	assert captured.out == fn_pdf + "\n"

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert len(lines) == 1

def test_get_log(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	os.mkdir(tmp_path / 'content')
	fn_tex = str(tmp_path / 'content' / 'inner.tex')
	fn_log = str(tmp_path / 'test.log')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX root = ../test.tex
hello world
""")
	with open(tmp_path / 'test.tex', 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
\input{content/inner.tex}
\end{document}
""")
	main(["--get-log", fn_tex])
	captured = capsys.readouterr()
	assert captured.out == fn_log + "\n"

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert len(lines) == 1

def test_get_log_with_jobname(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	os.mkdir(tmp_path / 'content')
	fn_tex = str(tmp_path / 'content' / 'inner.tex')
	fn_log = str(tmp_path / 'myjob.log')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX root = ../test.tex
hello world
""")
	with open(tmp_path / 'test.tex', 'wt') as f:
		f.write(r"""
% !TeX jobname = myjob
\documentclass{article}
\begin{document}
\input{content/inner.tex}
\end{document}
""")
	main(["--get-log", fn_tex])
	captured = capsys.readouterr()
	assert captured.out == fn_log + "\n"

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert len(lines) == 1

def test_get_root(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	os.mkdir(tmp_path / 'content')
	fn_tex = str(tmp_path / 'content' / 'inner.tex')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX root = ../test.tex
hello world
""")
	fn_root = str(tmp_path / 'test.tex')
	assert os.path.isabs(fn_root)
	with open(fn_root, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
\input{content/inner.tex}
\end{document}
""")
	main(["--get-root", fn_tex])
	captured = capsys.readouterr()
	assert captured.out == fn_root + "\n"

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert len(lines) == 1

def test_get_root_dir(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	os.mkdir(tmp_path / 'content')
	fn_tex = str(tmp_path / 'content' / 'inner.tex')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX root = ../test.tex
hello world
""")
	root_dir = str(tmp_path)
	with open(tmp_path / 'test.tex', 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
\input{content/inner.tex}
\end{document}
""")
	main(["--get-root-dir", fn_tex])
	captured = capsys.readouterr()
	assert captured.out == root_dir + "\n"

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert len(lines) == 1

def test_open_pdf(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: 'pytest.MonkeyPatch') -> None:
	runmock = RunMock()
	monkeypatch.setattr(SubprocessCommand, 'is_installed', lambda self: self.cmd[0] == 'xdg-open')
	monkeypatch.setattr(subprocess, 'run', runmock)
	os.mkdir(tmp_path / 'content')
	fn_tex = str(tmp_path / 'content' / 'inner.tex')
	fn_pdf = str(tmp_path / 'test.pdf')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX root = ../test.tex
hello world
""")
	with open(tmp_path / 'test.tex', 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
\input{content/inner.tex}
\end{document}
""")
	main(["--open-pdf", fn_tex])
	assert runmock.calls == [["xdg-open", fn_pdf]]
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert len(lines) == 1


# ------- test clear -------

def test_clear_other_directory(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: 'pytest.MonkeyPatch') -> None:
	subprocess.run(['git', 'init'], cwd=tmp_path)
	os.mkdir(tmp_path / 'sub')
	os.mkdir(tmp_path / 'ignored-dir')
	with open(tmp_path / '.gitignore', 'wt') as f:
		f.write('ignored*')
	with open(tmp_path / 'committed', 'wt') as f:
		f.write('committed')
	with open(tmp_path / 'changed', 'wt') as f:
		f.write('committed')
	# config is created by reset_config fixture
	subprocess.run(['git', 'add', '.gitignore', 'committed', 'changed', 'config'], cwd=tmp_path)
	subprocess.run(['git', 'commit', '-m', 'test commit'], cwd=tmp_path)
	with open(tmp_path / 'changed', 'wt') as f:
		f.write('changed')
	with open(tmp_path / 'added', 'wt') as f:
		f.write('added')
	with open(tmp_path / 'untracked', 'wt') as f:
		f.write('untracked')
	with open(tmp_path / 'sub' / 'untracked', 'wt') as f:
		f.write('sub/untracked')
	with open(tmp_path / 'ignored', 'wt') as f:
		f.write('ignored')
	with open(tmp_path / 'sub' / 'ignored', 'wt') as f:
		f.write('sub/ignored')
	with open(tmp_path / 'ignored-dir' / 'ignored-1', 'wt') as f:
		f.write('ignored-1')
	with open(tmp_path / 'ignored-dir' / 'ignored-2', 'wt') as f:
		f.write('ignored-2')
	subprocess.run(['git', 'add', 'added'], cwd=tmp_path)

	ls_expected_before = {'.git', '.gitignore', 'committed', 'changed', 'added', 'untracked', 'config', 'sub', 'ignored', 'ignored-dir'}
	ls_expected_after  = {'.git', '.gitignore', 'committed', 'changed', 'added', 'untracked', 'config', 'sub'}
	assert set(os.listdir(tmp_path)) == ls_expected_before

	monkeypatch.setattr('sys.stdin', io.StringIO('y'))
	main(['--clear', str(tmp_path)])

	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0].startswith("The following files/directories will be deleted:")
	assert lines[1] == "- %s" % (tmp_path / 'ignored')
	assert lines[2] == "- %s" % (tmp_path / 'ignored-dir' / '*')
	assert lines[3] == "- %s" % (tmp_path / 'sub' / 'ignored')
	assert lines[4] == "Do you want to continue? [Yn] "
	assert len(lines) == 5

	assert set(os.listdir(tmp_path)) == ls_expected_after

	main(['--clear', str(tmp_path)])
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0] == "There are no files to be deleted."
	assert len(lines) == 1

def test_clear_no(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: 'pytest.MonkeyPatch') -> None:
	subprocess.run(['git', 'init'], cwd=tmp_path)
	with open(tmp_path / '.gitignore', 'wt') as f:
		f.write('ignored')
	with open(tmp_path / 'committed', 'wt') as f:
		f.write('committed')
	with open(tmp_path / 'changed', 'wt') as f:
		f.write('committed')
	# config is created by reset_config fixture
	subprocess.run(['git', 'add', '.gitignore', 'committed', 'changed', 'config'], cwd=tmp_path)
	subprocess.run(['git', 'commit', '-m', 'test commit'], cwd=tmp_path)
	with open(tmp_path / 'changed', 'wt') as f:
		f.write('changed')
	with open(tmp_path / 'added', 'wt') as f:
		f.write('added')
	with open(tmp_path / 'untracked', 'wt') as f:
		f.write('untracked')
	with open(tmp_path / 'ignored', 'wt') as f:
		f.write('ignored')
	subprocess.run(['git', 'add', 'added'], cwd=tmp_path)

	ls_expected_before = {'.git', '.gitignore', 'committed', 'changed', 'added', 'untracked', 'config', 'ignored'}
	ls_expected_after  = {'.git', '.gitignore', 'committed', 'changed', 'added', 'untracked', 'config'}
	assert set(os.listdir(tmp_path)) == ls_expected_before

	monkeypatch.setattr('sys.stdin', io.StringIO('x\nn'))
	main(['--clear', str(tmp_path)])

	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0].startswith("The following files/directories will be deleted:")
	assert lines[1] == "- %s" % (tmp_path / 'ignored')
	assert lines[2] == "Do you want to continue? [Yn] Invalid input 'x'. Should be either y for yes or n for no."
	assert lines[3] == "Do you want to continue? [Yn] "
	assert len(lines) == 4

	assert set(os.listdir(tmp_path)) == ls_expected_before

def test_clear_current_directory(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: 'pytest.MonkeyPatch') -> None:
	monkeypatch.chdir(tmp_path)
	subprocess.run(['git', 'init'])
	os.mkdir(tmp_path / 'sub')
	os.mkdir(tmp_path / 'ignored-dir')
	with open(tmp_path / '.gitignore', 'wt') as f:
		f.write('ignored*')
	with open(tmp_path / 'committed', 'wt') as f:
		f.write('committed')
	with open(tmp_path / 'changed', 'wt') as f:
		f.write('committed')
	# config is created by reset_config fixture
	subprocess.run(['git', 'add', '.gitignore', 'committed', 'changed', 'config'], cwd=tmp_path)
	subprocess.run(['git', 'commit', '-m', 'test commit'], cwd=tmp_path)
	with open(tmp_path / 'changed', 'wt') as f:
		f.write('changed')
	with open(tmp_path / 'added', 'wt') as f:
		f.write('added')
	with open(tmp_path / 'untracked', 'wt') as f:
		f.write('untracked')
	with open(tmp_path / 'sub' / 'untracked', 'wt') as f:
		f.write('sub/untracked')
	with open(tmp_path / 'ignored', 'wt') as f:
		f.write('ignored')
	with open(tmp_path / 'sub' / 'ignored', 'wt') as f:
		f.write('sub/ignored')
	with open(tmp_path / 'ignored-dir' / 'ignored-1', 'wt') as f:
		f.write('ignored-1')
	with open(tmp_path / 'ignored-dir' / 'ignored-2', 'wt') as f:
		f.write('ignored-2')
	subprocess.run(['git', 'add', 'added'])

	ls_expected_before = {'.git', '.gitignore', 'committed', 'changed', 'added', 'untracked', 'config', 'sub', 'ignored', 'ignored-dir'}
	ls_expected_after  = {'.git', '.gitignore', 'committed', 'changed', 'added', 'untracked', 'config', 'sub'}
	assert set(os.listdir(tmp_path)) == ls_expected_before

	monkeypatch.setattr('sys.stdin', io.StringIO('\n'))
	main(['--clear'])

	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0].startswith("The following files/directories will be deleted:")
	assert lines[1] == "- ignored"
	assert lines[2] == "- ignored-dir/*"
	assert lines[3] == "- sub/ignored"
	assert lines[4] == "Do you want to continue? [Yn] "
	assert len(lines) == 5

	assert set(os.listdir(tmp_path)) == ls_expected_after

def test_clear_related_files(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: 'pytest.MonkeyPatch') -> None:
	# ----- setup -----
	subprocess.run(['git', 'init'], cwd=tmp_path)
	mkfile(tmp_path / '.gitignore', content='*.log')

	mkdir (tmp_path / 'd1')
	mkfile(tmp_path / 'd1' / 'foo.tex')
	mkfile(tmp_path / 'd1' / 'foo.log')
	mkfile(tmp_path / 'd1' / 'foo2.tex')
	mkfile(tmp_path / 'd1' / 'foo2.log')
	mkdir (tmp_path / 'd2')
	mkfile(tmp_path / 'd2' / 'foo.tex')
	mkfile(tmp_path / 'd2' / 'foo.log')

	ls_expected_before = {'.git', '.gitignore', 'config', 'd1/foo.tex', 'd1/foo.log', 'd1/foo2.tex', 'd1/foo2.log', 'd2/foo.tex', 'd2/foo.log'}
	ls_expected_after = ls_expected_before - {'d1/foo.log'}
	assert set(lsfiles(tmp_path)) == ls_expected_before

	# ----- test 1 -----
	monkeypatch.setattr('sys.stdin', io.StringIO('y'))
	main(['--clear', str(tmp_path / 'd1' / 'foo.tex')])

	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0].startswith("The following files/directories will be deleted:")
	assert lines[1] == "- %s" % (tmp_path / 'd1' / 'foo.log')
	assert lines[2] == "Do you want to continue? [Yn] "
	assert len(lines) == 3

	assert set(lsfiles(tmp_path)) == ls_expected_after

	# ----- test 2 -----
	monkeypatch.setattr('sys.stdin', io.StringIO('y'))
	main(['--clear', str(tmp_path / 'd1' / 'foo.tex')])
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0] == "There are no files to be deleted."
	assert len(lines) == 1

	assert set(lsfiles(tmp_path)) == ls_expected_after

	# ----- test 3 -----
	ls_expected_before = ls_expected_after
	ls_expected_after = ls_expected_before - {'d1/foo2.log'}
	monkeypatch.setattr('sys.stdin', io.StringIO('y'))
	main(['--clear', str(tmp_path / 'd1' / 'foo2.')])

	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0].startswith("The following files/directories will be deleted:")
	assert lines[1] == "- %s" % (tmp_path / 'd1' / 'foo2.log')
	assert lines[2] == "Do you want to continue? [Yn] "
	assert len(lines) == 3

	assert set(lsfiles(tmp_path)) == ls_expected_after

	# ----- test 4 -----
	monkeypatch.chdir(tmp_path)

	ls_expected_before = ls_expected_after
	ls_expected_after = ls_expected_before
	monkeypatch.setattr('sys.stdin', io.StringIO('y'))
	main(['--clear', 'main.tex'])

	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0].startswith("There are no files to be deleted.")
	assert len(lines) == 1

	assert set(lsfiles(tmp_path)) == ls_expected_after

def test_clear_dont_crash_on_invalid_path(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: 'pytest.MonkeyPatch') -> None:
	monkeypatch.chdir(tmp_path)
	with pytest.raises(SystemExit):
		main(['--clear', str('not-existing' + os.path.sep + 'foo.tex')])

	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0] == Colored("No such directory: not-existing")
	assert len(lines) == 1


# ------- test magic comments program and option -------

def test_magic_comment_tex_program(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX program = xelatex
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: xelatex %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_magic_comment_tex_option(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX option = --interaction=errorstopmode
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex --interaction=errorstopmode %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3


# ------- test output -------

def test_overfull_box(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass[a5paper]{article}
\begin{document}
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
\end{document}
""")
	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert r"Overfull \hbox" in lines[2]
	assert lines[-1] == Colored("aux file has changed")

def test_hide_overfull_box(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: 'pytest.MonkeyPatch') -> None:
	monkeypatch.setenv('LATEX_RUNNER_HIDE', 'box')
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass[a5paper]{article}
\begin{document}
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
\ref{undefed}
\end{document}
""")
	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("LaTeX Warning: Reference `undefed' on page 1 undefined on input line 5.")
	for ln in lines[3:]:
		assert "box" not in ln

def test_hide_context_overfull_box(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: 'pytest.MonkeyPatch') -> None:
	monkeypatch.setenv('LATEX_RUNNER_HIDE_CONTEXT', 'box')
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass[a5paper]{article}
\begin{document}
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
\ref{undefed}
\end{document}
""")
	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("LaTeX Warning: Reference `undefed' on page 1 undefined on input line 5.")
	i = next(i for i in range(3,len(lines)) if r"Overfull \hbox" in lines[i])
	assert lines[i+1] == Colored("LaTeX Warning: There were undefined references.")

def test_warning_context_one_par(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass[ngerman]{article}
\usepackage[english,ngerman]{babel}
\begin{document}
\end{document}
""")
	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert not os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("Package babel Warning: Last declared language option is 'ngerman',")
	assert lines[3] == "(babel)                but the last processed one was 'english'."
	assert lines[4] == "(babel)                The main language can't be set as both a global"
	assert lines[5] == "(babel)                and a package option. Use 'main=ngerman' as"
	assert lines[6].startswith("(babel)                option. Reported on input line")
	assert lines[7] == ""
	assert lines[8] == Colored("aux file has changed")
	assert len(lines) == 9

def test_error(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\foo
""")
	with pytest.raises(SystemExit):
		main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert not os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert "Undefined control sequence" in lines[2]

def test_show(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}

\def\foo{hello world}
\show\foo

\begin{document}
\foo
\end{document}
""")
	with pytest.raises(SystemExit):
		# \show causes non-zero exit code
		main([fn_tex, '--interaction=nonstopmode'])
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex --interaction=nonstopmode %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored(r"> \foo=macro:")
	assert lines[3] == Colored(r"->hello world.")
	assert lines[4] == Colored(r"l.5 \show\foo")
	assert lines[5] == Colored("")
	assert lines[6] == Colored("aux file has changed")
	assert len(lines) == 7
	assert os.path.isfile(fn_pdf)

def test_tracing(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}

\def\foo{hello world}

\begin{document}
	\typeout{! ========== tracing 1 ==========}
	\tracingmacros=1
	\tracingonline=1
\foo
	\tracingonline=0
	\tracingmacros=0
	\typeout{! ========== tracing 0 ==========}
\end{document}
""")
	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored(r"! ========== tracing 1 ==========")
	assert lines[3] == Colored("")
	assert lines[4] == Colored(r"\foo ->hello world")
	i = lines.index(Colored(r"! ========== tracing 0 =========="))  # type: ignore [arg-type]
	assert lines[i+1] == Colored("aux file has changed")
	assert len(lines) == i+2
	assert os.path.isfile(fn_pdf)


# ------- test command line arguments pass through -------

def test_pass_through_option_with_single_dash_and_no_arg(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main(['-no-shell-escape', fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex -no-shell-escape %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_pass_through_option_with_double_dash_and_no_arg(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main(['--no-shell-escape', fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex --no-shell-escape %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_pass_through_option_with_single_dash_and_arg(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main(['-synctex=1', fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex -synctex=1 %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_pass_through_option_with_double_dash_and_arg(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main(['--synctex=1', fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex --synctex=1 %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_pass_through_option_with_o(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main(['-O=-synctex=1', '-O-interaction=batch', fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex -synctex=1 -interaction=batch %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3

def test_order_of_options(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: 'pytest.MonkeyPatch') -> None:
	monkeypatch.setenv("LATEX_RUNNER_DEFAULT_TEX_OPTIONS", '-synctex=1')
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
%!TeX option = --shell-escape
\documentclass{article}
\begin{document}
hello world
\end{document}
""")
	main(['-no-shell-escape', fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex -synctex=1 --shell-escape -no-shell-escape %s" % os.path.split(fn_tex)[1]
	assert lines[2] == Colored("aux file has changed")
	assert len(lines) == 3


# ------- test rerun -------

def test_rerun_when_table_of_content_changes(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
\tableofcontents
\section{hello}
\section{world}
\end{document}
""")
	main([fn_tex, '-n5'])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	i = lines.index(Colored("========== rerun 1 =========="))   # type: ignore [arg-type]
	assert i > 2
	assert lines[i-1] == Colored("aux file has changed")
	assert lines[i+1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert len(lines) == i + 2

def test_rerun_when_references_change(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX program = pdflatex

\documentclass[a4paper]{article}
\usepackage{geometry}

\begin{document}
\tableofcontents

\vspace{17cm}

\section{hello}
\label{hello}

\section{world}
to be greeted as described in section~\ref{hello} on page~\pageref{hello}
\end{document}
""")
	main([fn_tex, '-n5'])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(fn_pdf)

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	i = lines.index(Colored("========== rerun 1 =========="), 2)   # type: ignore [arg-type]
	assert lines[i-1] == Colored("aux file has changed")
	assert lines[i+1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	i = lines.index(Colored("========== rerun 2 =========="), i)   # type: ignore [arg-type]
	assert lines[i-1] == Colored("aux file has changed")
	assert lines[i+1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert len(lines) == i + 2


def test_rerun_after_biber(monkeypatch: 'pytest.MonkeyPatch', tmp_path: Path) -> None:
	# I cannot use capsys because I am using subprocess.run(cmd, stdout=sys.stderr) in the system under test.
	# Trying to use capsys causes io.UnsupportedOperation: fileno.
	fn_tex = str(tmp_path / 'test.tex')
	fn_bib = str(tmp_path / 'test.bib')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX program = pdflatex

\documentclass{article}
\usepackage[backend=biber]{biblatex}
\addbibresource{test.bib}

\begin{document}
see the biblatex documentation~\autocite{biblatex}

\printbibliography[heading=bibnumbered]
\end{document}
""")
	with open(fn_bib, 'wt') as f:
		f.write(r"""
@manual{biblatex,
	title = {The biblatex Package},
	author = {Philip Kime and Moritz Wemheuer and Philipp Lehman},
	version = {3.19},
}
""")
	with tempfile.TemporaryFile(mode='w+') as tmp:
		monkeypatch.setattr(sys, 'stderr', tmp)
		main([fn_tex, '-n5'])
		tmp.seek(0)
		lines = tmp.read().splitlines()

	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert Colored("running `biber test`") in lines
	i = lines.index(Colored("========== rerun 1 =========="))  # type: ignore [arg-type]
	assert lines[i+1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert Colored("running `biber test`") not in lines[i:]
	i = lines.index(Colored("========== rerun 2 =========="), i)  # type: ignore [arg-type]
	assert lines[i+1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert len(lines) == i + 2

def test_dont_rerun_if_bib_file_contains_error(monkeypatch: 'pytest.MonkeyPatch', tmp_path: Path) -> None:
	# I cannot use capsys because I am using subprocess.run(cmd, stdout=sys.stderr) in the system under test.
	# Trying to use capsys causes io.UnsupportedOperation: fileno.
	fn_tex = str(tmp_path / 'test.tex')
	fn_bib = str(tmp_path / 'test.bib')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX program = pdflatex

\documentclass{article}
\usepackage[backend=biber]{biblatex}
\addbibresource{test.bib}

\begin{document}
see the biblatex documentation~\autocite{biblatex}

\printbibliography[heading=bibnumbered]
\end{document}
""")
	with open(fn_bib, 'wt') as f:
		f.write(r"""
@manual{biblatex,
	title = {The biblatex Package}
	author = {Philip Kime and Moritz Wemheuer and Philipp Lehman}
	version = {3.19}
}
""")
	with tempfile.TemporaryFile(mode='w+') as tmp:
		monkeypatch.setattr(sys, 'stderr', tmp)
		main([fn_tex, '-n5'])
		tmp.seek(0)
		lines = tmp.read().splitlines()

	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert Colored("running `biber test`") in lines
	assert Colored("========== rerun 1 ==========") not in lines

def test_rerun_after_makeglossaries(monkeypatch: 'pytest.MonkeyPatch', tmp_path: Path) -> None:
	# I cannot use capsys because I am using subprocess.run(cmd, stdout=sys.stderr) in the system under test.
	# Trying to use capsys causes io.UnsupportedOperation: fileno.
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX program = pdflatex

\documentclass{article}
\usepackage{hyperref}
\usepackage[xindy,nogroupskip,nopostdot,numberedsection]{glossaries}

\hypersetup{hidelinks}
\makeglossaries

\newglossaryentry{ao-meter}{
	name = {$\alpha\Omega$-\lowercase{meter}},
	sort = alphaOmega-meter,
	description = {An open source dosimeter which calculates the five alpha-opic values.},
}


\begin{document}
A text about the \gls{ao-meter}.

\printglossary

\end{document}
""")
	with tempfile.TemporaryFile(mode='w+') as tmp:
		monkeypatch.setattr(sys, 'stderr', tmp)
		main([fn_tex, '-n5'])
		tmp.seek(0)
		lines = tmp.read().splitlines()

	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
	assert Colored("running `makeglossaries test`") in lines
	i = lines.index(Colored("========== rerun 1 =========="))  # type: ignore [arg-type]
	assert lines[i+1] == Colored("running: pdflatex %s" % os.path.split(fn_tex)[1])
	assert lines[i+2] == Colored("Package rerunfilecheck Warning: File `test.out' has changed.")
	assert lines[i+3] == Colored("(rerunfilecheck)                Rerun to get outlines right")
	assert lines[i+4] == Colored("(rerunfilecheck)                or use package `bookmark'.")
	assert lines[i+5] == Colored("")
	assert lines[i+6] == Colored("aux file has changed")
	assert lines[i+7] == Colored("========== rerun 2 ==========")
	assert lines[i+8] == Colored("running: pdflatex test.tex")
	assert len(lines) == i + 9


# ------- test multi build (jobname) -------

def test_magic_comment_jobname_pattern_colon(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'main.tex')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX jobname = content:*.tex
\documentclass{article}
\begin{document}
\input{content/\jobname}
\end{document}
""")

	os.mkdir(tmp_path / 'content')
	for fn in ('a.tex', 'b.tex', 'c.tex', 'c.log', 'readme.md'):
		with open(tmp_path / 'content' / fn, 'wt') as f:
			f.write(r"""
\def\fn{%s}
\typeout{hello from \fn}
\fn
""" % fn)

	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(tmp_path / 'a.pdf')
	assert os.path.isfile(tmp_path / 'b.pdf')
	assert os.path.isfile(tmp_path / 'c.pdf')
	assert not os.path.isfile(tex_to_pdf(fn_tex))

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex -jobname=a %s" % os.path.split(fn_tex)[1]
	assert lines[2] == "running: pdflatex -jobname=b %s" % os.path.split(fn_tex)[1]
	assert lines[3] == "running: pdflatex -jobname=c %s" % os.path.split(fn_tex)[1]
	assert len(lines) == 4

	with open(tmp_path / 'a.log', 'rt') as f:
		assert "hello from a.tex" in f.read().splitlines()

	with open(tmp_path / 'b.log', 'rt') as f:
		assert "hello from b.tex" in f.read().splitlines()

	with open(tmp_path / 'c.log', 'rt') as f:
		assert "hello from c.tex" in f.read().splitlines()

def test_magic_comment_jobname_pattern_slash(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'main.tex')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX jobname = content/*.tex
\documentclass{article}
\begin{document}
\input{\jobname}
\end{document}
""")

	os.mkdir(tmp_path / 'content')
	for fn in ('a.tex', 'b.tex', 'c.tex', 'c.log', 'readme.md'):
		with open(tmp_path / 'content' / fn, 'wt') as f:
			f.write(r"""
\def\fn{%s}
\typeout{hello from \fn}
\fn
""" % fn)

	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(tmp_path / 'content' / 'a.pdf')
	assert os.path.isfile(tmp_path / 'content' / 'b.pdf')
	assert os.path.isfile(tmp_path / 'content' / 'c.pdf')
	assert not os.path.isfile(tex_to_pdf(fn_tex))

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex -jobname=content/a %s" % os.path.split(fn_tex)[1]
	assert lines[2] == "running: pdflatex -jobname=content/b %s" % os.path.split(fn_tex)[1]
	assert lines[3] == "running: pdflatex -jobname=content/c %s" % os.path.split(fn_tex)[1]
	assert len(lines) == 4

	with open(tmp_path / 'content' / 'a.log', 'rt') as f:
		assert "hello from a.tex" in f.read().splitlines()

	with open(tmp_path / 'content' / 'b.log', 'rt') as f:
		assert "hello from b.tex" in f.read().splitlines()

	with open(tmp_path / 'content' / 'c.log', 'rt') as f:
		assert "hello from c.tex" in f.read().splitlines()

def test_magic_comment_jobname_multiple_literals(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	fn_tex = str(tmp_path / 'main.tex')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX jobname = 1
% !TeX jobname = 2
\documentclass{article}
\begin{document}
  \def\comparejobname{1}
  \edef\expandedjobname{\jobname}
  \ifx\comparejobname\expandedjobname
      \def\say{This is job 1.}
  \else
      \def\say{This is not job 1.}
  \fi
  \typeout{\say}
  \say
\end{document}
""")

	main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert os.path.isfile(tmp_path / '1.pdf')
	assert os.path.isfile(tmp_path / '2.pdf')
	assert not os.path.isfile(tex_to_pdf(fn_tex))

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex -jobname=1 %s" % os.path.split(fn_tex)[1]
	assert lines[2] == "running: pdflatex -jobname=2 %s" % os.path.split(fn_tex)[1]
	assert len(lines) == 3

	with open(tmp_path / '1.log', 'rt') as f:
		assert "This is job 1." in f.read().splitlines()

	with open(tmp_path / '2.log', 'rt') as f:
		assert "This is not job 1." in f.read().splitlines()

def test_magic_comment_new_jobname(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path) -> None:
	with open(tmp_path / 'main.tex', 'wt') as f:
		f.write(r"""
% !TeX jobname = characters:*.tex
\documentclass{article}

\newcommand\SetName[2]{\expandafter\newcommand\csname name:#1\endcsname{#2}}
\newcommand\GetName[1]{\csname name:#1\endcsname}

\input{characters/alice}
\input{characters/bob}
\input{characters/charly}

\begin{document}
  List of all characters:
  \begin{itemize}
  \item \GetName{alice}
  \item \GetName{bob}
  \item \GetName{charly}
  \end{itemize}

  This is \GetName{\jobname}.
\end{document}
""")

	os.mkdir(tmp_path / 'characters')
	with open(tmp_path / 'characters' / 'alice.tex', 'wt') as f:
		f.write(r"""
% !TeX root = ../main.tex
% !TeX new jobname = %
\SetName{alice}{Alice}
""")
	with open(tmp_path / 'characters' / 'bob.tex', 'wt') as f:
		f.write(r"""
% !TeX root = ../main.tex
% !TeX new jobname = %
\SetName{bob}{Bob}
""")
	with open(tmp_path / 'characters' / 'charly.tex', 'wt') as f:
		f.write(r"""
% !TeX root = ../main.tex
% !TeX new jobname = %
\SetName{charly}{Charly}
""")

	main([str(tmp_path / 'characters' / 'bob.tex')])
	captured = capsys.readouterr()
	assert captured.out == ""
	assert not os.path.isfile(tmp_path / 'alice.pdf')
	assert os.path.isfile(tmp_path / 'bob.pdf')
	assert not os.path.isfile(tmp_path / 'charly.pdf')
	assert not os.path.isfile(tmp_path / 'main.pdf')

	lines = captured.err.splitlines()
	assert lines[0].startswith("cd ")
	assert lines[1] == "running: pdflatex -jobname=bob main.tex"
	assert len(lines) == 2


# ------- test errors -------

def test_error_no_files(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.chdir(tmp_path)
	with pytest.raises(SystemExit):
		main([])
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert strip_color(lines[0]) == "no tex file found in %r" % str(tmp_path)
	assert len(lines) == 1

def test_error_invalid_path(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.chdir(tmp_path)
	with pytest.raises(SystemExit):
		main(['not-existing.tex'])
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert strip_color(lines[0]) == "no such file: not-existing.tex"
	assert len(lines) == 1

def test_error_empty_file(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.chdir(tmp_path)
	with open(tmp_path / 'main.tex', 'wt') as f:
		f.write(r"""
% This file contains only comments
% and empty lines.
""")
	with open(tmp_path / 'content.tex', 'wt') as f:
		f.write(r"""
%!TeX root = main.tex
This file already contains something.
""")
	with pytest.raises(SystemExit):
		main(['content.tex'])
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert strip_color(lines[0]) == "the file is empty: main.tex"
	assert len(lines) == 1

def test_error_multiple_files(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.chdir(tmp_path)
	fn1_tex = str(tmp_path / 'test1.tex')
	fn1_pdf = tex_to_pdf(fn1_tex)
	with open(fn1_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello~1
\end{document}
""")
	fn2_tex = str(tmp_path / 'test2.tex')
	fn2_pdf = tex_to_pdf(fn2_tex)
	with open(fn2_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello~2
\end{document}
""")
	with pytest.raises(SystemExit):
		main([])
	captured = capsys.readouterr()
	assert not os.path.isfile(fn1_pdf)
	assert not os.path.isfile(fn2_pdf)
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert strip_color(lines[0]) == "multiple tex files found in %r:" % str(tmp_path)
	assert strip_color(lines[1]) == "- %s" % os.path.split(fn1_tex)[1]
	assert strip_color(lines[2]) == "- %s" % os.path.split(fn2_tex)[1]
	assert strip_color(lines[3]) == "pointing to different root files:"
	assert strip_color(lines[4]) == "- %s" % os.path.split(fn1_tex)[1]
	assert strip_color(lines[5]) == "- %s" % os.path.split(fn2_tex)[1]
	assert strip_color(lines[6]) == "please pass the file you want to build as command line argument"
	assert len(lines) == 7

def test_error_wrong_root_comment(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
	os.mkdir(tmp_path / 'preamble')
	monkeypatch.chdir(tmp_path / 'preamble')
	root_tex = str(tmp_path / 'test.tex')
	root_pdf = tex_to_pdf(root_tex)
	with open(root_tex, 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
hello~world
\end{document}
""")
	fn1_tex = str(tmp_path / 'preamble' / 'test1.tex')
	fn1_pdf = tex_to_pdf(fn1_tex)
	with open(fn1_tex, 'wt') as f:
		f.write(r"""
% !TeX root = ../test.tex
""")
	fn2_tex = str(tmp_path / 'preamble' / 'test2.tex')
	fn2_pdf = tex_to_pdf(fn2_tex)
	with open(fn2_tex, 'wt') as f:
		f.write(r"""
% !TeX root = ../main.tex
""")
	fn3_tex = str(tmp_path / 'preamble' / 'test3.tex')
	fn3_pdf = tex_to_pdf(fn3_tex)
	with open(fn3_tex, 'wt') as f:
		f.write(r"""
% !TeX root = ../main.tex
""")
	with pytest.raises(SystemExit):
		main([])

	captured = capsys.readouterr()
	assert not os.path.isfile(root_pdf)
	assert not os.path.isfile(fn1_pdf)
	assert not os.path.isfile(fn2_pdf)
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert strip_color(lines[0]) == "multiple tex files found in %r:" % str(tmp_path / 'preamble')
	assert strip_color(lines[1]) == "- %s" % os.path.split(fn1_tex)[1]
	assert strip_color(lines[2]) == "- %s" % os.path.split(fn2_tex)[1]
	assert strip_color(lines[3]) == "- %s" % os.path.split(fn3_tex)[1]
	assert strip_color(lines[4]) == "pointing to different root files:"
	assert strip_color(lines[5]) == "- ../test.tex"
	assert strip_color(lines[6]) == "- ../main.tex  (does not exist)"
	assert strip_color(lines[7]) == "please pass the file you want to build as command line argument"
	assert len(lines) == 8

def test_error_disallowed_program(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.chdir(tmp_path)
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX program = virus

\documentclass{article}
\begin{document}
hello~1
\end{document}
""")
	with pytest.raises(SystemExit):
		main([])
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert strip_color(lines[0]) == "'virus' is not a program I know, I am not running it for security reasons."
	assert strip_color(lines[1]) == "Please edit the magic comment in test.tex"
	assert strip_color(lines[2]) == "or run `latex-runner --edit-config` and add virus to allowed-tex-programs."
	assert len(lines) == 3
	assert not os.path.exists(fn_pdf)

def test_error_disallowed_program_after_root(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.chdir(tmp_path)
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = str(tmp_path / 'main.pdf')
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX root = main.tex
% !TeX program = virus

hello world
""")
	with open(tmp_path / 'main.tex', 'wt') as f:
		f.write(r"""
\documentclass{article}
\begin{document}
\input{test}
\end{document}
""")
	with pytest.raises(SystemExit):
		main([fn_tex])
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert strip_color(lines[0]) == "'virus' is not a program I know, I am not running it for security reasons."
	assert strip_color(lines[1]) == "Please edit the magic comment in %s" % os.path.abspath('test.tex')
	assert strip_color(lines[2]) == "or run `latex-runner --edit-config` and add virus to allowed-tex-programs."
	assert len(lines) == 3
	assert not os.path.exists(fn_pdf)

def test_error_disallowed_option_2(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.chdir(tmp_path)
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX program = xelatex
% !TeX option = --run-virus

\documentclass{article}
\begin{document}
hello~1
\end{document}
""")
	main([])
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert strip_color(lines[0]) == "--run-virus is not a tex option which I know is safe to use, I am ignoring it for security reasons."
	assert strip_color(lines[1]) == "Please edit the magic comment in test.tex"
	assert strip_color(lines[2]) == "or run `latex-runner --edit-config` and add --run-virus to allowed-tex-options."
	assert lines[3] == "running: xelatex %s" % os.path.split(fn_tex)[1]
	assert lines[4] == Colored("aux file has changed")
	assert len(lines) == 5
	assert os.path.exists(fn_pdf)

def test_error_disallowed_option_1(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.chdir(tmp_path)
	fn_tex = str(tmp_path / 'test.tex')
	fn_pdf = tex_to_pdf(fn_tex)
	with open(fn_tex, 'wt') as f:
		f.write(r"""
% !TeX program = xelatex
% !TeX option = -run-virus

\documentclass{article}
\begin{document}
hello~1
\end{document}
""")
	main([])
	captured = capsys.readouterr()
	assert captured.out == ""

	lines = captured.err.splitlines()
	assert strip_color(lines[0]) == "-run-virus is not a tex option which I know is safe to use, I am ignoring it for security reasons."
	assert strip_color(lines[1]) == "Please edit the magic comment in test.tex"
	assert strip_color(lines[2]) == "or run `latex-runner --edit-config` and add --run-virus to allowed-tex-options."
	assert lines[3] == "running: xelatex %s" % os.path.split(fn_tex)[1]
	assert lines[4] == Colored("aux file has changed")
	assert len(lines) == 5
	assert os.path.exists(fn_pdf)

def test_invalid_config(capsys: 'pytest.CaptureFixture[str]', tmp_path: Path, monkeypatch: 'pytest.MonkeyPatch') -> None:
	fn_config = str(tmp_path / 'test-config')
	with monkeypatch.context() as m:
		m.setattr(ConfigFile, 'config_path', str(fn_config))
		with open(fn_config, 'wt') as f:
			f.write('x')

		fn_tex = str(tmp_path / 'test.tex')
		fn_pdf = tex_to_pdf(fn_tex)
		with open(fn_tex, 'wt') as f:
			f.write(r"""
	\documentclass{article}
	\begin{document}
	hello world
	\end{document}
	""")
		main([fn_tex])
		captured = capsys.readouterr()
		assert captured.out == ""
		assert os.path.isfile(fn_pdf)

		lines = captured.err.splitlines()
		assert lines[0] == Colored("While loading %s:" % fn_config)
		assert lines[1] == Colored("unknown command 'x' in line 1 'x'")
		assert lines[2].startswith("cd ")
		assert lines[3] == "running: pdflatex %s" % os.path.split(fn_tex)[1]
		assert lines[4] == Colored("aux file has changed")
		assert len(lines) == 5
