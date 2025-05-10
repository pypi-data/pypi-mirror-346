# latex-runner

A wrapper around LaTeX to build files which

- reads [magic comments](#magic-comments) to determine the TeX program and options to be used.
- filters the output to show only errors, warnings, over-/underfull boxes, tracing commands and prompts.
- runs [biber](https://ctan.org/pkg/biber) and [makeglossaries](https://ctan.org/pkg/glossaries) if necessary.
- reruns LaTeX up to -n times if necessary.


## Magic Comments

This program supports the following [magic comments](https://texstudio-org.github.io/advanced.html#advanced-header-usage).
For performance reasons this program stops looking for magic comments at the first non-empty line which is not a comment.

```tex
% !TeX root = ../main.tex
```

Run the TeX program with the given file instead.
This is useful if you have split up your document into multiple files, the current file is included in the main file with [`\input` or `\include`](https://tex.stackexchange.com/questions/246/when-should-i-use-input-vs-include) and you have told vim to build the currently opened file with this program.

Magic comments from the root file are loaded immediately when this magic comment is encountered.


```tex
% !TeX program = pdflatex
```

The program used to build the tex file.

For security reasons programs *not* listed in the `allowed-tex-programs` setting are *not* executed.
By default the allowed programs are `pdflatex`, `xelatex`, `lualatex`, `latex`, `tex` and `pdftex`.
You can change these with `latex-runner --edit-config`.


```tex
% !TeX option = -shell-escape
```

A command line option which should be passed to the TeX program.
You can repeat this comment to enable several command line options.
I have introduced this type of comment because at the time of this writing `% !TeX program = pdflatex -shell-escape` breaks compilation in [TeX studio](https://www.texstudio.org/).

For security reasons options *not* listed in the `allowed-tex-options` setting are *not* passed to the TeX program.
By default the allowed options are `--shell-escape`, `--8bit`, `--interaction=batchmode`, `--interaction=nonstopmode`, `--interaction=scrollmode` and `--interaction=errorstopmode`.
You can change these with `latex-runner --edit-config`.


```tex
% !TeX [new] jobname = content:*.tex
```

The jobname to pass to LaTeX.
If this is a [glob pattern](https://docs.python.org/3/library/glob.html) matching several files the LaTeX file will be built several times, once for each jobname.
The file extension is stripped from the jobname.
Optionally a path may be specified before, separated by a colon, specifying the directory in which to look for the glob pattern.
You can use this magic comment multiple times in order to specify multiple glob patterns or literal jobnames.
(This is not a standard comment supported by other programs as well, I have defined it.)

For example, let's assume there is a directory called `content` next to the main file.
This directory contains four files `a.tex`, `b.tex`, `c.tex` and `c.log`.

- Then `% !TeX jobname = content:*.tex` causes the main file to be built three times with the jobnames `a`, `b` and `c`, generating three pdf files `a.pdf`, `b.pdf` and `c.pdf`.
- Then `% !TeX jobname = content/*.tex` causes the main file to be built three times with the jobnames `content/a`, `content/b` and `content/c`, generating three pdf files `content/a.pdf`, `content/b.pdf` and `content/c.pdf`.

You can access the jobname in TeX with the macro `\jobname`.
For example:

- `\input{content/\jobname}`
- or

  ```tex
  \def\comparejobname{a}
  \edef\expandedjobname{\jobname}
  \ifx\comparejobname\expandedjobname
      This is job a.
  \else
      This is not job a.
  \fi
  ```

If you use `new jobname` all previously encountered jobnames are forgotten.
If you use `jobname` without `new` the list of jobnames will be expanded.

If the value is `%` it is replaced by the name of the file.
(Inspired by vim which uses `%` as a wildcard for the name of the current file when running shell commands.)

For example:

- main.tex:

    ```latex
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
    ```

- characters/alice.tex:

    ```latex
    % !TeX root = ../main.tex
    % !TeX new jobname = %
    \SetName{alice}{Alice}
    ```

- characters/bob.tex:

    ```latex
    % !TeX root = ../main.tex
    % !TeX new jobname = %
    \SetName{bob}{Bob}
    ```

- characters/charly.tex:

    ```latex
    % !TeX root = ../main.tex
    % !TeX new jobname = %
    \SetName{charly}{Charly}
    ```

Running `latex-runner main.tex` generates all three: alice.pdf, bob.pdf and charly.pdf.
Running `latex-runner characters/alice.tex` generates alice.pdf only.

Note that `%!TeX new jobname` is specified after `%!TeX root`.
This is important because `%!TeX root = ../main.tex` loads the `%!TeX jobname = characters:*.tex` from main.tex.


## Config

You can change settings with

```bash
latex-runner --edit-config
```

You can get help how to configure this program with

```bash
latex-runner --help-config
```


## Installation

You can install this program via the python package manager [pipx](https://pipx.pypa.io/latest/):

```bash
pipx install latex-runner
```


## vim integration

Copy the following into `~/.vim/after/ftplugin/tex.vim`.
This will allow you to run LaTeX once with F5, build the pdf completely with Control+F5 and open the pdf at the cursor position in [zathura](https://pwmt.org/projects/zathura/) with Shift+F5 or F6. You can open the log file with F7.

```vim
" build pdf
nnoremap <buffer> <F5> :exec "!latex-runner -n1 -synctex=1 " .. expand('%:p:S')<cr>
nnoremap <buffer> <C-F5> :exec "!latex-runner -n5 -synctex=1 " .. expand('%:p:S')<cr>

" open pdf
nnoremap <buffer> <S-F5> :exec "silent! !zathura --synctex-forward " .. line('.') .. ":" .. col('.') .. ":" .. expand('%:p') .. " " .. trim(system('latex-runner --get-pdf ' .. expand('%:p:S') .. " 2>/dev/null")) .. " >/dev/null 2>/dev/null &"<cr>:redraw!<cr>
nnoremap <buffer> <F6> :exec "silent! !zathura --synctex-forward " .. line('.') .. ":" .. col('.') .. ":" .. expand('%:p') .. " " .. trim(system('latex-runner --get-pdf ' .. expand('%:p:S') .. " 2>/dev/null")) .. " >/dev/null 2>/dev/null &"<cr>:redraw!<cr>

" open log file, return with :bp
nnoremap <buffer> <F7> :exec "edit " .. trim(system('latex-runner --get-log ' .. expand('%:p:S') .. " 2>/dev/null"))<cr>

" texdoc, to be used when cursor is in argument of \usepackage
nnoremap <buffer> K :silent exec '!texdoc <c-r>=expand("<cfile>")<cr> >/dev/null 2>&1 &' \| redraw!<cr>

" inserting magic comments
command InsertMagicCommentXelatex     :0put ='% !TeX program = xelatex'
command InsertMagicCommentPdflatex    :0put ='% !TeX program = pdflatex'
command InsertMagicCommentShellEscape :1put ='% !TeX option = -shell-escape'
command InsertMagicCommentRoot        :0put ='% !TeX root = ../main.tex'
```

## Running the tests

I am using [mypy](https://www.mypy-lang.org/) for static type checking and [pytest](https://docs.pytest.org/en/latest/) for dynamic testing.
[tox](https://tox.wiki/en/latest/) creates a virtual environment and installs all dependencies for you.
You can install tox with [pipx](https://pypa.github.io/pipx/) (`pipx install tox`).

```bash
$ tox
```

In order to make tox work without an internet connection install [devpi](https://devpi.net/docs/devpi/devpi/stable/%2Bd/index.html):

```bash
$ pipx install devpi-server
$ devpi-init
$ devpi-gen-config
$ su
# cp gen-config/devpi.service /etc/systemd/system/
# systemctl start devpi.service
# systemctl enable devpi.service
```

and add the following line to your bashrc:

```bash
export PIP_INDEX_URL=http://localhost:3141/root/pypi/+simple/
```
