
// ChequeAccount.java
// Represents a bank saving account
public class SavingAccount extends Account
{
    // instance variables
    private double interestRate;

    // Saving Account constructor initializes attributes
    public SavingAccount(int theAccountNumber, int thePIN, 
    double theAvailableBalance, double theTotalBalance)
    {
        super( theAccountNumber,  thePIN,theAvailableBalance, theTotalBalance); // pass to Account constructor
        setInterestRate(0.1);
        //setInterestRate;
    } // end SavingAccount constructor

    //return double Interest Rate
    public double getInterestRate()
    {
        return interestRate;
    } // end method getInterestRate

    //set Interest Rate
    public void setInterestRate( double interestInput )
    {
        interestRate= interestInput/100;//interest rate per annum
    } //end method setInterestRate

    @Override
    public String toString()
    {
        return String.format("%s\nAvailableBalance: %s\nTotal Balance: %s\nInterest Rate:%s%%\n",
            "Account type: Saving Account",
            getAvailableBalance(),
            getTotalBalance(),
            getInterestRate()*100);
    } // end method toString
} //end public class SavingAccount
