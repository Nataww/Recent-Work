import javax.swing.JButton;
import java.awt.event.ActionListener;
import javax.swing.JPanel;
import java.awt.event.ActionEvent;


public class FixedAmountWithdrawalScreen extends MainScreen implements ActionListener{
    private static int withdrawlAmount;

    public FixedAmountWithdrawalScreen(String getFileName, int getAmount) {
        super(getFileName);
        withdrawlAmount = getAmount;
    } // end method FixedAmountWithdrawalScreen

    @Override
    public void screenCenter(JButton[] centerButton, JPanel panel){
    } // end method screenCenter

    public void execute()
    {
        double availableBalance; // amount available for withdrawal
        // get available balance of account involved
        availableBalance = 
        bankDatabase.getAvailableBalance( getAccount() );

        // check whether the user has enough money in the account 
        if ( withdrawlAmount <= availableBalance && withdrawlAmount > 0)
        {   
            // check whether the cash dispenser has enough money
            if ( cashDispenser.isSufficientCashAvailable( withdrawlAmount ) )
            {
                // update the account involved to reflect withdrawal
                bankDatabase.debit( getAccount(), withdrawlAmount );

                cashDispenser.dispenseCash( withdrawlAmount ); // dispense cash


                new ShowMessageScreen("takeCard.png",false,3, "withdrawlComplete1"); //Withdrawl completed step
                dispose();
            } // end if
            else {// cash dispenser does not have enough cash
                new ShowMessageScreen("ATMInsufficientCash.png",false,3); //Insufficient cash available in the ATM.
                dispose();
            }
            } // end if
            else // not enough money available in user's account
            {
                new ShowMessageScreen("AccountOrBalanceError.png",false,3); //Insufficient funds in your account.
                dispose();

            } // end else

        } // end method execute

        @Override
        public void actionPerformed( ActionEvent event )
        {

        switch (event.getActionCommand())
        {
            case "Enter":
                //call withdrawl function here
                execute();
                break;
            case "Change" :
                //go back withdrawl menu
                new WithdrawalMenuScreen("WithdrawalMenu.png");
                dispose();
                break;

            case "Cancel" :
                // cancel, go to main menu
                new MainMenuScreen("MainMenu.png");
                dispose();
                break;
        }
    } // end method actionPerformed
}
