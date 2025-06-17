import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JPasswordField;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.BorderLayout;
import javax.swing.JOptionPane;
import java.awt.GridLayout;
import javax.swing.ImageIcon;
import javax.swing.Icon;
import javax.swing.JFrame;
import java.awt.*;
import javax.swing.Timer;

public class ShowMessageScreen extends MainScreen implements ActionListener
{
    private JLabel background;
    private JButton button;
    private boolean endProgram = false; 
    private int delayMS = 0;
    private String runNext = "";
    private boolean waitingGo = true;

    public ShowMessageScreen(String getFileName, boolean endChoice, int waitingSecond) {
        super(getFileName);
        endProgram = endChoice;
        delayMS = waitingSecond * 1000;
        waitingThenNext(delayMS);
    } //end method ShowMessageScreen
    
    public ShowMessageScreen(String getFileName, boolean endChoice, int waitingSecond, String runNext) {
        super(getFileName);
        endProgram = endChoice;
        delayMS = waitingSecond * 1000;
        this.runNext = runNext;
        waitingThenNext(delayMS);
    }//end method ShowMessageScreen
    
    private void waitingThenNext(int waitingMS) {
        //Create a timer for wait the action
        Timer timer = new Timer(waitingMS, new ActionListener() {
                    public void actionPerformed(ActionEvent e) {
                        if(!endProgram) {
                            switch(runNext) {
                                case "empty":
                                    //do nothing
                                    break;  
                                case "logout":
                                    //call logout
                                    logout();
                                    break;
                                case "withdrawlComplete1":
                                    //Show CardEjected, then next
                                    new ShowMessageScreen("CardEjected.png",false,3, "withdrawlComplete2");
                                    break;
                                case "withdrawlComplete2":
                                    //Show takeCash, then next
                                    new ShowMessageScreen("takeCash.png",false,3, "withdrawlComplete3");
                                    break;
                                case "withdrawlComplete3":
                                    //Show CASHdispensed, then logout
                                    new ShowMessageScreen("CASHdispensed.png",false,3, "logout");
                                    break;
                                default:
                                    //go to main menu
                                    new MainMenuScreen("MainMenu.png");
                                    break;
                            }
                        }
                        waitingGo = false;
                        dispose();             
                        //do once only, so stop timer.
                        ((Timer)e.getSource()).stop();
                    }
                });
        timer.start();
    }// end method waitingThenNext

    public void waiting() { 
        while(waitingGo) {
            try
            {
                Thread.sleep(1);
            }
            catch (InterruptedException ie)
            {
                ie.printStackTrace();
            }
        }
    } //end method waiting
    
    @Override
    public void screenCenter(JButton[] centerButton, JPanel panel){

        //end of Center
    } //end method screenCenter

    @Override
    public void actionPerformed( ActionEvent event )
    {
        switch (event.getActionCommand())
        {

        }
    } // end method actionPerformed
}

