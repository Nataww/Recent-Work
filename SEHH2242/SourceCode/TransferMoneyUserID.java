import javax.swing.JTextField;
import java.awt.event.ActionListener;
import javax.swing.JPanel;
import javax.swing.JButton;
import java.awt.event.ActionEvent;

public class TransferMoneyUserID extends MainScreen implements ActionListener{

    private JTextField transferMoneyUserID;

    public TransferMoneyUserID(String getFileName) {
        super(getFileName);
    }

    public String getTransferMoneyUserID() {
        return transferMoneyUserID.getText();
    } // end method getTransferMoneyUserID

    @Override
    public void screenCenter(JButton[] centerButton, JPanel panel){

        transferMoneyUserID = getTextField("",false,(screenWidth-309)/2, 300, 605/2, 32) ;
        panel.add (transferMoneyUserID);
        //end of Center
    } // end method screenCenter

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
    } // end method waiting

    @Override
    public void actionPerformed( ActionEvent event )
    {
        switch (event.getActionCommand())
        {
            case "0" : 
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "00" : 
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "." :
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "7" :
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "8" :
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "9" :
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "6" :
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "5" :
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "4" :
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "3" :
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "2" :
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "1" :
                //Input text to TextFeild
                transferMoneyUserID.setText(transferMoneyUserID.getText().concat( event.getActionCommand() ));
                break;

            case "Enter":
                //next page
                waitingEnter = false;
                dispose();   
                break;
            case "Change" :
                //reset Textfeild
                transferMoneyUserID.setText("");
                break;

            case "Cancel" :
                //cancel, return main menu
                new MainMenuScreen("MainMenu.png");
                dispose();
                break;
        }

    } // end method actionPerformed

}
