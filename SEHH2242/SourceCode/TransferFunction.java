
/**
 * Write a description of class runLogin here.
 *
 * @author (your name)
 * @version (a version number or a date)
 */
public class TransferFunction extends MainScreen
{   private Confirmation confirmation;
    private String userID="";
    private String amount="" ;
    public TransferFunction() {
        //Start Transfer
        //get Transfer User ID
        TransferMoneyUserID transferMoneyUserID = new TransferMoneyUserID("TransferMoneyUserID.png");
        transferMoneyUserID.setVisible(true);
        transferMoneyUserID.waiting();
        
        //get Transfer User Amount
        TransferMoneyAmount transferMoneyAmount = new TransferMoneyAmount("TransferMoneyAmount.png");
        transferMoneyAmount.setVisible(true);
        transferMoneyAmount.waiting();
        try{
            userID = transferMoneyUserID.getTransferMoneyUserID();
            amount = transferMoneyAmount.getTransferMoneyAmount();
        }
        catch(Exception ex){
        }
        transferMoneyUserID = null;
        transferMoneyAmount = null;
        //Show Confirm Page
        try{
            Confirmation confirmation = new Confirmation("Confirmation.png",Integer.parseInt(userID),Double.parseDouble(amount));
            confirmation.setVisible(true);
        }
        catch(Exception ex){
            ShowMessageScreen showErrorMessage = new ShowMessageScreen("AccountOrBalanceError.png",false,3); //show error message if account or amount is error
            showErrorMessage.setVisible(true);
            showErrorMessage.waiting();
        }

    } //end method TransferFunction
}
