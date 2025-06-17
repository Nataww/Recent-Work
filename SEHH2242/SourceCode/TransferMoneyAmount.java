import java.awt.event.ActionListener;
import javax.swing.JTextField;
import javax.swing.JButton;
import javax.swing.JPanel;
import java.awt.event.ActionEvent;



public class TransferMoneyAmount extends MainScreen implements ActionListener{
    private JTextField transferMoneyAmount;
    public TransferMoneyAmount(String getFileName) {
        super(getFileName);
    } //end method TransferMoneyAmount

    public String getTransferMoneyAmount() {
        return transferMoneyAmount.getText();
    } //end method getTransferMoneyAmount

    @Override
    public void screenCenter(JButton[] centerButton, JPanel panel){

        transferMoneyAmount = getTextField("",false,(screenWidth-309)/2, 300, 605/2, 32);
        panel.add (transferMoneyAmount);
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
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "00" : 
                //Input text to TextFeild
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "." :
                //Input text to TextFeild
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "7" :
                //Input text to TextFeild
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "8" :
                //Input text to TextFeild
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "9" :
                //Input text to TextFeild
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "6" :
                //Input text to TextFeild
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "5" :
                //Input text to TextFeild
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "4" :
                //Input text to TextFeild
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "3" :
                //Input text to TextFeild
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "2" :
                //Input text to TextFeild
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "1" :
                //Input text to TextFeild
                transferMoneyAmount.setText(transferMoneyAmount.getText().concat( event.getActionCommand() ));
                break;

            case "Enter":
                //go to next page
                waitingEnter = false;
                dispose();

                break;
            case "Change" :
                //reset amount textfeild
                transferMoneyAmount.setText("");
                break;

            case "Cancel" :
                //cancel, go to main menu
                new MainMenuScreen("MainMenu.png");
                dispose();
                break;
        }

    } // end method actionPerformed

}

