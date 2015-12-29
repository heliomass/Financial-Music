/* SoundTester Class
 * By Daniel Demby
 * dd20@hw.ac.uk
 */

public class SoundTester {
	
	// Path to a default file.
	// Used if the user does not specify their own file.
	private static final String DEFAULT_FILE_PATH = "c:\\default.txt";
	
	// Main method. Works by reading a file's contents using
	// ReadFile, and pipes the output into PlayMusic which then
	// plays it. It does this once, then it exits.
	public static void main(String [] args)
	{
		
		System.out.println("Running...");
		
		/*if (args.length == 0)
			PlayMusic.playMusicDirect(new ReadFile(DEFAULT_FILE_PATH).getContents());
		else
			PlayMusic.playMusicDirect(new ReadFile(args[0]).getContents());*/
			
		//Mapping mapping = new Mapping();
		//System.out.println(mapping.test());
		
		//Mapping.test2();
		
		System.exit(0);
		
	}

}
