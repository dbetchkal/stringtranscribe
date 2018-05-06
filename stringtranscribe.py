import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd

class Instrument(object):
    
    def __init__(self, num_frets, tuning, notation="integer", capo=0):
        
        self.num_frets = num_frets
        
        # check to see if the tuning was input as letter or integer
        if(isinstance( tuning[0] , int )):
            self.tuning = pd.Series(tuning)+capo
        elif(isinstance( tuning[0] , str )):
            self.tuning = pd.Series(self.letterToInteger(tuning))+capo
            
        self.num_strings = len(tuning)   
        
        # color dictionary
        self.colors = {0:"#ff0000", 1:"#00ffd8", 2:"#ff7f00", 
                       3:"#ffb1f7", 4:"#ffff00", 5:"#c71585",
                       6:"#32c715", 7:"#917249", 8:"#5959ff",
                       9:"#ffd864", 10:"#9542ff", 11:"#ebff5e"}
        
        self.notation = notation
            
        
        # a dictionary to convert numeric note names to letter note names
        # TO DO: parameter to override the convention of 0 = C ??
        self.noteToLetter = {0:"C", 1:"C#", 2:"D", 3:"D#", 4:"E", 5:"F", 6:"F#", 
                       7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}
    
    def letterToInteger(self, input):
        
        input = [x.title() for x in input]
    
        # a dictionary to convert letter to integer notes
        lettToIntDict = {"C":0, "C#":1, "Db":1, "D":2, "D#":3, "Eb":3, "E":4, "F":5, "F#":6, 
                         "Gb":6, "G":7, "G#":8, "Ab":8, "A":9, "A#":10, "Bb":10, "B":11}
    
        output = [lettToIntDict[h] for h in input]
    
        return output  
    
    def tabToInteger(self, tablature):
        '''convert tablature for a chord into raag
           expects a list of values with "X" indicating
           the note values that are not played.
           
           the user MUST enter all strings for the
           given instrument.'''
        
        # remove unplayed notes (indicated by "X")
        remove_indices = [m for m, x in enumerate(tablature) if x == "X" or x == "x"]
        reduced_tab = np.array([i for j, i in enumerate(tablature) if j not in remove_indices])
        
        # only the strings used in the tab
        strings_remaining = np.delete(np.arange(1, self.num_strings+1), remove_indices)
        
        # use the fretboard to calculate the notes played
        raagInput = [self.fretboard().loc["string " + str(y), "fret " + str(x)] for x, y in zip(reduced_tab, strings_remaining)]
        
        return raagInput
    
    
    def tabToLetter(self, tablature):
         
        return [self.noteToLetter[nT] for nT in self.tabToInteger(tablature)]
        
    def neckDiagram(self, notes):

        # an arbitrary length of the instrument
        s = 100

        # set up the spacing of the frets
        fret_positions = [s - (s / pow(2, (n / 12))) for n in range(0, self.num_frets + 1)]

        # space the strings out using a linear interpolation
        string_positions = np.linspace(0,10,self.num_strings+1, endpoint=False)
            
        # instantiate a figure object
        fig = plt.figure(figsize=(20,3))

        # give it a tan background color
        plt.rcParams['axes.facecolor']='tan'

        # draw frets
        for fret in fret_positions:

            # draw the nut in a little different color
            if(fret == 0):
                plt.axvline(x=fret, ymin=0.0, ymax = 6, linewidth=7, color='moccasin', zorder = 0)

            elif(fret > 0):
                plt.axvline(x=fret, ymin=0.0, ymax = 6, linewidth=2, color='lightgray', zorder = 0)
            
        # (lightly) draw strings
        for string in string_positions:

            plt.axhline(y=string, xmin = 0.0, xmax = fret_positions[-1], linewidth=3, color='silver', alpha=0.8)

        # set up fret labels & limit the diagram to the nut
        plt.xticks(fret_positions, np.arange(0, self.num_frets + 1))
        plt.gca().set_xlim(left=-0.5)

        # then set up the string lables
        plt.yticks(string_positions, np.arange(0, self.num_strings + 1))
        plt.ylim((0,10)) # something more elegant for spacing would be cool

        # a list comprehension of (row, column, note)  
        pos = np.array([(i, j, notes.ix[i, j]) for j, col in enumerate(notes.columns) for i, row in enumerate(notes.index)])
            
        # these are the positions of each value
        fingering_x = [fret_positions[x] for x, z in zip(pos[:,1], pos[:,2]) if not z == 999]
        fingering_y = [string_positions[y+1] for y, z in zip(pos[:,0], pos[:,2]) if not z == 999]

        #the name (numeric value) of the note
        notename = [z for z in pos[:,2] if not z == 999]

        # grab the colors of each note
        colors = [self.colors[g] for g in notename]

        # draw the selected notes on the fretboard
        plt.scatter(fingering_x, fingering_y, s=6845*pow(self.num_strings,-1.52), zorder=100, c=colors)
            
        for i, n in enumerate(notename):

            if(self.notation == "integer"):
                plt.annotate(n, xy=(fingering_x[i], fingering_y[i]), ha='center', zorder = 150, fontsize=14)

            elif(self.notation == "letter"):
                plt.annotate(self.noteToLetter[n], xy=(fingering_x[i], fingering_y[i]), ha='center', zorder = 150, fontsize=14)

        return fig
        

    def fretboard(self):
        '''calculates note values for the given instrument
           organized with rows as strings and columns as frets
           
           returns a pandas dataframe'''
        
        fboard = pd.DataFrame([(self.tuning + i) % 12 for i in range(self.num_frets + 1)]).T
        fboard.columns = ["fret " + str(num) for num in range(self.num_frets + 1)]
        fboard.index = ["string " + str(num) for num in range(1, self.num_strings + 1)]
        
        return fboard
        
        
    def raag(self, raag=None, tab=False):
        '''a method to return an image of notes on the fretboard
           
           expects a list integer or string values'''
        
        # if no raag is used, the method will return a full fretboard
        if(raag is None):
            raag = [0,1,2,3,4,5,6,7,8,9,10,11]
        
        # if a raag is used, and it's a list of integer values...
        elif(isinstance( raag[0] , int )):
            
            # ...if they're traditional integer notation, do nothing.
            if(tab == False):
                pass
            
            # ...but if they're in tablature notation, convert to integer
            elif(tab == True):
                raag = self.tabToInteger(raag)
            
        elif(isinstance( raag[0] , str )):
            
            # if tablature isn't being used, the whole raag must be converted to integer
            if(tab == False):
                raag = self.letterToInteger(raag)
            
            # sometimes tabs contain "X" or "x" on the first string
            # but this is fully handled by tabToInteger()
            elif(tab == True):
                raag = self.tabToInteger(raag)

        
        notes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        not_raag = [np.int(x) for x in notes if x not in raag]
        
        f = self.fretboard()  
        r = f.replace(not_raag, 999)
        
        return self.neckDiagram(r)
