# stringtranscribe
<b> A simple class to transcribe and visualize music across stringed instruments. </b>

Imagine you're playing music with an unconventional ensemble made up of an electric bass guitar, 5-string electric octave mandolin, and a lap steel guitar in C-6 tuning. Outside of the most basic chords, odds are that you and your friends are not going to have a clear way of of communicating songs to one another. To further complicate things, casual musicians may only be familiar with one type notation (say, tabulature) further constraining the ability of the group to learn new songs.

The purpose of this repository is to provide a way to transcribe music across a wide variety of stringed instruments. By visualizing notes directly on the fretboard of the musician's instrument it attempts to facilitate the exploration of more nuanced harmony when learning compositions. notation that suits them best.

## A note on the color scheme

Throughout this module I use a color scheme that utilizes the agreement between the chromatic scale (in music) and the chromatic color wheel (in pigments) - both of which have twelve values. The module allows for both [alpha (i.e., letter) notation](https://en.wikipedia.org/wiki/Letter_notation) as well as [integer notation](https://en.wikipedia.org/wiki/Pitch_class#Integer_notation), where "C" = 0. 

To maximize contrast in the plots, progressive colors of the chromatic color wheel are assigned to progressive notes of [the circle of 5ths](https://en.wikipedia.org/wiki/Circle_of_fifths) - each representing seven steps of the chromatic scale:

<img src="https://github.com/dbetchkal/stringtranscribe/blob/master/static/ColorNotationWheel.png" width="400">


## The `Instrument` class

We begin using the module by initializing an instrument. 

For now, instruments are assumed to have:

- a fingerboard (_fretted or not_) with a certain number of positions that the musician prefers to use
- a certain number of strings, each with a specific tuning

This one's an acoustic guitar tuned to a common blues tuning, [Open C](https://en.wikipedia.org/wiki/Open_C_tuning):
```
openC_guitar = Instrument(num_frets = 14, tuning = ["C", "G", "C", "E", "G", "C"])
```

This one's a fiddle, where the player is only using the 1st, 2nd, and 3rd positions:
```
fiddle = Instrument(num_frets = 10, tuning = ["G", "D", "A", "E"])
```


Since the guitar is in a major open tuning we know one obvious way to play a 'D' chord is to barre across the 2nd fret.
But what other ways of voicing 'D' are available?  Knowing the letter names of the notes in a 'D' chord we can use the [`raag()`](https://en.wikipedia.org/wiki/Raga) method to find out:
```
openC_guitar.raag(["D","F#","A"])
```
<img src="https://github.com/dbetchkal/stringtranscribe/blob/master/static/D_chord-OpenC_guitar.png" width="800">

Quite a few playable possibilities!

It turns out we can return the same information _even if we didn't know the note names in a 'D' chord_. Instead we can use our pre-existing knowledge of the 2nd fret barre chord to provide alternative fingerings. We convert from [tabulature](https://en.wikipedia.org/wiki/Tablature) to alpha notation using the `tabToAlpha()` method:

```
openC_guitar.raag(openC_guitar.tabToAlpha([2, 2, 2, 2, 2, 2]))
```
<img src="https://github.com/dbetchkal/stringtranscribe/blob/master/static/D_chord-OpenC_guitar.png" width="800">


Take for example the following chord on a 

0, 9, 10, 8, 10, x
