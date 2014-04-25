#!/usr/bin/python

#  Create passphrase from dice rolls

from Tkinter import Tk, Frame, Button, LEFT, TOP, Label
from sys import exit
from json import load

# empty is a string of spaces to make the width of the labels good

EMPTY = '                   '
DICE = 6          #  There are 6 dice
DIE = 6           #  there are 6 spots on a die
WORDS = 6         #  We are generating 6 words
CAESAR = 13       #  ROT13 constant
ALPHABET = 26     #  Alphabet size


def fold(base, c):
  return base + (((c-base)+CAESAR) % ALPHABET)
  
def caesar(c):
  print c
  o = ord(c)
  if o < ord('a'):
    result = fold(ord('A'), o)
  else:
    result = fold(ord('a'), o)
  
  return chr(result)
  
#  The class Connect holds a die value and connects it to the corresponding label

class Connect(Label):
  def __init__(self, label):
    self.label = label
    self.value = -1
    
  def clear(self):
    self.value = -1
    self.label.config(text=' ')
    
  def set(self, value):
    self.value = value
    self.label.config(text = str(value+1))
    
  def setPick(self):
    self.label.config(bg = 'red')

  def clearPick(self):
    self.label.config(bg = 'white')

#  the class Switch is the central data repository

class Switch():
  def __init__(self):

# row and column can go out of range

    self.columnIndex = 0
    self.rowIndex = 0
    self.connectList = []
    self.wordLabels = []
    self.resultWords = []
    
    wordFile = open('randomWords.json', 'r')
    self.wordList = load(wordFile)
    wordFile.close()
    
  def add(self, row, column, connect):
    if column is 0:
      rowList = []
      self.connectList.append(rowList)
    else:
      rowList = self.connectList[row]
    
    rowList.append(connect)
  
  def iterateDice(self, function):
    for row in self.connectList:
      for item in row:
        function(item)

  def iterateWords(self, function):
    for label in self.wordLabels:
      function(label)
      
  def clear(self):
    self.iterateDice(lambda item: item.clear())
    self.iterateWords(lambda label: label.config(text = EMPTY))
    
    for index in range(len(self.resultWords)):
      self.resultWords[index] = ''
      
    self.rowIndex = 0
    self.columnIndex = 0
    self.setPick()
    
  def clearPick(self):
    self.iterateDice(lambda item: item.clearPick())

  def inRange(self):
    return 0 <= self.rowIndex < WORDS and 0 <= self.columnIndex < DICE

# row and column must be in range when this is called
    
  def getConnect(self):
    return self.connectList[self.rowIndex][self.columnIndex]

  def setPick(self):
    self.clearPick()
    
    if self.inRange():
      self.getConnect().setPick()

  def set(self, value):
    if self.inRange():
      self.getConnect().set(value)
      self.setWord()
      
    self.columnIndex += 1
    
    if self.columnIndex >= DICE:
      self.rowIndex += 1
      self.columnIndex = 0
      
    self.setPick()

  def changePick(self, rowArg, columnArg):
    self.rowIndex = rowArg
    self.columnIndex = columnArg
    self.setPick()

  def setWord(self):
    if 0 <= self.rowIndex < WORDS:
      row = self.connectList[self.rowIndex]
      result = 0
      multiply = 1

# this is in reverse order because the high order digit is on the left

      if all(item.value >= 0 for item in row):
        for index in range(DICE-1, -1, -1):
          result += multiply * row[index].value
          multiply *= DIE
          
        word = self.wordList[result]
        self.resultWords[self.rowIndex] = word
        self.wordLabels[self.rowIndex].config(text = word)

  def join(self):
    return (' '.join(self.resultWords)).strip()
    
  def obscure(self):
    result = map((lambda word: map (caesar, word)), self.resultWords)
    print result
    return (' '.join(map((lambda l: ''.join(l)), result))).strip()
      
#  Passphrase is the UI class, it also initializes the Switch class
            
class Passphrase(Frame, Switch):
  def __init__(self, parent, switch):
    Frame.__init__(self, parent, background="white")   
     
    self.parent = parent
    self.switch = switch

    self.initUI()

    self.switch.clear()
  
  def initUI(self):
    self.parent.title("Create Passphrase")
    self.makeInstructions()
    self.makeKeys()
    diceContainer = Frame(self)
    self.makeDice(diceContainer)
    self.makeWords(diceContainer)
    diceContainer.grid(row = 2, column = 0)
    self.makeButtons()
    
    self.grid()
      
  def makeInstructions(self):
    instructions = "Press a numbered button to enter a dice roll. "
    instructions += "When the row is full the word will appear.\n"
    instructions += "Click on a cell to edit entered rolls\n"
    instructions += "Text copied to clipboard may disappear when the program exits."
    label = Label(self, text = instructions, wraplength=300)
    label.grid(row = 0, column = 0)
  
  def makePress(self, number):
    return lambda: self.switch.set(number)
    
  def makeKeys(self):
    keyContainer = Frame(self)
    for number in range (0, DICE):
      button = Button(keyContainer, text = str(number+1), command = self.makePress(number))
      button.grid(row = 1,  column=number)
    
    keyContainer.grid(row = 1, column = 0)
    
  def makeClick(self, rowIndex, columnIndex):
    return lambda event: self.switch.changePick(rowIndex, columnIndex)
    
  def makeDice(self, container):
    for row in range (0, WORDS):
      for column in range (0, DICE):
        label = Label(container, text = ' ', borderwidth = 1, relief = 'solid')
        label.grid(row = row, column = column)
        label.bind("<Button-1>", self.makeClick(row, column))
        self.switch.add(row, column, Connect(label))
  
  def makeWords(self, container):
    for number in range (0, WORDS):
      label = Label(container, text=EMPTY, borderwidth=1, relief='solid')
      label.grid(row = number,  column = DICE)
      self.switch.wordLabels.append(label)
      self.switch.resultWords.append('')
        
  def copy(self):
    string = self.switch.join()
    self.parent.clipboard_clear()
    self.parent.clipboard_append(string)

  def copyObscure(self):
    string = self.switch.obscure()
    self.parent.clipboard_clear()
    self.parent.clipboard_append(string)

  def makeButtons(self):
    container = Frame(self)
    copy = Button(container, text = 'copy\nplain', command=self.copy)
    copy.grid(row = 0, column = 0, rowspan = 2)
    copy = Button(container, text = 'copy\nobscure', command=self.copyObscure)
    copy.grid(row = 0, column = 1, rowspan = 2)
    copy = Button(container, text = 'clear', command = self.switch.clear)
    copy.grid(row = 0, column = 2, rowspan = 2)
    leave = Button(container, text = 'exit', command = exit)
    leave.grid(row = 0, column = 3, rowspan = 2)
    container.grid(row = 3, column = 0)

def main():
  
  root = Tk()
  switch = Switch()
  app = Passphrase(root, switch)
  switch.setPick()
  root.mainloop()  


if __name__ == '__main__':
  main()  

