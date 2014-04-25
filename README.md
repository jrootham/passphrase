passphrase
==========

xkcd on steriods

A small project to generate good passphrases

The python script passphrase.py is a GUI that accepts die rolls and selects words based on the rolls.

Download and unpack the zip file to get it. It should run as an executable.  It requires python with the tkinter option.

It turns out to be faster to roll one die six times than to roll six dice and sort them.

The words are between 6 and 12 characters long to balance unlikelyhood and ease of memorization.

Copy plain puts the phrase on the clipboard, copy obscure puts an obscured (case preserving ROT13) copy of the phrase on the clipboard. This is designed so that applications which accept pasted passphrases will reject bad passphrases typed into them.
