import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JPanel;
import java.awt.event.ActionEvent;

public class WithdrawalMenuScreen extends MainScreen implements ActionListener{

    public WithdrawalMenuScreen(String getFileName) {
        super(getFileName);
    } //end method WithdrawalMenuScreen
    
    @Override
    public void screenCenter(JButton[] centerButton, JPanel panel){

        //end of Center
    } //end method screenCenter

    @Override
    public void actionPerformed( ActionEvent event )
    {
        switch (event.getActionCommand())
        {
            case "L1" : 
                //Withdrawal $100
                new FixedAmountWithdrawalScreen("Withdrawal100.png",100);
                dispose();
                break;
            case "L2" : 
                //Withdrawal $500
                new FixedAmountWithdrawalScreen("Withdrawal500.png",500);
                dispose();
                break;
            case "L3" : 
                //Withdrawal $1000
                new FixedAmountWithdrawalScreen("Withdrawal1000.png",1000);
                dispose();
                break;
            case "R1" : 
                //Custom Withdrawal Amount
                new CustomWithdrawalScreen("customWithdrawal.png");
                dispose();
                break;
            case "R3" : 
                //Cancel, go back Main Menu
                new MainMenuScreen("MainMenu.png");
                dispose();
                break;
            case "Cancel":
                //Cancel, go back Main Menu
                new MainMenuScreen("MainMenu.png");
                dispose();
                break;
        }
    } // end method actionPerformed
}
