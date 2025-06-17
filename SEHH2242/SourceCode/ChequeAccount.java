
// ChequeAccount.java
// Represents a bank cheque account
public class ChequeAccount extends Account
{
    // instance variables
    private double eachChequeLimit;

    // Cheque Account constructor initializes attributes
    public ChequeAccount(int theAccountNumber, int thePIN, 
    double theAvailableBalance, double theTotalBalance)
    {
        super( theAccountNumber, thePIN, theAvailableBalance,  theTotalBalance);
        // initialise instance variables
        setEachChequeLimit(10000.0);
    } // end ChequeAccount constructor

    //set Each Cheque Limit
    public void setEachChequeLimit(double limitValue)
    {
        eachChequeLimit = limitValue;
    } //end method setEachChequeLimit

    //return double Each Cheque Limit
    public double getEachChequeLimit()
    {
        return eachChequeLimit;
    } //end method getEachChequeLimit

    @Override
    public String toString()
    {
        return String.format("%s\nAvailableBalance: %s\nTotal Balance: %s\nEach Cheque Limit:%s\n",
            "Account type: Cheque Account",
            getAvailableBalance(),
            getTotalBalance(),
            getEachChequeLimit());
    }
} //end public class ChequeAccount
