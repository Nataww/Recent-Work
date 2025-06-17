// ATM.java
// Represents an automated teller machine


public class ATM
{
    private boolean userAuthenticated; // whether user is authenticated
    private BankDatabase bankDatabase;
    private CashDispenser cashDispenser;
    private MainScreen getMainScreen;


    // no-argument ATM constructor initializes instance variables
    public ATM() 
    {
        userAuthenticated = false; // user is not authenticated to start
        getMainScreen = new MainScreen();
        bankDatabase = getMainScreen.getBankDatabase();
        cashDispenser = getMainScreen.getCashDispenser();

    } // end no-argument ATM constructor

    // start ATM 
    public void run()
    {
        // welcome and authenticate user; perform transactions
        while ( true )
        {
            // loop while user is not yet authenticated
           while ( !userAuthenticated ) 
            {
                //screen.displayMessageLine( "\nWelcome!" );
                ShowMessageScreen welcomeMessage = new ShowMessageScreen("welcomeATM.png",false,3,"empty");
                welcomeMessage.setVisible(true);
                welcomeMessage.waiting();
                authenticateUser(); // authenticate user
            } // end while

            performTransactions(); // user is now authenticated 
            userAuthenticated = false; // reset before next ATM session
            //currentAccountNumber = 0; // reset before next ATM session 
            //screen.displayMessageLine( "\nThank you! Goodbye!" );
        } // end while   
    } // end method run

    // attempts to authenticate user against database
    private void authenticateUser() 
    {
        //get user account
        accountLoginScreen loginAccount = new accountLoginScreen("UserID.png");
        loginAccount.setVisible(true);
        loginAccount.waiting();

        int accountNumber = loginAccount.getAccount();
        loginAccount = null;

        //get user password
        passwordLoginScreen loginPassword = new passwordLoginScreen("Password.png");
        loginPassword.setVisible(true);
        loginPassword.waiting();
        int pin = loginPassword.getPassword();
        loginPassword = null;

        // set userAuthenticated to boolean value returned by database
        userAuthenticated = 
        bankDatabase.authenticateUser( accountNumber, pin );

        // check whether authentication succeeded
        if ( userAuthenticated )
        {
            getMainScreen.setAccount(accountNumber); // save user's account #

        } // end if
        else {
            //wrong userid or password
            ShowMessageScreen showMessage = new ShowMessageScreen("WrongLogin.png",false, 3, "empty");
            showMessage.setVisible(true);
            showMessage.waiting();
        }
        
    } // end method authenticateUser

    // display the main menu and perform transactions
    private void performTransactions() 
    {
        boolean userExited = false; // user has not chosen to exit
        MainMenuScreen mainMenu = new MainMenuScreen("MainMenu.png");
        mainMenu.setVisible(true);
        while(!userExited) {
            try
            {
                Thread.sleep(1);
            }
            catch (InterruptedException ie)
            {
                ie.printStackTrace();
            }
            if(getMainScreen.getAccount() == 0) {
                userExited = true;
            }
        }

    } // end method performTransactions

} // end class ATM

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