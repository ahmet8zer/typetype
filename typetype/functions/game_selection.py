import curses
import time
import random
import os




#user selects which game mode they want to play
def get_game(stdscr):
    active = 1
    while True:
        height, width = stdscr.getmaxyx()
        curses.curs_set(0)
        stdscr.clear()
        startheight = int(height/3)
        startheight = 4 if startheight<4 else startheight
        try:
            stdscr.addstr(1, int((width-4)/2), "type", curses.color_pair(2))
            stdscr.addstr(2, int((width-4)/2), "ǝdʎʇ", curses.color_pair(2))
            if active == 1:
                stdscr.addstr(startheight, int((width-len("timed mode"))/2), "timed mode", curses.color_pair(2))
            else:
                stdscr.addstr(startheight, int((width-len("timed mode"))/2), "timed mode", curses.color_pair(1))
            if active == 2:
                stdscr.addstr(startheight+2, int((width-len("words mode"))/2), "words mode", curses.color_pair(2))
            else:
                stdscr.addstr(startheight+2, int((width-len("words mode"))/2), "words mode", curses.color_pair(1))
            if active == 3:
                stdscr.addstr(startheight+4, int((width-len("quote mode"))/2), "quote mode", curses.color_pair(2))
            else:
                stdscr.addstr(startheight+4, int((width-len("quote mode"))/2), "quote mode", curses.color_pair(1))
            if active == 4:
                stdscr.addstr(startheight+7, int((width-len("quit"))/2), "quit", curses.color_pair(2))
            else:
                stdscr.addstr(startheight+7, int((width-len("quit"))/2), "quit", curses.color_pair(1))
            
        except:
            stdscr.addstr(0, 0, "Window is too small!", curses.color_pair(4))
        
        stdscr.refresh()
            
        #wait for an input key
        stdscr.timeout(-1)

        key = stdscr.getch()
        #down,up,left,right,space,enter: 258,259,260,261,32,10
        #next
        if key == 258 or key == 261:
            if active<4:
                active+=1
        #previous
        elif key == 259 or key == 260:
            if active>1:
                active-=1
        #enter
        elif key == 10:
            if active == 1:
                return 't'
            elif active == 2:
                return 'w'
            elif active == 3:
                return 'x'
            elif active == 4:
                return 'q'
        #esc
        elif key == 27:
            return 'q'











#user selects which difficulty they want
def get_diff(stdscr, choice):
    if 'q' in choice:
        return choice
    active = 1
    while True:
        height, width = stdscr.getmaxyx()
        sml = int((width-4)/2)
        startheight = int(height/3)
        startheight = 4 if startheight<4 else startheight
        curses.curs_set(0)
        stdscr.clear()
        try:
            stdscr.addstr(1, int((width-4)/2), "type", curses.color_pair(2))
            stdscr.addstr(2, int((width-4)/2), "ǝdʎʇ", curses.color_pair(2))
            if choice == 't' or choice == 'w':
                if active == 1:
                    stdscr.addstr(startheight, int((width-len("easy"))/2), "easy", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight, int((width-len("easy"))/2), "easy", curses.color_pair(1))
                if active == 2:
                    stdscr.addstr(startheight+2, int((width-len("medium"))/2), "medium", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight+2, int((width-len("medium"))/2), "medium", curses.color_pair(1))
                if active ==3:
                    stdscr.addstr(startheight+4, int((width-len("hard"))/2), "hard", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight+4, int((width-len("hard"))/2), "hard", curses.color_pair(1))
            elif choice == 'x':
                if active == 1:
                    stdscr.addstr(startheight, int((width-4)/2), "short", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight, int((width-4)/2), "short", curses.color_pair(1))
                if active == 2:
                    stdscr.addstr(startheight+2, int((width-4)/2), "medium", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight+2, int((width-4)/2), "medium", curses.color_pair(1))
                if active == 3:
                    stdscr.addstr(startheight+4, int((width-len("long"))/2), "long", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight+4, int((width-len("long"))/2), "long", curses.color_pair(1))
            if active == 4:
                stdscr.addstr(startheight+7, int((width-len("back"))/2), "back", curses.color_pair(2))
            else:
                stdscr.addstr(startheight+7, int((width-len("back"))/2), "back", curses.color_pair(1))
        except:
            stdscr.addstr(0, 0, "Window is too small!", curses.color_pair(4))
        
        stdscr.refresh()
            
        #wait for an input key
        stdscr.timeout(-1)
        key = stdscr.getch()
        #down,up,left,right,space,enter: 258,259,260,261,32,10
        
        #next
        if key == 258 or key == 261:
            if active<4:
                active+=1
        #previous
        elif key == 259 or key == 260:
            if active>1:
                active-=1
        #enter
        elif key == 10:
            if active == 1 and (choice == 't' or choice == 'w'):
                return choice + 'e'
            elif active == 2:
                return choice + 'm'
            elif active == 3 and (choice == 't' or choice == 'w'):
                return choice + 'h'
            elif active == 4:
                return get_diff(stdscr, get_game(stdscr))
            elif active == 1 and (choice == 'x'):
                return choice + 's'
            elif active == 3 and (choice == 'x'):
                return choice + 'l'
        #delete
        elif key == 127 or key == 8:
            return get_diff(stdscr, get_game(stdscr))
        








