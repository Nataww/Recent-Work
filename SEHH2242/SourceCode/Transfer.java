// Withdrawal.java
// Represents a withdrawal ATM transaction

public class Transfer extends Transaction
{
    private double amount; // transfer amount
    private Keypad keypad; // reference to keypad
    private int transferAccount; //the account to be transferred

    // constant corresponding to menu option to cancel
    private final static int CANCELED = 3;

    // Withdrawal constructor
    public Transfer( int userAccountNumber, Screen atmScreen, 
    BankDatabase atmBankDatabase, Keypad atmKeypad)
    {
        // initialize superclass variables
        super( userAccountNumber, atmScreen, atmBankDatabase );

        // initialize references to keypad and cash dispenser
        keypad = atmKeypad;
    } // end Withdrawal constructor

    // perform transaction
    public void execute()
    {
        boolean transferred = false; // cash was not dispensed yet
        double availableBalance; // amount available for withdrawal

        // get references to bank database and screen
        BankDatabase bankDatabase = getBankDatabase(); 
        Screen screen = getScreen();

        // loop until cash is dispensed or the user cancels
        do
        {
            if(displayMenu() == CANCELED) {

                screen.displayMessageLine( "\nCanceling transaction..." );
                return; // return to main menu because user canceled
            }
            if(getAccountNumber() == transferAccount) {
                screen.displayMessageLine( "\nTransfers to your own account are not allowed." );
                return; // return to main menu because can't transfer money to myself
            }

            if(bankDatabase.checkAccountExist(transferAccount)) {

                // get available balance of account involved
                availableBalance = 
                bankDatabase.getAvailableBalance( getAccountNumber() );

                // check whether the user has enough money in the account 
                if ( amount <= availableBalance && amount > 0)
                {   
                    // update the account involved to reflect withdrawal
                    bankDatabase.debit( getAccountNumber(), amount );
                    bankDatabase.transferAdd( transferAccount, amount );

                    transferred = true; // Successfully transferred.

                    // instruct user to take cash
                    screen.displayMessageLine( 
                        "\nSuccessfully transferred." );
                } // end if
                else // not enough money available in user's account
                {
                    screen.displayMessageLine( 
                        "\nInsufficient funds in your account." +
                        "\n\nPlease enter a smaller amount or positive amount." );
                } // end else
            } else {
                //transfer account not exist
                screen.displayMessageLine( 
                    "\nTransfer account does not exist. Please try again." );
            }

        } while ( !transferred );

    } // end method execute

    // display a menu of withdrawal amounts and the option to cancel;
    // return the chosen amount or 0 if the user chooses to cancel
    private int displayMenu()
    {
        int userChoice = 0; // local variable to store return value

        Screen screen = getScreen(); // get screen reference

        // loop while no valid choice has been made
        while ( userChoice == 0 )
        {
            // display the menu
            screen.displayMessageLine( "\nTransfer Menu:" );
            screen.displayMessage( "\nPlease enter the account number you want to transfer to: " );

            int accountNumber = keypad.getInput(); // get user input through keypad

            screen.displayMessage( "\nPlease enter the amount you want to transfer: " );

            double inputAmount = keypad.getDoubleInput(); // get user input through keypad

            screen.displayMessageLine("Please confirm the account number and amount you entered.\n");
            screen.displayMessageLine("Account Number: " + Integer.toString(accountNumber));
            screen.displayMessageLine("Amount transferred: " + Double.toString(inputAmount));

            // display the menu
            screen.displayMessageLine( "\nTransfer Confirmation:" );
            screen.displayMessageLine( "1 - Confirm" );
            screen.displayMessageLine( "2 - Re-enter" );
            screen.displayMessageLine( "3 - Cancel transaction" );
            screen.displayMessage( "\nChoose an action: " );

            userChoice = keypad.getInput(); // get user input through keypad
            switch(userChoice) {
                case 1:
                    //Confirm
                    transferAccount = accountNumber;        
                    amount = inputAmount;
                    break;
                case 2:
                    userChoice = 0;
                    break;
                case CANCELED:
                    userChoice = CANCELED;
                    break;
                default: // the user did not enter a value from 1-6
                    screen.displayMessageLine( 
                        "\nIvalid selection. Try again." );
            }
        } // end while

        return userChoice; // return withdrawal amount or CANCELED
    } // end method displayMenuOfAmounts
} // end class Withdrawal

/**************************************************************************
 * (C) Copyright 1992-2007 by Deitel & Associates, Inc. and               *
 * Pearson Education, Inc. All Rights Reserved.                           *
 *                                                                        *
 * DISCLAIMER: The authors and publisher of this book have used their     *
 * best efforts in preparing the book. These efforts include the          *
 * development, research, and testing of the theories and programs        *
 * to determine their effectiveness. The authors and publisher make       *
 * no warranty of any kind, expressed or implied, with regard to these    *
 * programs or to the documentation contained in these books. The authors *
 * and publisher shall not be liable in any event for incidental or       *
 * consequential damages in connection with, or arising out of, the       *
 * furnishing, performance, or use of these programs.                     *
 *************************************************************************/