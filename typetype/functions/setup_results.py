import curses
import time
import random
import os


#setup the colors that will be used for the text and return the text for the user
def setup(stdscr, choices):

    #choose sentence from sentences
    if choices[0] == 'x':
        lines = open(os.path.dirname(os.path.dirname(__file__ ))+"/words/text.txt").readlines()
    elif choices[0] != 'x' and choices[1] == 'e':
        lines = open(os.path.dirname(os.path.dirname(__file__)) +"/words/200words.txt").readlines()
    elif choices[0] != 'x' and choices[1] == 'm':
        lines = open(os.path.dirname(os.path.dirname(__file__)) +"/words/5000words.txt").readlines()
    elif choices[0] != 'x' and choices[1] == 'h':
        lines = open(os.path.dirname(os.path.dirname(__file__)) +"/words/25000words.txt").readlines()
        
    #text
    if choices[0] == 'x' and choices[1] == 's':
        chosen = random.choice(lines)[:-1]
        while len(chosen)>160:
            chosen = random.choice(lines)[:-1]
    elif choices[0] == 'x' and choices[1] == 'm':
        chosen = random.choice(lines)[:-1]
        while len(chosen)>300 or len(chosen)<=160:
            chosen = random.choice(lines)[:-1]
    elif choices[0] == 'x' and choices[1] == 'l':
        chosen = random.choice(lines)[:-1]
        while len(chosen)<=300:
            chosen = random.choice(lines)[:-1]
    if choices[0] == 'x':
        return chosen
    
    #timed or words
    last10 = []
    sentence = ""
    needed = 200
    
    if choices[0] == 't' and choices[2] == '1':
        needed = 50
    elif choices[0] == 't' and choices[2] == '2':
        needed = 100
    elif choices[0] == 'w' and choices[2] == '1':
        needed = 10
    elif choices[0] == 'w' and choices[2] == '2':
        needed = 25
    elif choices[0] == 'w' and choices[2] == '3':
        needed = 50
    elif choices[0] == 'w' and choices[2] == '4':
        needed = 100
    
    #get the need ammount of words from the file
    while len(sentence.split(" "))<needed:
        randomword = random.choice(lines)[:-1]
        #don't let the same word repeat close to each other
        if randomword in last10:
            continue
        if len(last10) == 10:
            last10.pop(0)
        last10.append(randomword)
        if sentence!= "":
            randomword = " " + randomword
        sentence+=randomword
    
    return sentence






#---------------------------------------------------------------------------------------------------------------------






