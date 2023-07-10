import curses
import time
import random
import os


#clears the screen and updates it with the most recent data
def refresh_screen(stdscr, status, original_words, playing_game, new_words, extras, onword, start_time, timed, cursor):
    #hide the cursor and clear the screen
    if cursor:
        curses.curs_set(0)
    else:
        curses.curs_set(1)
    stdscr.clear()
    cursorplaced = False
    #get the first word that we have to start at (we only show 2 or 3 lines at a time)
    firstword = find_start_word(stdscr, status, original_words, playing_game, new_words, extras, onword, start_time, timed, cursor)
    #this is how many lines we're going to display
    linesleft = 3 if firstword!=-1 else 2
    
    #adjust variables according to the screen dimensions
    height, width = stdscr.getmaxyx()
    line_start = int(width/6)
    line_width = int(width/6*4)
    start_height = int(height/4)
    #if the game hasn't started, then display a message
    if not playing_game:
        try:
            stdscr.addstr(start_height-2, int((width-len("start typing..."))/2), "start typing...")
        except: 
            stdscr.addstr(0, 0, "Window is too small!", curses.color_pair(4))
    
    #add character by character to the display
    current_x = line_start
    current_y = start_height
    cursor_x = line_start
    cursor_y = start_height
    wordcount = firstword if firstword !=-1 else 0
    
    #loop for each word in the text
    while wordcount<len(original_words):
        
        lettercount = 0
        #if the cursor is on this word, then take into account the width of the cursor
        if cursor and onword == wordcount:
            cursorwidth = 1
        else:
            cursorwidth = 0
        #if the word wont fit on this line, then move it down to the next
        if (current_x+cursorwidth+len(original_words[wordcount])+len(extras[wordcount]))>(line_start+line_width):
            current_y += 1
            linesleft -= 1
            if linesleft<1:
                break
            current_x = line_start
        #for each letter in the word
        while lettercount<len(original_words[wordcount]):
            #set the color of the letter based on the status of the letter
            if status[wordcount][lettercount]=='u':
                color = 1
            elif status[wordcount][lettercount]=='r':
                color = 2
            if status[wordcount][lettercount]=='w':
                color = 3
            if status[wordcount][lettercount]=='s':
                color = 1
            #place cursor if this is the right place
            if cursorplaced==False and (wordcount == onword) and (len(extras[wordcount])==0) and lettercount>=len(new_words[wordcount]):
                if not cursor:
                    cursor_y = current_y
                    cursor_x = current_x
                    cursorplaced = True
                else:
                    try:
                        stdscr.addstr(current_y, current_x, "|", curses.color_pair(2))
                    except:
                        stdscr.addstr(0, 0, "Window is too small!", curses.color_pair(4))
                    cursorplaced = True
                    current_x+=1
            #place letter on the screen
            try:
                stdscr.addstr(current_y, current_x, original_words[wordcount][lettercount], curses.color_pair(color))
            except:
                stdscr.addstr(0, 0, "Window is too small!", curses.color_pair(4))
            current_x+=1
            lettercount+=1
        #if there are letters in extra then we can place it now
        for count, letter in enumerate(extras[wordcount]):
            try:
                stdscr.addstr(current_y, current_x, extras[wordcount][count], curses.color_pair(4))
            except:
                stdscr.addstr(0, 0, "Window is too small!", curses.color_pair(4))
            current_x+=1
        #place cursor if this is the right place
        if (onword==wordcount) and cursorplaced == False:
            if not cursor:
                cursor_x = current_x
                cursor_y = current_y
                cursorplaced = True
            else:
                try:
                    stdscr.addstr(current_y, current_x, "|", curses.color_pair(2))
                except:
                    stdscr.addstr(0, 0, "Window is too small!", curses.color_pair(4))
                cursorplaced = True
                current_x+=1
        #add space between each word
        try:
            stdscr.addstr(current_y, current_x, " ", curses.color_pair(3))
        except:
            stdscr.addstr(0, 0, "Window is too small!", curses.color_pair(4))
        current_x+=1
        wordcount+=1
    
    #add the time to the screen
    time_diff = int(time.time() - start_time) if playing_game else 0
    if timed>0:
        time_diff = int(timed-time_diff) if (timed-time_diff)>0 else 0
    try:
        stdscr.addstr(current_y+2, int((width-len(str(time_diff)))/2), str(time_diff), curses.color_pair(2))
    except:
        stdscr.addstr(0, 0, "Window is too small!", curses.color_pair(4))
    #put to the screen
    stdscr.move(cursor_y,cursor_x)
    stdscr.refresh()
    



#-----------------------------------------------------------------------------------------------------





#updates the contents of the status dictionary
def update_status(status, original_words, new_words, onword):
    status2 = status
    i = onword-1 if onword>0 else 0
    while i<=onword:
        word = new_words[i]
        correct = original_words[i]
        #for each letter in the full word
        for count, correctchar in enumerate(correct):
            #if the user hasn't typed this part of the word, then break
            if count >= len(word):
                break
            #if the letter is right
            if correctchar == word[count]:
                status2[i][count] = 'r'
            #if the letter is wrong
            elif correctchar != word[count]:
                status2[i][count] = 'w'
        lastcount = len(word)
        if i!=onword:
            #if the letter was skipped then it will be here
            while lastcount<len(correct):
                status2[i][lastcount] = 's'
                lastcount+=1
        else:
            #this is for the word that you are on, for the letters after the cursor
            while lastcount<len(correct):
                status2[i][lastcount] = 'u'
                lastcount+=1
        i+=1
    #return the new and updated version of status
    return status2










#-------------------------------------------------------------------------------------------

#this function will find the word that we have to start displaying from 
#I want to display one line above and below where the cursor is
def find_start_word(stdscr, status, original_words, playing_game, new_words, extras, onword, start_time, timed, cursor):
    #hide the cursor and clear the screen
    cursorplaced = False
    
    #adjust variables according to the screen dimensions
    height, width = stdscr.getmaxyx()
    line_start = int(width/6)
    line_width = int(width/6*4)
    start_height = int(height/4)
    
    startword = 0
    previndex = 0
    
    #add character by character to the display
    current_x = line_start
    current_y = start_height
    wordcount = 0
    
    #loop for each word in the text
    while wordcount<len(original_words):
        lettercount = 0
        if cursor and onword == wordcount:
            cursorwidth = 1
        else:
            cursorwidth = 0
        #if the word wont fit on this line, then move it down to the next
        if (current_x+cursorwidth+len(original_words[wordcount])+len(extras[wordcount]))>(line_start+line_width):
            current_y += 1
            previndex = startword
            startword = wordcount
            current_x = line_start
        #for each letter in the word
        while lettercount<len(original_words[wordcount]):
            #place cursor if this is the right place
            if cursorplaced==False and (wordcount == onword) and (len(extras[wordcount])==0) and lettercount>=len(new_words[wordcount]):
                cursorplaced = True
                if startword == 0:
                    return -1
                return previndex
                current_x+=1
            #place letter on the screen
            current_x+=1
            lettercount+=1
        #if there are letters in extra then we can place it now
        for count, letter in enumerate(extras[wordcount]):
            current_x+=1
        #place cursor if this is the right place
        if (onword==wordcount) and cursorplaced == False:
            cursorplaced = True
            if startword == 0:
                return -1
            return previndex
            current_x+=1
        #add space between each word
        current_x+=1
        wordcount+=1
    

