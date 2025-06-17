import javax.swing.JTextField;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import javax.swing.JPanel;
import java.awt.event.ActionEvent;


public class confirmWithdrawalScreen extends MainScreen implements ActionListener{
    private JTextField withdrawlAmountText;
    private int withdrawlAmount;
    

    public confirmWithdrawalScreen(String getFileName, int withdrawalAmount) {
        super(getFileName);
        this.withdrawlAmount = withdrawalAmount;
        withdrawlAmountText.setText(Integer.toString(withdrawlAmount));
    } //end method confirmWithdrawalScreen

    @Override
    public void screenCenter(JButton[] centerButton, JPanel panel){
        withdrawlAmountText = getTextField("",false,(screenWidth-309)/2, 300, 605/2, 32) ;
        panel.add (withdrawlAmountText);
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
            case "0" : 
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "00" : 
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "." :
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "7" :
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "8" :
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "9" :
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "6" :
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "5" :
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "4" :
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "3" :
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "2" :
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "1" :
                //Input text to TextFeild
                withdrawlAmountText.setText(withdrawlAmountText.getText().concat( event.getActionCommand() ));
                break;

            case "Enter":
                //Confirm Withdrawl Amount information is correct
                try {  
                    // update the account involved to reflect withdrawal
                    bankDatabase.debit( getAccount(), withdrawlAmount );

                    cashDispenser.dispenseCash( withdrawlAmount ); // dispense cash

                    new ShowMessageScreen("takeCard.png",false,3, "withdrawlComplete1"); //Please take your cash now.
                    dispose();

                } catch(NumberFormatException e){  

                } 
                break;

            case "Change" :
                //reset Textfield
                withdrawlAmountText.setText("");
                break;

            case "Cancel" :
                //Cancel, go back Main Menu
                new MainMenuScreen("MainMenu.png");
                dispose();
                break;
        }
    } // end method actionPerformed
}
