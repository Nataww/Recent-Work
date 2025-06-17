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


public class ViewBalanceScreen extends MainScreen {
    private JTextField viewAvailableBalance;
    private JTextField viewTotalBalance;
    private boolean waitingEnter = true;
    private int accountNumber;
    private double availableBalance;
    private double totalBalance;

    public ViewBalanceScreen(String getFileName) {
        super(getFileName);

        // get the available balance for the account involved
         availableBalance = bankDatabase.getAvailableBalance( getAccount() );
         viewAvailableBalance.setText(Double.toString(availableBalance));

        // get the total balance for the account involved
         totalBalance = bankDatabase.getTotalBalance( getAccount() );
         viewTotalBalance.setText(Double.toString(totalBalance));

    } //end method ViewBalanceScreen


    @Override
    public void screenCenter(JButton[] centerButton, JPanel panel){
        viewAvailableBalance = getTextField("",false,(screenWidth)/2+25, 167, 248, 32);
        panel.add (viewAvailableBalance);
        
        viewTotalBalance = getTextField("",false,(screenWidth)/2-30, 260, 605/2, 32);
        panel.add (viewTotalBalance);
        //end of Center
    } //end method screenCenter

    public void waiting() { 
        while(waitingEnter) {
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
    public void actionPerformed( ActionEvent event )
    {
        switch (event.getActionCommand())
        {
            case "Enter":
                //go to main menu
                new MainMenuScreen("MainMenu.png");
                dispose();
                break;
        }
    } // end method actionPerformed    
}

