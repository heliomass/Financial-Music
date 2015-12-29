/* PlayMusic Class
 * By Daniel Demby
 * dd20@hw.ac.uk
 */

import javax.sound.midi.*;

public class PlayMusic
{
	
	// The maximum and minimum speeds
	private static final int MAX_TEMPO = 240;
	private static final int MIN_TEMPO = 40;
	
	// Note representations.
	public static final int NOTE_C = 0;
	public static final int NOTE_D = 2;
	public static final int NOTE_E = 4;
	public static final int NOTE_F = 5;
	public static final int NOTE_G = 7;
	public static final int NOTE_A = 9;
	public static final int NOTE_B = 11;
	
	public static final int NOTE_HOLD = -2;
	public static final int NOTE_REST = -3;
	
	public static final int NOTE_INVALID = -1;
	
	// Sets the default tempo (in BPM) that the music will play at.
	private static final int TEMPO = 120;
	
	// Some statics to represent the available musical instruments.
	private static final int INSTRUMENT_PIANO = 1;
	private static final int INSTRUMENT_PIANO_BRIGHT = 2;
	private static final int INSTRUMENT_GLOCKENSPIEL = 10;
	private static final int INSTRUMENT_HAMMOND = 17;
	private static final int INSTRUMENT_VIOLIN = 41;
	private static final int INSTRUMENT_VIOLA = 42;
	private static final int INSTRUMENT_CELLO = 43;
	private static final int INSTRUMENT_STRINGS = 50;
	
	// Some instrument schemes
	private static final int INSTRUMENT_SCHEME_PIANOS = 1;
	private static final int INSTRUMENT_SCHEME_PIANO_AND_STRINGS = 2;
	private static final int INSTRUMENT_SCHEME_ORCHESTRA = 3;
	
	// The delay between notes.
	private int delay;
	
	// The synthesiser we will use to play the notes.
	private Synthesizer synth;
	
	// An array containing several note sequences to be played
	// concurrently.
	int[][] noteSequence;
	
	// The maximum number of notes in the sequence;
	int numberOfNotes;
	
	// Factory method to create an instance
	public static PlayMusic playMusicDirect(int[][] theNoteSequence, int theTempo, int theInstrumentScheme)
	{
		
		PlayMusic music = new PlayMusic(theNoteSequence, theTempo, theInstrumentScheme);
		
		return music;
		
	}
	
