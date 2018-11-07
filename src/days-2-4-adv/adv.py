from room import Room
from player import Player
from item import Item

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
"North of you, the cave mount beckons.\n"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.\n"""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.\n"""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.\n"""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.\n"""),
}

player = {'default_character': Player('Terrance', room['outside']),}


# Link rooms together

# room['outside'].n_to = room['foyer']
# room['foyer'].s_to = room['outside']

# room['foyer'].n_to = room['overlook']
# room['foyer'].e_to = room['narrow']

# room['overlook'].s_to = room['foyer']

# room['narrow'].w_to = room['foyer']
# room['narrow'].n_to = room['treasure']
# room['treasure'].s_to = room['narrow']

room['outside'].connectRooms(room['foyer'], 'n')
room['foyer'].connectRooms(room['overlook'], 'n')
room['foyer'].connectRooms(room['narrow'], 'e')
room['narrow'].connectRooms(room['treasure'], 'n')

rock = Item('rock', 'large, grey boulder near the entrance to the cave.')

room['outside'].addItem(rock)


def printErrorString(errorString):
  print("\n{}\n".format(errorString))
  global noPrint
  noPrint = True



validDirection = ['n', 's', 'e', 'w']
noPrint = False
current_room = room['outside']
user_character = player['default_character']
print("Welcome to the game!")
inp = input("Type 'Terrance' to play as default character, or Type 'C' to create a character:")
if inp == 'Terrance':
  user_character == player['default_character']
  print(user_character)
elif inp == 'C' or inp == 'c':
  user_character = Player(input("Please enter your characters name: "), start_room = room['outside'])
  print('Welcome, {}!'.format(user_character.name))


def lookCommand(player, *args):
    if len(args) == 1:
      return False
    elif args[1] in validDirection:
      lookRoom = user_character.location.getRoomInDirection(args[1])
      if lookRoom == None:
        printErrorString('\nThere is nothing to see that way\n')
        return True
      else:
        print(f'\nTo the {args[1]} you see {lookRoom.name}.\n')
        return True
    else:
      print('\nI dont even know where you are trying to go..\n')
      return True

def moveCommand(player, *args):
  global current_room
  current_room = user_character.location.getRoomInDirection(args[0])
  global newRoom
  newRoom = user_character.location.getRoomInDirection(args[0])
  if newRoom == None:
    printErrorString('Cant go that direction')
  else:
    user_character.changeLocation(newRoom)
    return False
  
def itemCommand(user_character, *args):
  if (args[0] == 'get' or args[0] == 'take'):
    item = user_character.location.findItem(args[1])
    print(item)
    if item == None:
      printErrorString('\nThat item is not avalible\n')
    else:
      user_character.addItem(args[1])
      print(f'{args[1]} added to your inventory\n')
    return True
  elif args[0] == 'drop':
    if len(args) > 1:
      user_character.removeItem(args[1])
      print(f'\n{args[1]} was deleted from your inventory\n')
      return True
    else:
      print(f'{args[1]} doesnt exist.')  

commands = {}
commands['n'] = moveCommand
commands['s'] = moveCommand
commands['e'] = moveCommand
commands['w'] = moveCommand
commands['look'] = lookCommand
commands['get'] = itemCommand
commands['take'] = itemCommand
commands['drop'] = itemCommand

commandsHelp = {}
commandsHelp['n'] = 'move north'
commandsHelp['s'] = 'move south'
commandsHelp['e'] = 'move east'
commandsHelp['w'] = 'move west'
commandsHelp['look'] = 'look somewhere'



while True:
  if noPrint:
    noPrint = False
  else:
    print(current_room)
  inp = input("What is your input: ")
  inplist = inp.split(' ')
  print(f'Your input has {len(inplist)} arguments')
  for arg in inplist:
    print(arg)

  if inplist[0] == 'q':
    print("Bye!")
    break
    
 

  elif (inplist[0] == 'inventory' or inplist[0] == 'items'):
    print('\n--Your Inventory--\n')
    if len(user_character.inventory) > 0:
      for item in user_character.inventory:
        print(f'item --{item}\n')
        noPrint = True
    else:
      printErrorString('\nThere is nothing in your inventory\n')     

  elif inplist[0] == 'help':
    for command in commandsHelp:
      print(f'{command} -- {commandsHelp[command]}')
  elif inplist[0] in commands:
    noPrint = commands[inplist[0]](user_character, *inplist)
  else:
    printErrorString("\nI don't understand that\n")
