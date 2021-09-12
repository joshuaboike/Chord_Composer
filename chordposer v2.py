#GOOD FINDS!! (root, scale, chords)
#1) 45, HARMONIC_MINOR_SCALE, [1, 2, 4, 5, 1, 2, 6, 7]

from music import *
from random import *

score = Score("First Pass", 65)

drumsPart = Part("Drums", 0, 9)
bassDrumPhrase = Phrase(0.0)
snareDrumPhrase = Phrase(0.0)
hiHatPhrase = Phrase(0.0)

part = Part(STRINGS, 0)

bassPart = Part(BASS, 1)



phr = Phrase(0.0)
phr.setInstrument(ELECTRIC_GRAND)
 
mel = Phrase(0.0)
mel.setInstrument(MUTED_GUITAR)

bass = Phrase(0.0)
bass.setInstrument(ELECTRIC_BASS)

# Set scale of acceptable notes for 2 octaves
root = 59
scale = MINOR_SCALE
scale_second_oct = [x + 12 for x in scale]
scale = scale + scale_second_oct
print(scale)




# Determine tonic, sub-dom, and dominate notes
tonic = []
sub_dom = []
dom = []
for n in range(0, len(scale)):
   if n in [0, 2, 4, 6, 7]: #,  9, 11, 13]:
      tonic.append(scale[n])
   if n in [0, 1, 2, 3, 5, 7]: #, 8, 9, 10, 12]:
      sub_dom.append(scale[n])
   if n in [1, 3, 4, 6]: #, 8, 10, 11, 13]:
      dom.append(scale[n])

print("TONIC = " )
print(tonic)
#INPUTS
diatonic_prog = []
#diatonic_prog = [1]


#Add first melodic note as root
#note = Note(root, HN)
#mel.addNote(note)

durations = [
[QN, QN],
[QN, QN],
[QN, QN],
[HN],
[EN, EN, EN, EN],
[EN, EN, QN],
[QN, EN, EN],
[EN, QN, EN]
]



#Create chord progression
chord_prog = []
notes = [] #for testing output
for j in diatonic_prog:

   #diatonic chord you want to play:
   dtn_chord_og = j
   dtn_chord = dtn_chord_og - 1
   
   #Generate chords
   chord = []
   for i in range(dtn_chord,dtn_chord + 5,2):
      chord.append(root + scale[i])
   
   #randomize inversion  
   #random.shuffle(chord)
   print(chord[0])
   
   if random() < 0.25: #we only want to randomly invert quarter the time
      inversion = randint(0,3) #random inversion, if 0, invert first note (pitch up 12). if 2, invert last (pitch down)
      if inversion == 0:
         chord[0] += 12
         print(chord[0])
      elif inversion == 2:
         chord[2] -= 12
   

   chord_prog.append(chord)
   
   #Generate melody
   #get durations, we are essentiall marrying two half measure together
   duration = choice(durations)
   duration2 = choice(durations)
   duration = duration + duration2
   
   for i in range(len(duration)):
      #determine pitch based on tonic/sub/dominate
      if dtn_chord_og in [1, 3]: #tonic
         pitch = choice([root + x for x in tonic])
      elif dtn_chord_og in [2, 4, 6]: #sub dominate
         pitch = choice([root + x for x in sub_dom])
      else: #dominate
         pitch = choice([root + x for x in dom])
      #print pitch
      note = Note(12 + pitch, duration[i])
      notes.append(pitch)
      mel.addNote(note)
      
   
   #generate bass
   note = Note(chord[0] - 12, WN, 120)
   bass.addNote(note)

# add chords to progression
for chord in chord_prog:
   #print chord
   phr.addChord(chord, WN)
   

Mod.repeat(bass, 2)
bassPart.addPhrase(bass)
   
Mod.repeat(phr, 2)
part.addPhrase(phr)

# add melody to progression
#add to part
Mod.repeat(mel,2)
part.addPhrase(mel)



score.addPart(bassPart)
score.addPart(part)


# Print to see

#print chord_prog
#print notes


#DRUMS

#measures to play
measures = len(diatonic_prog)

#bass
for i in range(2*measures):
   dynamics = randint(80,110)
   n = Note(ACOUSTIC_BASS_DRUM, HN, dynamics)
   bassDrumPhrase.addNote(n)
   

#snare
for i in range(2*measures):
   r = Note(REST, QN)
   snareDrumPhrase.addNote(r)
   
   dynamics = randint(60,80)
   n = Note(SNARE, QN, dynamics)
   snareDrumPhrase.addNote(n)
   
#hats

comeAlive = 0.15 #35% of the time we play an open hi hat sound instead of closed

for i in range(8*measures):
   # if the modulo of i divided by 2 is 1, we are at an odd hit
   # (if it is 0, we are at an even hit)
   oddHit = i%2 == 1
   
   # time to come alive?
   doItNow = random() < comeAlive
   
   # let's give some life to the hi-hats
   if oddHit and doItNow: #on odd hits, if it's time to do it,
      pitch = OPEN_HI_HAT #let's open the hi-hat
   else: #otherwise,
      pitch = CLOSED_HI_HAT #keep it closed
      
   
   #also add dynamics
   dynamics = randint(80,110)
   
   #create note
   n = Note(pitch, SN, dynamics)
   hiHatPhrase.addNote(n)
   
   #create rest
   r = Note(REST, SN)
   hiHatPhrase.addNote(r)
   

#combine drum parts
Mod.repeat(bassDrumPhrase, 2)
Mod.repeat(snareDrumPhrase, 2)
Mod.repeat(hiHatPhrase, 2)
drumsPart.addPhrase(bassDrumPhrase)
drumsPart.addPhrase(snareDrumPhrase)
drumsPart.addPhrase(hiHatPhrase)
score.addPart(drumsPart)


#Play midi
Play.midi(score)



'''
# random melody (divorced from chords in chord prog)

mel = Phrase(0.0)
mel.setInstrument(ACOUSTIC_GUITAR)

durations = [QN, DEN, EN, SN]
#durations = [EN]


numNotes = randint(12, 18)
#numNotes = (len(chord_prog) - 2)*4

#add first note
note = Note(root, QN)
mel.addNote(note)


notes = [] #for testing output

#- 2 because we want the first and last to end on root note
for i in range(numNotes - 2):
   pitch = choice([root + x for x in scale])
   #print pitch
   duration = choice(durations)
   note = Note(pitch, duration)
   notes.append(pitch)
   mel.addNote(note)

#add last note
note = Note(root, HN)
mel.addNote(note)

#add to part
part.addPhrase(mel)

print [root + x for x in scale]
print list(set(notes))
'''





# COPY OF CHORD PROGRESSION GENERATOR CODE THAT WORKS
'''
#Create chord progression
chord_prog = []
for j in diatonic_prog:

   #diatonic chord you want to play:
   dtn_chord = j
   dtn_chord -= 1
   
   #Generate chords
   chord = []
   for i in range(dtn_chord,dtn_chord + 5,2):
      chord.append(root + scale[i])
      
   chord_prog.append(chord)

# add chords to progression
for chord in chord_prog:
   print chord
   phr.addChord(chord, HN)
part.addPhrase(phr)
'''