	// Class' constructor.
	private PlayMusic(int[][] theNoteSequence, int theTempo, int theInstrumentScheme)
	{
		
		// Set the notes for the sequence.
		noteSequence = theNoteSequence;
		
		// Work out the maximum length of the 'song'.
		numberOfNotes = getNumberOfNotes(noteSequence);
		
		// Get the delay needed between playing notes.
		delay = getDelayFromTempo(theTempo);
		
		// Prepare the synth for use.
		setupSynth();

		// Get a full list of available channels from the synth.
		final MidiChannel[] channels = synth.getChannels();
	
		// Access the synth's soundbank to get a list of available instruments
		Instrument[] instruments = synth.getDefaultSoundbank().getInstruments();
		
		// Remembers the last note played in each of the channels.
		// This is used for holding notes down.
		// (remember that noteSequence.length tells us the
		// number of channels)
		int[] lastNotePlayed = new int[noteSequence.length];
	   
		// Load the synths with an instrument.
		if (theInstrumentScheme == INSTRUMENT_SCHEME_PIANO_AND_STRINGS) {
			channels[0].programChange(INSTRUMENT_PIANO);
			channels[1].programChange(INSTRUMENT_PIANO);
			channels[2].programChange(INSTRUMENT_STRINGS);
			channels[3].programChange(INSTRUMENT_STRINGS);
			channels[4].programChange(INSTRUMENT_STRINGS);
		} else if (theInstrumentScheme == INSTRUMENT_SCHEME_ORCHESTRA) {
			channels[0].programChange(INSTRUMENT_CELLO);
			channels[1].programChange(INSTRUMENT_VIOLA);
			channels[2].programChange(INSTRUMENT_STRINGS);
			channels[3].programChange(INSTRUMENT_STRINGS);
			channels[4].programChange(INSTRUMENT_STRINGS);
		} else
			for (int i = 0; i < noteSequence.length; i++)
				channels[i].programChange(INSTRUMENT_PIANO);
	
		// Play the song!
		for (int i = 0; i < numberOfNotes; i++) {
		
			for (int j = 0; j < noteSequence.length; j++) {
		
				// Play the next note in the sequence.
				if (i < noteSequence[j].length)
					if (noteSequence[j][i] != NOTE_HOLD)
						channels[j].noteOn(noteSequence[j][i], 200);
				
				// Turn off the previous note if a new note is being
				// played in this channel.
				if (i < noteSequence[j].length)
					if (i > 0)
						if (noteSequence[j][i] != NOTE_HOLD)
							channels[j].noteOff(lastNotePlayed[j], 200);
				
				// Turn off the previous note if there is an instruction
				// to release it.
				if (i < noteSequence[j].length)
					if (noteSequence[j][i] == NOTE_REST)
						channels[j].noteOff(lastNotePlayed[j], 200);
				
				// Remember the last note.
				if (i < noteSequence[j].length)
					if (noteSequence[j][i] >= 0)
						lastNotePlayed[j] = noteSequence[j][i];
				
				// If we've played the last note of a channel's sequence, then
				// release the note in that channel.
				if (i == noteSequence[j].length) {
					channels[j].noteOff(lastNotePlayed[j], 200);
					System.out.println("release " + j);
				}
		
			}
			
			// Pause for the amount of time as determined by the tempo
			pause(delay);
		
		}
		
		// Stop notes playing on all the channels.
		for (int i = 0; i < noteSequence.length; i++)
			channels[i].allNotesOff();
		
		// Pause for a beat tp allow the notes to be released
		// and their sustain to ring out naturally.
		// This sounds better than the notes just cutting out
		// as sound channel is killed.
		pause(delay * 4);
		
		// Close the synth off.
		closeSynth();
		
	}
	
	// Work out the maximum number of notes in the sequence
	// (ie, to make sure we keep plaing until the channel with
	// the most notes to play has finished its sequence)
	private int getNumberOfNotes(int[][] theNoteSequence)
	{
		
		// Start with the max number of notes set to 0.
		int theNumberOfNotes = 0;
		
		// Now we loop through all the tracks, upping theNumberOfNotes
		// to always be the length of the longest track so far.
		for (int i = 0; i < theNoteSequence.length; i++) {
			
			if (theNoteSequence[i].length > theNumberOfNotes)
				theNumberOfNotes = theNoteSequence[i].length;
			
		}
		
		return theNumberOfNotes;
		
	}
	
	// Prepares the synth to play notes.
	private void setupSynth()
	{

		try {
		
			// Ask Java to get us a synth to play around with.
			synth = MidiSystem.getSynthesizer();
	
			// Open the synth up for input.
			synth.open();
			
		}
		
		catch (MidiUnavailableException ex) {
			
			System.err.println(ex.getMessage());
			System.exit(1);
				
		}
		
	}
	
	// Turns off the synth once we're done.
	private void closeSynth()
	{
		
		// Put the synth away in the cupboard.
		synth.close();
		
	}
	
	// Gets the delay needed between notes from the BPM supplied.
	private int getDelayFromTempo(int theTempo)
	{
		
		// Limit the tempo to be between 40 and 240 BPM.
		if (theTempo < MIN_TEMPO)
			theTempo = 40;
		else if (theTempo > MAX_TEMPO)
			theTempo = 240;
		
		// Calculate the delay between notes from the BPM.
		float theDelay = ((60 / (float)theTempo) * 1000) / 2;
		
		// Return the delay via some horrible casting.
		return (int)theDelay;
		
	}
	
	// Pauses between beats.
	private void pause(int theDelay)
	{
		
		try {
			Thread.sleep(theDelay);
		}
		
		catch (InterruptedException ex)
		{
			System.err.println(ex.getMessage());
			System.exit(1);
		}
		
	}
	
	public static void test(int[][] test)
	{
		
		System.out.println("OK");	
		
	}

}
