import javax.swing.JTextField;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import javax.swing.JPanel;
import java.awt.event.ActionEvent;


public class accountLoginScreen extends MainScreen implements ActionListener{
    private static JTextField userText;
    

    public accountLoginScreen(String getFileName) {
        super(getFileName);
    } //end method accountLoginScreen

    @Override
    public void screenCenter(JButton[] centerButton, JPanel panel){
        userText = getTextField("",false,(screenWidth-309)/2, 300, 605/2, 32) ;
        panel.add (userText);
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
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "00" : 
                //Input text to TextFeild
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "." :
                //Input text to TextFeild
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "7" :
                //Input text to TextFeild
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "8" :
                //Input text to TextFeild
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "9" :
                //Input text to TextFeild
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "6" :
                //Input text to TextFeild
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "5" :
                //Input text to TextFeild
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "4" :
                //Input text to TextFeild
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "3" :
                //Input text to TextFeild
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "2" :
                //Input text to TextFeild
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "1" :
                //Input text to TextFeild
                userText.setText(userText.getText().concat( event.getActionCommand() ));
                break;

            case "Enter":
                //call next page
                try {  
                    setAccount(Integer.parseInt(userText.getText()));
                    waitingEnter = false;
                    dispose();

                } catch(NumberFormatException e){  

                } 
                break;

            case "Change" :
                //reset account textfield
                userText.setText("");
                break;

            case "Cancel" :
                //reset account textfield
                userText.setText("");
                break;
        }
    } // end method actionPerformed
}
