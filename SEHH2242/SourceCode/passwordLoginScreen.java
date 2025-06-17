
import javax.swing.JPasswordField;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JPanel;
import java.awt.event.ActionEvent;


public class passwordLoginScreen extends MainScreen implements ActionListener{
    private JPasswordField passwordText;
    

    public passwordLoginScreen(String getFileName) {
        super(getFileName);
    } //end method passwordLoginScreen

    @Override
    public void screenCenter(JButton[] centerButton, JPanel panel){
        passwordText = getPasswordTextField("",false,(screenWidth-309)/2, 300, 605/2, 32);
        panel.add (passwordText);

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
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "00" : 
                //Input text to TextFeild
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "." :
                //Input text to TextFeild
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "7" :
                //Input text to TextFeild
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "8" :
                //Input text to TextFeild
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "9" :
                //Input text to TextFeild
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "6" :
                //Input text to TextFeild
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "5" :
                //Input text to TextFeild
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "4" :
                //Input text to TextFeild
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "3" :
                //Input text to TextFeild
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "2" :
                //Input text to TextFeild
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "1" :
                //Input text to TextFeild
                passwordText.setText(passwordText.getText().concat( event.getActionCommand() ));
                break;

            case "Enter":
                //call next page
                try {  
                    setPassword(Integer.parseInt(passwordText.getText()));
                    waitingEnter = false;
                    dispose();  
                } catch(NumberFormatException e){  

                } 

                break;

            case "Change" :
                //reset password textfield
                passwordText.setText("");
                break;

            case "Cancel" :
                //reset password textfield
                passwordText.setText("");
                break;
        }
    } // end method actionPerformed
}
