/**
 * Financial Music GUI
 * By Daniel Demby
 */


import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.*;

public class Gui extends JFrame
{
	// Popup menu for choosing the approach
	JPopupMenu implementationMenu;
	
	// Array of approach options by name
	private final String[] approachOptions = {"Mapping", "Genome"};
	
	// Label to display the current chosen approach
	JLabel approach;
	
	// Button to select the implementation
	JButton implementationButton;
	
	// Fields containing the actual data
	JTextField year1Fields[] = new JTextField[6];
	JTextField year2Fields[] = new JTextField[6];
	
	// Main method
	public static void main(String[] args)
	{
		
		// Brew some coffee
		Coffee coffee = new Coffee();
		
		// Drink some coffee
		coffee.drink();

		// Open a window.
		new Gui().setVisible(true);
		
	}
	
	public Gui()
	{
		
		// Initialize the window
		setSize(800, 600);
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		// Prepare a content area and a layout
		Container contentPane = getContentPane();
		contentPane.setBackground(Color.WHITE);
		SpringLayout layout = new SpringLayout();
		contentPane.setLayout(layout);
		
		// Title
		JLabel title = new JLabel("Financial Music");
		title.setFont(new Font("System", Font.BOLD, 18));
		contentPane.add(title);
		layout.putConstraint(SpringLayout.WEST, title, 20, SpringLayout.WEST, contentPane);
		layout.putConstraint(SpringLayout.NORTH, title, 20, SpringLayout.NORTH, contentPane);
		
		// Approach
		approach = new JLabel();
		setApproach(approachOptions[0]);
		approach.setFont(new Font("System", Font.BOLD, 14));
		contentPane.add(approach);
		layout.putConstraint(SpringLayout.WEST, approach, 20, SpringLayout.WEST, contentPane);
		layout.putConstraint(SpringLayout.NORTH, approach, 160, SpringLayout.NORTH, contentPane);
		
		//.Play button
		JButton playButton = new JButton("Play!");
		playButton.addMouseListener(new MouseListener() {
			
			public void mouseClicked(MouseEvent e) {textDump();}
			public void mouseEntered(MouseEvent e) {}
			public void mouseExited(MouseEvent e) {}
			public void mousePressed(MouseEvent e) {}
			public void mouseReleased(MouseEvent e) {}
			
		});
		contentPane.add(playButton);
		layout.putConstraint(SpringLayout.WEST, playButton, 20, SpringLayout.WEST, contentPane);
		layout.putConstraint(SpringLayout.NORTH, playButton, 60, SpringLayout.NORTH, contentPane);
		
		//.Quit button
		JButton quitButton = new JButton("Quit");
		quitButton.addMouseListener(new MouseListener() {
			
			public void mouseClicked(MouseEvent e) { System.exit(0); }
			public void mouseEntered(MouseEvent e) {}
			public void mouseExited(MouseEvent e) {}
			public void mousePressed(MouseEvent e) {}
			public void mouseReleased(MouseEvent e) {}
			
		});
		contentPane.add(quitButton);
		layout.putConstraint(SpringLayout.WEST, quitButton, 20, SpringLayout.WEST, contentPane);
		layout.putConstraint(SpringLayout.NORTH, quitButton, 120, SpringLayout.NORTH, contentPane);
		
		// Create the drop-down menu
		implementationMenu = new JPopupMenu("Implementation");
		
		// Add the items to the drop-down menu
		for (String s : approachOptions) {
			
			final String sClone = s;
			
			JMenuItem implementationOption = new JMenuItem(s);
			implementationMenu.add(implementationOption);
			
			implementationOption.addActionListener(new ActionListener() {
				
				public void processMouseEvent(MouseEvent action)
				{
					if(action.isPopupTrigger())
						implementationMenu.show(action.getComponent(), action.getX(), action.getY());

					processMouseEvent(action);
				}

				
				public void actionPerformed(ActionEvent action) {
					setApproach(sClone);
					showImplementationMenu(false);
				}
				
			});
			
		}
		
		// Implementation button
		implementationButton = new JButton("Implementation");
		implementationButton.addMouseListener(new MouseListener() {
			
			public void mouseClicked(MouseEvent e) {}
			public void mouseEntered(MouseEvent e) {}
			public void mouseExited(MouseEvent e) {}
			public void mousePressed(MouseEvent e) {
				if (!implementationMenu.isVisible()) {
					updateMenuLocation();
					showImplementationMenu(true);
				}
				else
					showImplementationMenu(false);
			}
			public void mouseReleased(MouseEvent e) {  }
			
		});
		contentPane.add(implementationButton);
		layout.putConstraint(SpringLayout.WEST, implementationButton, 180, SpringLayout.WEST, contentPane);
		layout.putConstraint(SpringLayout.NORTH, implementationButton, 60, SpringLayout.NORTH, contentPane);
		
		contentPane.add(implementationMenu);
		
		// Add some fields for entering data into
		for (int i = 0; i < 6; i++)
		{
			
			year1Fields[i] = new JTextField(10);
			contentPane.add(year1Fields[i]);
			layout.putConstraint(SpringLayout.WEST, year1Fields[i], 20, SpringLayout.WEST, contentPane);
			layout.putConstraint(SpringLayout.NORTH, year1Fields[i], 200 + (i * 30), SpringLayout.NORTH, contentPane);
			
			year2Fields[i] = new JTextField(10);
			contentPane.add(year2Fields[i]);
			layout.putConstraint(SpringLayout.WEST, year2Fields[i], 300, SpringLayout.WEST, contentPane);
			layout.putConstraint(SpringLayout.NORTH, year2Fields[i], 200 + (i * 30), SpringLayout.NORTH, contentPane);
			
		}
		
		// Finalize the window for display
		pack();
		
	}
	
	private void updateMenuLocation()
	{
		
		Point loc = this.getLocation();
		loc.translate((int)implementationButton.getLocation().getX(), (int)implementationButton.getLocation().getY() + 40);
		
		implementationMenu.setLocation(loc);
		
	}
	
	private void showImplementationMenu(boolean state)
	{
		
		implementationMenu.setVisible(state);
		
	}
	
	private void setApproach(String newApproach)
	{
		
		approach.setText("Chosen Algorithm: " + newApproach);
		
	}
	
	private void textDump()
	{
		
		System.out.println("Column 1\n=====");
		for (JTextField e : year1Fields) {
			
			System.out.println(e.getText());
			
		}
		
		System.out.println("\nColumn 2\n=====");
		for (JTextField e : year2Fields) {
			
			System.out.println(e.getText());
			
		}
		
	}
	
}

class Coffee
{
		
	// Brew some coffee
	public Coffee() {}
		
	// Drink the coffee
	public boolean drink()
	{
			
		Random generator = new Random();
		
		boolean tooHot = (generator.nextInt(20) == 1);
		boolean choke = (generator.nextInt(100) == 1);
		
		return (!(tooHot || choke));
			
	}
		
}