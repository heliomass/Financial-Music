import java.io.*;
import java.util.*;

public class MusicReader {
	
	// The location of the files
	private static final String MUSIC_FILE = "music_output.csv";
	
	private int musicSequence[][];
	
	private int tempo;
	
	private int instrumentScheme;
	
	public MusicReader()
	{
	
		// Temporary place holders for the file contents
		LinkedList <String> fileContents = new LinkedList<String>();
		
		// Read in the files
		try {
			
			FileReader file = new FileReader(MUSIC_FILE);
			
			BufferedReader reader = new BufferedReader(file);
			
			// First line is the tempo
			tempo = Integer.decode(reader.readLine());
			System.out.println(tempo);
			
			// Second line is the instrument sheme
			instrumentScheme = Integer.decode(reader.readLine());
			System.out.println(instrumentScheme);
			
			String nextLine;
			while((nextLine = reader.readLine()) != null) {
			
				if (nextLine != "")
					fileContents.add(nextLine);
				
			}
			
			reader.close();
			
			file.close();
			
		} catch (Exception ex) {
			System.err.println("There was an error reading in the files.");
			ex.printStackTrace();
			System.exit(1);
		}
		
		LinkedList <int[]> values = new LinkedList <int[]> ();
		
		// Split up the file into sections
		for (String e : fileContents) {
			
			String[] splitContents = e.split(",");
			int[] valueSubset = new int[splitContents.length];
			
			int counter = 0;
			for (String f : splitContents) {
				
				valueSubset[counter] = Integer.decode(f);
				counter++;
				
			}
			
			values.add(valueSubset);
			
		}
		
		musicSequence = new int[values.size()][];
		
		for (int i = 0; i < values.size(); i++) {
			
			int[] hold = new int[values.get(i).length];
			
			for (int j = 0; j < values.get(i).length; j++) {
				
				hold = values.get(i);
				
			}
			
			musicSequence[i] = hold;
			
		}
		
		
		
		for (int[] e : musicSequence) {
			for (int f : e) {
				System.out.print(f);
			}
			System.out.print("=");
		}
		System.out.print("/");
		
	}
	
	public static void main(String[] args)
	{
		
		MusicReader seq = new MusicReader();
		PlayMusic play = PlayMusic.playMusicDirect(seq.getMusicSequence(), seq.getTempo(), seq.getInstrumentScheme());
		
	}
	
	public int[][] getMusicSequence()
	{
		
		return musicSequence;
		
	}
	
	public int getTempo()
	{
		
		return tempo;
		
	}
	
	public int getInstrumentScheme()
	{
		
		return instrumentScheme;
		
	}

}



