#get the time or word number that the user wants
def get_mode(stdscr, choice):
    if 'q' in choice:
        return choice
    active = 1
    active_max = 4 if choice[0]=='t' else 5
    while True:
        height, width = stdscr.getmaxyx()
        startheight = int(height/3)
        startheight = 4 if startheight<4 else startheight
        
        curses.curs_set(0)
        stdscr.clear()
        try:
            stdscr.addstr(1, int((width-4)/2), "type", curses.color_pair(2))
            stdscr.addstr(2, int((width-4)/2), "ǝdʎʇ", curses.color_pair(2))
            if choice[0] == 't':
                if active == 1:
                    stdscr.addstr(startheight, int((width-len("15s "))/2), "15s", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight, int((width-len("15s "))/2), "15s", curses.color_pair(1))
                if active == 2:
                    stdscr.addstr(startheight+2, int((width-len("30s "))/2), "30s", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight+2, int((width-len("30s "))/2), "30s", curses.color_pair(1))
                if active == 3:
                    stdscr.addstr(startheight+4, int((width-len("60s "))/2), "60s", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight+4, int((width-len("60s "))/2), "60s", curses.color_pair(1))
                if active == 4:
                    stdscr.addstr(startheight+7, int((width-len("back"))/2), "back", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight+7, int((width-len("back"))/2), "back", curses.color_pair(1))
            elif choice[0] == 'w':
                if active == 1:
                    stdscr.addstr(startheight, int((width-len("10 words"))/2), "10 words", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight, int((width-len("10 words"))/2), "10 words", curses.color_pair(1))
                if active == 2:
                    stdscr.addstr(startheight+2, int((width-len("25 words"))/2), "25 words", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight+2, int((width-len("25 words"))/2), "25 words", curses.color_pair(1))
                if active == 3:
                    stdscr.addstr(startheight+4, int((width-len("50 words"))/2), "50 words", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight+4, int((width-len("50 words"))/2), "50 words", curses.color_pair(1))
                if active == 4:
                    stdscr.addstr(startheight+6, int((width-len("100 word"))/2), "100 words", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight+6, int((width-len("100 word"))/2), "100 words", curses.color_pair(1))
                if active == 5:
                    stdscr.addstr(startheight+9, int((width-len("back"))/2), "back", curses.color_pair(2))
                else:
                    stdscr.addstr(startheight+9, int((width-len("back"))/2), "back", curses.color_pair(1))
        except:
            stdscr.addstr(0, 0, "Window is too small!", curses.color_pair(4))
        
        stdscr.refresh()
        
        #wait for an input key
        stdscr.timeout(-1)
        key = stdscr.getch()
        #down,up,left,right,space,enter: 258,259,260,261,32,10
        
        #next
        if key == 258 or key == 261:
            if active<active_max:
                active+=1
        #previous
        elif key == 259 or key == 260:
            if active>1:
                active-=1
        #select
        elif key == 10:
            if active == 1:
                return choice + '1'
            elif active == 2:
                return choice + '2'
            elif active == 3:
                return choice + '3'
            elif active == 4 and choice[0] == 't':
                return get_mode(stdscr, get_diff(stdscr, choice[:-1]))
            elif active == 14 and choice[0] == 'w':
                return choice + '4'
            elif active == 5:
                return get_mode(stdscr, get_diff(stdscr, choice[:-1]))
        #delete
        elif key == 127 or key == 8:
            return get_mode(stdscr, get_diff(stdscr, choice[:-1]))
        
        