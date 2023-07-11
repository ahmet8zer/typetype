try:
    from functions.game_selection import get_game, get_diff, get_mode
    from functions.setup_results import setup, end_screen
    from functions.refresh_update import refresh_screen, update_status, find_start_word
except:
    from typetype.functions.game_selection import get_game, get_diff, get_mode
    from typetype.functions.setup_results import setup, end_screen
    from typetype.functions.refresh_update import refresh_screen, update_status, find_start_word
import curses
import time
import random
import os
import argparse
import keyboard
import ctypes
import sys


def main(stdscr):
    
    #get command line args
    cursor = False
    parser = argparse.ArgumentParser(description='Typing Game')
    parser.add_argument('-cursor', action='store_true', help='Enable cursor mode')
    args = parser.parse_args()
    if args.cursor:
        #display | cursor
        cursor = True
    
    #start and setup colors and use the default terminal color as the background
    curses.start_color()
    curses.use_default_colors()
    stdscr.clear()
    #grey
    curses.init_pair(1, 235, -1)
    #white
    curses.init_pair(2, curses.COLOR_WHITE, -1)
    #(error)
    curses.init_pair(3, 160, -1)
    #(extra)
    #change color red to a greyish salmon color
    curses.init_color(curses.COLOR_RED, 300, 150, 150)
    curses.init_pair(4, curses.COLOR_RED, -1)
    #magenta
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)
    
    #prompt user for what type of game they want
    choices = get_game(stdscr)
    if choices == 'q':
        return 
    choices = get_diff(stdscr, choices)
    if 'q' in choices:
        return
    if 'x' not in choices:
        choices = get_mode(stdscr, choices)
    if 'q' in choices:
        return
    response = start_game(stdscr, choices, cursor)
    while True:
        if response == 'r':
            response = start_game(stdscr, choices, cursor)
        elif response == 'm':
            choices = get_game(stdscr)
            if choices == 'q':
                return
            choices = get_diff(stdscr, choices)
            if 'q' in choices:
                return
            if 'x' not in choices:
                choices = get_mode(stdscr, choices)
            if 'q' in choices:
                return
            response = start_game(stdscr, choices, cursor)
        elif response == 'q':
            break
    return









#this is where each indivudual game is played
def start_game(stdscr, choices, cursor):
    
    #get the sentence based on the users choices
    sentence = setup(stdscr, choices)
    #set some variables
    playing_game = False
    time_started = False
    start_time = 0
    end_time = 0
    onword = 0
    errors = 0
    stdscr.timeout(-1)
    
    #determine if it's a timed game:
    timed = 0
    if choices[0] == 't':
        if choices[2] == '1':
            timed = 15
        if choices[2] == '2':
            timed = 30
        if choices[2] == '3':
            timed = 60
    
    #list of valid characters that can be used while typing
    allchars = "qwertyuiopasdfghjklzxcvbnm QWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*()-=_+[]{}|;:\'\",./<>?`~\\"
    valid_characters = [thing for thing in allchars]
    
    #create a dictionary for the status of each character in each word
    status = {}
    
    #a list of every word in the sentence NO SPACES
    original_words = sentence.split(" ")
    
    #initialize staus dictionary
    for count, words in enumerate(original_words):
        status[count] = ['u' for _ in range(len(words))]

    #make a list of empty strings for each word in the sentence. The list will be populated as the user types
    new_words = ["" for words in original_words]
    
    #make a list of empty strings for the overflowing characters for each word
    extras = ["" for words in original_words]
    
    
    
    
    #initialize the screen with the message and the initial sentence
    refresh_screen(stdscr, status, original_words, playing_game, new_words, extras, onword, start_time, timed, cursor)
    
    #loop that waits for user input
    while True:
        
        #allow the getch() function to timeout so we can refresh the screen every 0.3 seconds
        stdscr.timeout(300)
        
        #wait for an input key
        key = stdscr.getch()
        try:
            char = chr(key)
        except:
            char = 'NA'
        
        #end the game if the timer has passed the time limit
        if timed!=0 and time_started:
            if time.time()-start_time>timed:
                break
        
        #if the function times out, refresh the screen
        if key == -1:
            refresh_screen(stdscr, status, original_words, playing_game, new_words, extras, onword, start_time, timed, cursor)
            continue
            
        
        #if the key is not a valid character, the delete key, or the esc key: go to the start of the loop
        #127 is the delete key and 27 is the esc key
        if char not in valid_characters and key!=127 and key!=27 and key!=8:
            continue
        
        
        #start time when the user starts typing for the first time
        if not time_started:
            #* will return to menu if the game hasn't started
            if key == 42:
                return 'm'
            time_started = True
            playing_game = True
            start_time = time.time()
        
        
        #if the delete key is pressed
        if key == 127 or key == 8:
            try:
                if sys.platform == 'win32':
                    if keyboard.is_pressed('ctrl') or (ctypes.windll.user32.GetKeyState(0x11) & 0x8000):
                        ctrldown = True
                    else:
                        ctrldown = False
                else:
                    ctrldown = False
            except:
                ctrldown = False
            #if ctrl is also pressed
            if ctrldown:
                #delete the whole word plus extras
                if len(extras[onword])>0:
                    extras[onword] = ''
                    new_words[onword] = ''
                elif len(new_words[onword])>0:
                    new_words[onword] = ''
                elif onword>0:
                    #if the word is empty then delete the whole previous word
                    onword-=1
                    extras[onword] = ''
                    new_words[onword] = ''
            #normal delete key
            #deleting from the current word
            elif len(extras[onword])>0:
                extras[onword] = extras[onword][:-1]
            elif len(new_words[onword])>0:
                new_words[onword] = new_words[onword][:-1]
            #move to previous word if the cursor is at the beginning of a word (if its not the first word)
            elif onword>0:
                onword -= 1
            
                
        #esc key restarts the game with the same settings
        elif key == 27:
            return start_game(stdscr, choices, cursor)
        
        
        
        #add character to extras list
        elif len(new_words[onword])>=len(original_words[onword]) and char!= ' ':
            if len(extras[onword])<10:
                extras[onword] = extras[onword] + char
                errors+=1
        #add character to the word that the user is typing
        elif char!=' ':
            new_words[onword] = new_words[onword] + char
            #if the character is wrong: increment the errors variable
            if original_words[onword][len(new_words[onword])-1] != char:
                errors+=1
            #if the last word is typed completely correctly, end the game
            if onword == len(original_words)-1 and new_words[onword] == original_words[onword]:
                status = update_status(status, original_words, new_words, onword)
                break
        #space means that the word is finished and we are on to the next word
        if char == ' ':
            #if letters are skipped then add to the error count.
            if len(original_words[onword])>len(new_words[onword]):
                errors+=1
            onword+=1
            #if we pass the last word then end the game
            if onword >= len(original_words):
                break
        
        
        #update the status dictionary
        status = update_status(status, original_words, new_words, onword)
        #refresh the screen
        refresh_screen(stdscr, status, original_words, playing_game, new_words, extras, onword, start_time, timed, cursor)
    
    #the time it took the user to finish
    end_time = time.time()-start_time
    #show the user the results on the end screen.
    user_response = end_screen(stdscr, original_words, new_words, extras, end_time, errors, status, timed, choices)
    #return the user response to main
    return user_response
    

#used to call main
def callmain():
    #this is to take away the escape delay
    os.environ.setdefault('ESCDELAY', '25')
    #run main
    curses.wrapper(main)

callmain()
