import java.io.*;

public class AccountReader {

	static final int PARAMETER_SIZE = 5;
	
	// Array for the column headings from the files
	private String [] columnHeadings;
	
	// The account data from each of the two years
	private float [] f1ColumnContents;
	private float [] f2ColumnContents;
	
	// The locations of the two files
	private static final String ACCOUNT_FILE_1 = "default1.csv";
	private static final String ACCOUNT_FILE_2 = "default2.csv";
	
	// Positions in the array of specific account items
	private static final int CURRENT_ASSETS = 0;
	private static final int TOTAL_ASSETS = 1;
	private static final int CURRENT_LIABILITIES = 2;
	private static final int TOTAL_LIABILITIES = 3;
	private static final int TOTAL_EQUITY = 4;
	
	
	public static AccountReader newAccountReader()
	{
		
		return new AccountReader(ACCOUNT_FILE_1, ACCOUNT_FILE_2);
		
	}
	
	public static AccountReader newAccountReader(String accountFile1, String accountFile2)
	{
		
		return new AccountReader(accountFile1, accountFile2);
		
	}
	
	
	private AccountReader(String accountFile1, String accountFile2)
	{
		
		System.out.println("Using \"" + accountFile1 + "\" and \"" + accountFile2 + "\".");
		
		// Temporary place holders for the file contents
		String f1Headings = null;
		String f2Headings = null;
		String f1Contents = null;
		String f2Contents = null;
		
		// Read in the two files using two seperate file readers, one for each csv file
		try {
		
			FileReader file1 = new FileReader(accountFile1);
			FileReader file2 = new FileReader(accountFile2);
			
			BufferedReader file1Reader = new BufferedReader(file1);
			BufferedReader file2Reader = new BufferedReader(file2);
			
			f1Headings = file1Reader.readLine();
			f1Contents = file1Reader.readLine();
			f2Headings = file2Reader.readLine();
			f2Contents = file2Reader.readLine();
			
			file1Reader.close();
			file2Reader.close();
			
			file1.close();
			file2.close();
			
		} catch (Exception ex) {
			System.err.println("There was an error reading in the files.");
			ex.printStackTrace();
			System.exit(1);
		}
		
		// Split all these strings into arrays
		String f1HeadingsSplit[] = f1Headings.split(",");
		String f1ContentsSplit[] = f1Contents.split(",");
		String f2HeadingsSplit[] = f2Headings.split(",");
		String f2ContentsSplit[] = f2Contents.split(",");
		
		// Check that the number of headings in each file is identical
		if (f1HeadingsSplit.length != f2HeadingsSplit.length) {
			System.err.println("Account data does not match.");
			System.exit(1);
		}
		
		// Check that the number of content items in each file is identical
		if (f1ContentsSplit.length != f2ContentsSplit.length) {
			System.err.println("Account data does not match.");
			System.exit(1);
		}
		
		// Check that the headings of both files are identical
		for (int i = 0; i < f1HeadingsSplit.length; i++) {
			if ( !f1HeadingsSplit[i].equalsIgnoreCase(f2HeadingsSplit[i]) ) {
				System.err.println("Account headings do not match.");
				System.exit(1);
			}
		}
		
		// Store the column headings
		columnHeadings = f1HeadingsSplit;
		
		// Store the accounts of file 1 as an integer array
		f1ColumnContents = new float[f1ContentsSplit.length];
		for (int i = 0; i < f1ContentsSplit.length; i++) {
			try {
				f1ColumnContents[i] = Float.valueOf(f1ContentsSplit[i]);
			} catch (NumberFormatException ex) {
				System.out.println(ex.getMessage());
				System.exit(1);
			}
		}
			
		// Store the accounts of file 2 as an integer array
		f2ColumnContents = new float[f2ContentsSplit.length];
		for (int i = 0; i < f2ContentsSplit.length; i++) {
			try {
				f2ColumnContents[i] = Float.valueOf(f2ContentsSplit[i]);
			} catch (NumberFormatException ex) {
				System.out.println(ex.getMessage());
				System.exit(1);
			}
		}
		
		// Check that everything balances out correctly
		if (!checkBalance(getColumn1())) {
			System.out.println("Warning: File 1's accounts do not balance.");
			//System.exit(1);
		}
		else {
			if (!checkBalance(getColumn2())) {
				System.out.println("Warning: File 2's accounts do not balance.");
				//System.exit(1);
			}
			else {
				System.out.println("Accounts balance.");
			}
		}
		
	}
	
	// Accessor to return an array of headings
	public String[] getHeadings()
	{
		
		return columnHeadings;
		
	}
	
	// Accessor to return an array of account values from file 1
	public float[] getColumn1()
	{
		
		return f1ColumnContents;	
		
	}
	
	// Accessor to return an array of account values from file 2
	public float[] getColumn2()
	{
		
		return f2ColumnContents;	
		
	}
	
	/*
	 * Validate that balance sheet correctly balances
	 *
	 * The below method expects each file to have been in the format:
	 * Current Assets,Total Assets,Current Liabilities,Total Liabilities,Total Equity
	 *
	 * Therefore, Total Assets = Total Liabilities + Total Equity
	 *
	 */
	public boolean checkBalance(float[] accountData)
	{
		
		boolean balanceResult = (accountData[TOTAL_ASSETS] == accountData[TOTAL_LIABILITIES] + accountData[TOTAL_EQUITY]);
		
		return balanceResult;
		
	}
	
	// main() method should we wish to just test the workings of this module
	public static void main(String[] args)
	{
		
		AccountReader fp = newAccountReader();
		
		if (!fp.checkBalance(fp.getColumn1()))
			System.out.println("File 1's accounts do not balance.");
		else if (!fp.checkBalance(fp.getColumn2()))
			System.out.println("File 2's accounts do not balance.");
		else
			System.out.println("Accounts balance.");
		
	}

}



















