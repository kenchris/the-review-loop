@echo off
rem Builds deck.pptx and deck.pdf. Usage: make.cmd [pptx|pdf|render 5 7 13]
python "%~dp0make.py" %*
