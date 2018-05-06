# stringtranscribe
<b> A simple class to transcribe and visualize music across stringed instruments. </b>

Imagine you're playing music with an unconventional ensemble made up of an electric bass guitar, 5-string electric octave mandolin, and a lap steel guitar in C6 tuning. Outside of the most basic chords, odds are that you and your friends are not going to have a clear way of of communicating songs to one another. To further complicate things, casual musicians may only be familiar with one type notation (say, tabulature) further constraining the ability of the group to learn new songs.

The purpose of this repository is to provide a way to transcribe music across a wide variety of stringed instruments. By visualizing notes directly on the fretboard of the musician's instrument it attempts to facilitate the exploration of more nuanced harmony when learning compositions. It also allows musicians to choose the notation that suits their learning best.

Fidelity to the harmonic structure of a song is expressed by the concept of [_raag_](https://en.wikipedia.org/wiki/Raga) within the context of Indian classical music:
>"A harmonious note, melody, formula, or building block of music available to a musician to construct a state of experience in the audience."


## A note on the color scheme

Throughout this module I use a color scheme that leverages the agreement between the chromatic scale in music and the chromatic color wheel in pigments, both of which have twelve values. The module allows for use of either [letter notation](https://en.wikipedia.org/wiki/Letter_notation) or [integer notation](https://en.wikipedia.org/wiki/Pitch_class#Integer_notation), where "C" = 0. 

To maximize contrast in the plots, progressive colors of the chromatic color wheel are assigned to progressive notes of [the circle of 5ths](https://en.wikipedia.org/wiki/Circle_of_fifths) - each representing seven steps of the chromatic scale:

<img src="https://github.com/dbetchkal/stringtranscribe/blob/master/static/ColorNotationWheel_altScheme.png" width="400">


## The `Instrument` class

We begin using the module by initializing an instrument. 

For now, instruments are assumed to have:

- a fingerboard (_fretted or not_) with a certain range of positions that the musician prefers to use
- a certain number of strings, each with a specific tuning

Here's how you would initialize an acoustic guitar tuned to [Open C tuning](https://en.wikipedia.org/wiki/Open_C_tuning) using letter notation:
```
openC_guitar = Instrument(num_frets = 14, tuning = ["C", "G", "C", "E", "G", "C"], notation = "letter")
```

This one's a fiddle, where the player is only using the 1st, 2nd, and 3rd positions:
```
fiddle = Instrument(num_frets = 10, tuning = ["G", "D", "A", "E"], notation = "letter")
```

---

Since the guitar is in a major open tuning we know one obvious way to play a 'D' chord is to barre across the 2nd fret.
But what other ways of voicing 'D' are available?  Knowing the letter names of the notes in a 'D' chord we can use the `.raag()` method to find out:
```
openC_guitar.raag(["D","F#","A"])
```
<img src="https://github.com/dbetchkal/stringtranscribe/blob/master/static/D_chord-OpenC_guitar_letter.png" width="1200">

Quite a few playable possibilities! <br><br>

It turns out we can return the same information _even if we didn't know the note names in a 'D' chord_. Instead we can use our pre-existing knowledge of the 2nd fret barre chord to provide alternative fingerings. We convert from [tabulature](https://en.wikipedia.org/wiki/Tablature) to letter notation using the `.tabToLetter()` method:

```
openC_guitar.raag(openC_guitar.tabToLetter([2, 2, 2, 2, 2, 2]))
```
<img src="https://github.com/dbetchkal/stringtranscribe/blob/master/static/D_chord-OpenC_guitar_letter.png" width="1200">

---

Now, what can the fiddler play that would sound good along with the guitar?  Any notes the guitar is playing might be a good start (others _could_ work within the harmonic structure of the song, but this module can't suggest those!) Use `.raag()` to transfer the letter notes from the guitar onto the fiddle fingerboard:

```
fiddle.raag(openC_guitar.tabToLetter([2, 2, 2, 2, 2, 2]))
```
<img src="https://github.com/dbetchkal/stringtranscribe/blob/master/static/D_chord-fiddle_letter.png" width="800">

---

The real power of this tool is when performance involves a great deal of fidelity to a subtle chord progression. Take for instance the following chord (a _C11 with no 5th_ - not exactly the kind of chord you shout out on the fly.):
```
openC_guitar.raag(openC_guitar.tabToLetter([0, 9, 10, 8, 10, "x"]))
```
<img src="https://github.com/dbetchkal/stringtranscribe/blob/master/static/unknown_chord-OpenC_guitar.png" width="1200">

<br><br>

Here are the same notes mapped onto the neck of a lap steel guitar in C6 tuning:
```
steelGuitar = Instrument(24, [0, 4, 7, 9, 0, 4])
steelGuitar.raag(openC_guitar.tabToLetter([0, 9, 10, 8, 10, "x"]))
```
<img src="https://github.com/dbetchkal/stringtranscribe/blob/master/static/unknown_chord-lapsteelC6.png" width="1200">

Lots of choices for moving counter-melody!