def end_screen(stdscr, original_words, new_words, extras, end_time, errorcount, status, timed, choices):
    
    #if its timed then set the end_time to the time
    if end_time>timed and timed:
        end_time = timed
    
    #count the number of r's in status
    correct_chars = 0
    i = 0
    while i<len(status):
        for stat in status[i]:
            if stat == 'r':
                correct_chars+=1
        i+=1
        

    #count the number of correct words typed
    correct_words = sum([1 if ( (word == new_words[count]) and len(extras[count])==0 ) else 0 for count, word in enumerate(original_words)])
    
    #take into account the spaces placed after correct words (dont count the last word)
    correct_chars += correct_words if correct_words != len(original_words) else (correct_words-1)
    
    
            
            
    #calculate results
    cpm = int(correct_chars*60.0/end_time)
    wpm = round(cpm/5.0,2) #round(correct_words*60.0/end_time ,2)
    accuracy = round((correct_chars)*1.0/(correct_chars+errorcount)*100,2)
    
    
    new_high = False
    scoreindex = 0
    #get the old highscore a list of incorrect words
    lines = open(os.path.dirname(os.path.dirname(__file__ ))+"/words/highscores.txt").readlines()
    if choices[0] == 't':
        if choices[1] == 'm':
            scoreindex += 3
        elif choices[1] == 'h':
            scoreindex += 6
    elif choices[0] == 'w':
        if choices[1] == 'e':
            scoreindex += 9
        elif choices[1] == 'm':
            scoreindex += 13
        elif choices[1] == 'h':
            scoreindex += 17
    try:
        if choices[2] == '2':
            scoreindex += 1
        elif choices[2] == '3':
            scoreindex += 2
        elif choices[2] == '4':
            scoreindex += 3
    except:
        scoreindex = -1
        
    if scoreindex != -1:
        old_high = float(lines[scoreindex][:-1])
        #update the highscore if it is beat
        if wpm > old_high:
            new_high = True
            f = open(os.path.dirname(os.path.dirname(__file__ ))+"/words/highscores.txt", "w")
            for count, line in enumerate(lines):
                if count == scoreindex:
                    f.write(str(wpm)+"\n")
                else:
                    f.write(line)
            f.close()
    

    
    
    
    
    active = 1
    
    while True:
        height, width = stdscr.getmaxyx()
        curses.curs_set(0)
        startheight = int(height/2.0)
        stdscr.clear()
        resultheight = int(height/4.0)
        resultx = int((width-len("wpm: {}      ".format(wpm))-len("acc: {}%".format(accuracy)))/2)+1
        try:
            if new_high:
                stdscr.addstr(resultheight-2, int((width-len("NEW HIGH SCORE"))/2), "NEW HIGH SCORE", curses.color_pair(5))
                stdscr.addstr(resultheight, resultx, "wpm: {}      ".format(wpm), curses.color_pair(5))
                stdscr.addstr(resultheight, resultx+len("wpm: {}      ".format(wpm)), "acc: {}%".format(accuracy), curses.color_pair(2))
                stdscr.addstr(resultheight+2, resultx, "time: {}s      ".format(round(end_time,1)), curses.color_pair(2))
                stdscr.addstr(resultheight+2, resultx+len("wpm: {}      ".format(wpm)), "cpm: {}".format(cpm), curses.color_pair(2))
            else: 
                stdscr.addstr(resultheight, resultx, "wpm: {}      ".format(wpm), curses.color_pair(2))
                stdscr.addstr(resultheight, resultx+len("wpm: {}      ".format(wpm)), "acc: {}%".format(accuracy), curses.color_pair(2))
                stdscr.addstr(resultheight+2, resultx, "time: {}s      ".format(round(end_time,1)), curses.color_pair(2))
                stdscr.addstr(resultheight+2, resultx+len("wpm: {}      ".format(wpm)), "cpm: {}".format(cpm), curses.color_pair(2))
            
            if active == 1:
                stdscr.addstr(startheight, int((width-len("restart game"))/2), "restart game", curses.color_pair(2))
            else:
                stdscr.addstr(startheight, int((width-len("restart game"))/2), "restart game", curses.color_pair(1))
            if active == 2:
                stdscr.addstr(startheight+2, int((width-len("back to menu"))/2), "back to menu", curses.color_pair(2))
            else:
                stdscr.addstr(startheight+2, int((width-len("back to menu"))/2), "back to menu", curses.color_pair(1))
            if active == 3:
                stdscr.addstr(startheight+4, int((width-len("quit"))/2), "quit", curses.color_pair(2))
            else:
                stdscr.addstr(startheight+4, int((width-len("quit"))/2), "quit", curses.color_pair(1))
            
                
        except:
            stdscr.addstr(0, 0, "Window is too small!", curses.color_pair(4))
        stdscr.refresh()
            
        #wait for an input key
        stdscr.timeout(-1)
        key = stdscr.getch()
        
        #down,up,left,right,space,enter: 258,259,260,261,32,10
        #next
        if key == 258 or key == 261:
            if active<3:
                active+=1
        #previous
        elif key == 259 or key == 260:
            if active>1:
                active-=1
        #select
        elif key == 10:
            if active == 1:
                return 'r'
            elif active == 2:
                return 'm'
            elif active == 3:
                return 'q'
        #esc
        elif key == 27:
            return 'q'
        


