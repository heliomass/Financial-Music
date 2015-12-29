/* ReadFile Class
 * By Daniel Demby
 * dd20@hw.ac.uk
 */

import java.io.*;
import java.util.regex.*;
import java.util.*;

public class ReadFile {

	// A file reader.
	private FileReader musicFile;

	// A buffered reader.
	private BufferedReader musicBuffer;

	// Location of input file.
	private String filePath;

	// The current octave.
	private int octave;
	
	// The default/starting octive. We'll set it to middle 'c'.
	private static final int DEFAULT_OCTIVE = 5;

	// Upper octave bound.
	private static final int MAXIMUM_OCTAVE = 11;

	// Our RegEx expression.
	private static final String notesRegEx = "[a-g][FS]?|[HR]|[O][0-9][0-1]?";
	private static final Pattern notesPattern = Pattern.compile(notesRegEx);
	
	// Method to return the contents of a file in a two dimensional
	// array that can be parsed by PlayMusic.
	public int[][] getContents()
	{
		
		// Create temporary storage for all the channels that we
		// will need.
		ArrayList <int[]> channelHolder = new ArrayList <int[]> ();
		
		try {
			
			String line;
			
			while ((line = musicBuffer.readLine()) != null) {
				
				if (line.contains("("))
					channelHolder.add(getSequence());
				
			}
			
		}
		
		catch (IOException ex) {

			System.err.println("An error occurred reading the file: " + ex.getMessage());
			System.exit(1);

		}
		
		// Now, get the ArrayList into an array.
		int outputArray[][] = new int[channelHolder.size()][];
		for (int i = 0; i < outputArray.length; i++)
			outputArray[i] = channelHolder.get(i);
		
		// Close the file.
		closeStream();
		
		return outputArray;
		
	}
	
	// Method to return a sequence of notes for a single channel in
	// the file.
	private int[] getSequence()
	{

		// Temporary storage for the array, as we don't know the final size
		// of the array of notes.
		ArrayList <Integer> noteHolder = new ArrayList <Integer> ();
		
		// Set the octive to the default.
		octave = DEFAULT_OCTIVE;

		System.out.println("* Start of sequence *");

		try {
			
			// Holds the current line being read from the file.
			String line;

			while ((line = musicBuffer.readLine()) != null && !line.contains(")")) {

				Matcher lineMatch = notesPattern.matcher(line);

				while (lineMatch.find()) {

					// Read the next code in the sequence as specified by
					// our RegEx.
					String currentNote = lineMatch.group();

					// Temporary storage for the note's MIDI value.
					int noteCode = PlayMusic.NOTE_INVALID;

					// Check if we're setting an octave
					if (	(currentNote.length() == 2 || currentNote.length() == 3) && 
							currentNote.substring(0, 1).equals("O")) {

						// Get the new octave.
						int octaveChange;

						if (currentNote.length() == 2)
							octaveChange = Integer.parseInt(currentNote.substring(1, 2));
						else if (currentNote.length() == 3)
							octaveChange = Integer.parseInt(currentNote.substring(1, 3));
						else
							octaveChange = octave;

						// Make sure that the new octave is within out bounds.
						if (octaveChange < 1)
							octaveChange = 1;
						else if (octaveChange > MAXIMUM_OCTAVE)
							octaveChange = MAXIMUM_OCTAVE;

						//Set the octave.
						octave = octaveChange;
						
						System.out.println("Octave changed to " + octave);

					}

					// Otherwise, we have note information to parse!
					else {

						// Determine what the note's MIDI value should be.
						if (currentNote.substring(0, 1).equals("a"))
							noteCode = PlayMusic.NOTE_A;
						else if (currentNote.substring(0, 1).equals("b"))
							noteCode = PlayMusic.NOTE_B;
						else if (currentNote.substring(0, 1).equals("c"))
							noteCode = PlayMusic.NOTE_C;
						else if (currentNote.substring(0, 1).equals("d"))
							noteCode = PlayMusic.NOTE_D;
						else if (currentNote.substring(0, 1).equals("e"))
							noteCode = PlayMusic.NOTE_E;
						else if (currentNote.substring(0, 1).equals("f"))
							noteCode = PlayMusic.NOTE_F;
						else if (currentNote.substring(0, 1).equals("g"))
							noteCode = PlayMusic.NOTE_G;
						else if (currentNote.substring(0, 1).equals("H"))
							noteCode = PlayMusic.NOTE_HOLD;
						else if (currentNote.substring(0, 1).equals("R"))
							noteCode = PlayMusic.NOTE_REST;
						else
							noteCode = PlayMusic.NOTE_INVALID;

						// Sharpen or flatten the note if necessary.
						if (noteCode >= 0)
							if (currentNote.length() == 2)
								if (currentNote.substring(1, 2).equals("F"))
									noteCode--;
								else if (currentNote.substring(1, 2).equals("S"))
									noteCode++;

						// Set the noteCode to be in the correct octave.
						if (noteCode >= 0) 
							noteCode = noteCode + ((octave - 1) * 12);

						// Finally, add the note to the array list.
						noteHolder.add(new Integer(noteCode));

						System.out.println(currentNote + " : " + noteCode);

					}

				}
				
			}
			
		}

		catch (IOException ex) {

			System.err.println("An error occurred reading the file: " + ex.getMessage());
			System.exit(1);

		}

		System.out.println("* End of sequence *");
		
		// Now, get the ArrayList into an array.
		int outputArray[] = new int[noteHolder.size()];
		for (int i = 0; i < outputArray.length; i++)
			outputArray[i] = noteHolder.get(i);
		
		return outputArray;
		
	}

	// Class' constructor.
	public ReadFile(String theFilePath)
	{
		
		filePath = theFilePath;

		musicBuffer = getStream(filePath);

	}

	// Create and return a simple buffered text stream from
	// a given file path.
	private BufferedReader getStream(String theFilePath)
	{
		
		try {

			musicFile = new FileReader(theFilePath);

		}

		catch (FileNotFoundException ex) {

			System.err.println("File not found: \"" + theFilePath + "\"");
			System.exit(1);

		}

		musicBuffer = new BufferedReader(musicFile);

		return musicBuffer;

	}

	

	private void closeStream()
	{
		
		try {

			musicBuffer.close();

		}

		catch (IOException ex) {

			System.out.println("Could not close the file buffer: " + ex.getMessage());

		}

		try {

			musicFile.close();

		}

		catch (IOException ex) {

			System.out.println("Could not close the file: " + ex.getMessage());

		}

	}

}