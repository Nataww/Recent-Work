#include <iostream>
#include <string>
#include <cctype>
#include <algorithm>
#include <time.h>

using namespace std;

int numberOfPiece = 15;			// sets the default number of puzzle pieces in game
int range = 5;
int maximum = 5;
int minimum = 0;
// sets the default range of edge number of each puzzle pieces
class Piece {

public:
	char* direction;			// prepare functions for rotation
	int slot;
	bool IsNull = true;

	void rotateClockwise() {
		char temp = direction[4];
		direction[4] = direction[3];
		direction[3] = direction[2];
		direction[2] = direction[1];
		direction[1] = temp;
	}
	void rotateAntiClockwise() {
		char temp = direction[1];
		direction[1] = direction[2];
		direction[2] = direction[3];
		direction[3] = direction[4];
		direction[4] = temp;
	}

	Piece(char* c, int i) {
		direction = c;
		slot = i;
	}

	Piece() {
	}

	void SetIsEmptyFalse(bool emp)
	{
		IsNull = emp;
	}
};

class GameBoard {				// printing board border and 

private:
	char board[20][18] = {};	//for printing puzzlebox
	char puzzleBox[18][18] = {};//where pieces is store, also the answer
	int boardCoordinate[25][2] = { { 5, 3 },{ 8, 3 },{ 11, 3 },{ 14, 3 },{ 17, 3 },
								{ 5, 6 },{ 8, 6 },{ 11, 6 },{14, 6 },{17, 6},
								{5,9},{8,9},{11,9},{14,9},{17,9},
								{5,12},{8,12},{11,12},{14,12},{17,12},
								{5,15},{8,15},{11,15},{14,15},{17,15} };

	Piece piecesInBox[25];
	Piece piecesPlaced[25];
	Piece savedAnswer[25];
	Piece emptyNullPiece;
	Piece empty;

	int move = 0; // counts the number of moves

	char RandomNumChar()		// generate random edge number of 
	{
		int random = rand() % (maximum + 1 - minimum) + minimum;
		return (char)(random + 48);
	}

	void PreparePieces(int num) {
		string indexString = "ABCDEFGHIJKLMNOPRSTUVWXYZ";

		for (int i = 0; i < num; i++) {
			char center, top, right, bottom, left;

			int random = rand() % indexString.length();
			center = indexString[random];
			indexString = indexString.erase(random, 1);

			if (i < 5) {
				top = RandomNumChar();
			}
			else {
				top = piecesInBox[i - 5].direction[3];
			}

			right = RandomNumChar();
			bottom = RandomNumChar();

			if (i == 0 || i % 5 == 0) {
				left = RandomNumChar();
			}
			else {
				left = piecesInBox[i - 1].direction[2];
			}

			piecesInBox[i] = Piece(new char[5]{ center,top,right,bottom,left }, i);
			piecesInBox[i].IsNull = false;
			savedAnswer[i] = Piece(new char[5]{ center,top,right,bottom,left }, i);
		}

		//------------------------------do random swap here---------------------------
		Piece temp;
		for (int i = 0; i < numberOfPiece; i++) {						//randomize the pieces on hand by position

			int firstrand = rand() % 25;
			int secondrand = rand() % 25;
			int rotate = rand() % 4;
			temp = piecesInBox[firstrand];								//sorting them into different slots
			piecesInBox[firstrand] = piecesInBox[secondrand];
			piecesInBox[secondrand] = temp;
			piecesInBox[firstrand].slot = firstrand;
			piecesInBox[secondrand].slot = secondrand;
			if (!(&piecesInBox[firstrand].direction[0] == nullptr)) {	//randomize the pieces on hand by position
				switch (rotate) {
				case 1:piecesInBox[firstrand].rotateClockwise(); break;
				case 2:piecesInBox[firstrand].rotateClockwise(); piecesInBox[firstrand].rotateClockwise(); break;
				case 3:piecesInBox[firstrand].rotateClockwise(); piecesInBox[firstrand].rotateClockwise(); piecesInBox[firstrand].rotateClockwise(); break;
				}
			}

		}
	}

	void PrepareCoordinate() {
		// code move to initiate in above
	}

	void PrepareEmptyBoard()// prepares an emptyboard
	{
		emptyNullPiece.IsNull = true;
		for (auto& x : board) {
			for (auto& y : x) {
				y = ' ';
			}
		}
		for (auto& x : puzzleBox) {
			for (auto& y : x) {
				y = ' ';
			}
		}
		string s;			// elements of the board used in for loop
		s = "     A  B  C  D  E    ";
		for (int i = 0; i < 20; i++) {
			board[i][0] = s[i];
		}
		s = "   +---------------+";
		for (int i = 0; i < 20; i++)
		{
			board[i][1] = s[i];
			board[i][17] = s[i];
		}
		s = " +|||||||||||||||+";
		for (int i = 0; i < 18; i++)
		{
			board[3][i] = s[i];
			board[19][i] = s[i];
		}
		s = "   1  2  3  4  5  ";
		for (int i = 0; i < 18; i++)
		{
			board[1][i] = s[i];
		}

		s = "  Pieces on Hand  "; // prepare the inventory box of puzzle on hand
		for (int i = 0; i < 18; i++)
		{
			puzzleBox[i][0] = s[i];
		}
		s = " +---------------+";
		for (int i = 0; i < 18; i++)
		{
			puzzleBox[i][1] = s[i];
			puzzleBox[i][17] = s[i];
		}
		s = " +|||||||||||||||+";
		for (int i = 0; i < 18; i++)
		{
			puzzleBox[1][i] = s[i];
			puzzleBox[17][i] = s[i];
		}
	}

	void AddPiecesToDisplay() {		//adds the pieces to board and inventory box for printing, according to the coordinates prepared at the start
		for (int i = 0; i < 25; i++) {
			if (piecesInBox[i].direction) {
				puzzleBox[boardCoordinate[i][0] - 2][boardCoordinate[i][1]] = piecesInBox[i].direction[0];
				puzzleBox[boardCoordinate[i][0] - 2][boardCoordinate[i][1] - 1] = piecesInBox[i].direction[1];
				puzzleBox[boardCoordinate[i][0] - 1][boardCoordinate[i][1]] = piecesInBox[i].direction[2];
				puzzleBox[boardCoordinate[i][0] - 2][boardCoordinate[i][1] + 1] = piecesInBox[i].direction[3];
				puzzleBox[boardCoordinate[i][0] - 3][boardCoordinate[i][1]] = piecesInBox[i].direction[4];
			}
		}

		for (int i = 0; i < 25; i++)
		{
			if (piecesPlaced[i].direction)
			{
				board[boardCoordinate[i][0]][boardCoordinate[i][1]] = piecesPlaced[i].direction[0];
				board[boardCoordinate[i][0]][boardCoordinate[i][1] - 1] = piecesPlaced[i].direction[1];
				board[boardCoordinate[i][0] + 1][boardCoordinate[i][1]] = piecesPlaced[i].direction[2];
				board[boardCoordinate[i][0]][boardCoordinate[i][1] + 1] = piecesPlaced[i].direction[3];
				board[boardCoordinate[i][0] - 1][boardCoordinate[i][1]] = piecesPlaced[i].direction[4];
			}
		}
	}

	bool CheckValidBeforePlace(int slot) {	// check valid placement of the pieces
		int above, below, left, right;		//approach is to check if it has pieces in above/below/left/right slots
											//their value must be same to be able to place		
		if (slot < 5)					//Check slot has above
		{
			above = -1;					//above don't have slot so we use -1 to represent here
		}
		else {
			above = slot - 5;
		}


		if (slot == 0 || slot % 5 == 0) //Check slot has left
		{
			left = -1;					//slot 0 is left
		}
		else {
			left = slot - 1;
		}


		if ((slot + 1) % 5 == 0)		//Check slot has right
		{
			right = -1;					//slot 2 is right
		}
		else
		{
			right = slot + 1;
		}


		if (slot >= 20)					//Check slot has below
		{
			below = -1;					//slot 6 is below
		}
		else
		{
			below = slot + 5;
		}

		bool valid = true;				//check if these slot has piece already
		if (above != -1) {
			if (!(&piecesPlaced[above].direction[0] == nullptr) &&
				piecesPlaced[above].direction[3] != selected.direction[1]) {
				valid = false;
			}
		}
		if (right != -1)
		{
			if (!(&piecesPlaced[right].direction[0] == nullptr) &&
				piecesPlaced[right].direction[4] != selected.direction[2])
			{
				valid = false;
			}
		}
		if (below != -1)
		{
			if (!(&piecesPlaced[below].direction[0] == nullptr) &&
				piecesPlaced[below].direction[1] != selected.direction[3])
			{
				valid = false;
			}
		}
		if (left != -1)
		{
			if (!(&piecesPlaced[left].direction[0] == nullptr) &&
				piecesPlaced[left].direction[2] != selected.direction[4])
			{
				valid = false;
			}
		}
		return valid;
	}

public:
	int numberOfPiece, range;
	Piece selected;

	GameBoard(int numberOfPiece, int range) {	// applies the configurated settings
		this->numberOfPiece = numberOfPiece;
		this->range = range;
		PreparePieces(numberOfPiece);
		PrepareCoordinate();
	}

	void PrintBoard() {
		PrepareEmptyBoard();
		AddPiecesToDisplay();

		system("cls");
		cout << "Move Count: " << move << "\n"; // uses the move int as counter
		cout << "\n";
		for (int i = 0; i < 18; i++)
		{
			for (int j = 0; j < 20; j++)
			{
				cout << (board[j][i]);
				if (board[j][i] == '\0') {
					cout << " ";
				}
			}
			for (int j = 0; j < 18; j++) {
				cout << (puzzleBox[j][i]);
				if (puzzleBox[j][i] == '\0') {
					cout << " ";
				}
			}
			cout << "\n";
		}
	}

	int SelectPiece(char c) { //selects a puzzle piece for further action, return it is inbox/ inPlaced / not exist
		for (int i = 0; i < 25; i++) {
			if (!(&piecesInBox[i].direction[0] == nullptr) && c == piecesInBox[i].direction[0]) {
				selected = piecesInBox[i];
				return 2;
			}
		}

		for (int i = 0; i < 25; i++) {
			if (!(&piecesPlaced[i].direction[0] == nullptr) && c == piecesPlaced[i].direction[0]) {
				selected = piecesPlaced[i];
				return 1;
			}
		}
		return 0;
	}

	void ShowAnswer() {		//shows answer after player decide to quit before returning to main menu
		copy(std::begin(savedAnswer), std::end(savedAnswer), std::begin(piecesPlaced));
		for (int i = 0; i < 25; i++) {
			emptyNullPiece.IsNull = true;
			piecesInBox[i] = emptyNullPiece;
		}

		PrepareEmptyBoard(); // similar to printboard
		AddPiecesToDisplay();
		system("cls");
		cout << "Move Count: " << move << "\n";
		cout << "\n";
		cout << "sample answer for reference" << "\n";
		for (int i = 0; i < 18; i++)
		{
			for (int j = 0; j < 20; j++)
			{
				cout << (board[j][i]);
				if (board[j][i] == '\0') {
					cout << " ";
				}
			}
			for (int j = 0; j < 18; j++) {
				cout << (puzzleBox[j][i]);
				if (puzzleBox[j][i] == '\0') {
					cout << " ";
				}
			}
			cout << "\n";
		}
	}

	bool ISslotEmpty(int slot) //scenario when piece is not in place
	{
		return piecesPlaced[slot].IsNull;
	}

	void PlaceToPlaced(string s)
	{
		int slot;
		slot = ((int)toupper(s[0]) - 65) + (stoi(string{ s[1] }) - 1) * 5;

		if (CheckValidBeforePlace(slot) && ISslotEmpty(slot))
		{
			piecesPlaced[slot] = piecesInBox[selected.slot];
			piecesInBox[selected.slot] = emptyNullPiece;
			piecesPlaced[slot].slot = slot;
			selected = emptyNullPiece;
			move++;
		}
		else {
			selected = emptyNullPiece;
			cout << "Invalid placement" << "\n";
			cin.ignore(); cin.get();
		}
	}

	void PutBackToBox() {  // function for putting puzzle pieces back to inventory
		for (int i = 0; i < 25; i++) {
			if ((&piecesInBox[i].direction[0] == nullptr)) {
				piecesInBox[i] = selected;
				piecesPlaced[selected.slot] = emptyNullPiece;
				piecesInBox[i].slot = i;
				selected = emptyNullPiece;
				break;
			}
		}
		move++;
	}

	bool CheckWin() { //checks if the player wins with 2 conditions

		bool noRemain = true; // 1. inventory box has zero piece
		int count = 0;
		for (int i = 0; i < 25; i++) {
			if (!(&piecesInBox[i].direction[0] == nullptr)) {
				count++;
			}
		}
		if (count > 0) {
			noRemain = false;
		}


		bool connected = true; // 2. pieces in placed(board) is at least connected to one other piece
		if (noRemain) {
			for (int i = 0; i < 25; i++)
			{
				if (!(&piecesPlaced[i].direction[0] == nullptr))
				{
					count = 0;
					int above, below, left, right;

					if (piecesPlaced[i].slot < 5)
					{
						above = -1;
					}
					else
					{
						above = piecesPlaced[i].slot - 5;
					}

					//Check p.slot has left
					if (piecesPlaced[i].slot == 0 || piecesPlaced[i].slot % 5 == 0)
					{
						left = -1;
					}
					else
					{
						left = piecesPlaced[i].slot - 1;
					}

					//Check p.slot has right
					if ((piecesPlaced[i].slot + 1) % 5 == 0)
					{
						right = -1;
					}
					else
					{
						right = piecesPlaced[i].slot + 1;
					}

					//Check p.slot has below
					if (piecesPlaced[i].slot >= 20)
					{
						below = -1;
					}
					else
					{
						below = piecesPlaced[i].slot + 5;
					}

					bool valid = true;
					if (above != -1)
					{
						if (!(&piecesPlaced[above].direction[0] == nullptr))
						{
							count++;
						}
					}
					if (right != -1)
					{
						if (!(&piecesPlaced[right].direction[0] == nullptr))
						{
							count++;
						}
					}
					if (below != -1)
					{
						if (!(&piecesPlaced[below].direction[0] == nullptr))
						{
							count++;
						}
					}
					if (left != -1)
					{
						if (!(&piecesPlaced[left].direction[0] == nullptr))
						{
							count++;
						}
					}

					if (count == 0)
					{
						connected = false;
					}
				}
			}
		}

		if (numberOfPiece == 1) {
			connected = true;
		}

		return noRemain && connected;

	}
};

void PrintMainMenu() { // stores the main menu text
	system("cls");
	cout << "Welcome to our Jigsaw Puzzle!! (-w-)\n";
	cout << "\n";
	cout << "*** Main Menu ***\n";
	cout << "[1] Start Game\n";
	cout << "[2] Settings\n";
	cout << "[3] Useful feature(s) added\n";
	cout << "[4] Credits\n";
	cout << "[5] Exit\n";
	cout << "*****************\n";
	cout << "Option (1 - 5): ";
}

void ShowFeature() { // stores the feature menu text
	system("cls");
	cout << "*** Useful Features ***" << endl;
	cout << "1. Steps Count" << endl;
	cout << "It counts steps player has done in top left of interface" << endl << endl;
	cout << "2. Shows Inventory" << endl;
	cout << "Puzzle pieces on hand is visible in the inventory box" << endl << endl;
	cout << "3. Scrambled Pieces" << endl;
	cout << "Puzzle pieces initially given are rotated and located differently for increasing difficulty" << endl << endl;
	cout << "press ENTER to continue... " << endl;
	cin.ignore(); cin.get();
}

void ShowPersonalDetails() { // stores the credit text
	system("cls");
	cout << "Groupmate Information  :)" << endl;
	cout << "Wu Wai Lam Friedman 21014195A 204C" << endl;
	cout << "Kwan Wai Kiu Ada 21023942A 204C" << endl;
	cout << "Ng Kwan Ho Gino 21090099A 204D" << endl;
	cout << "Lai Chun Ho Hugo 21024140A 204C" << endl;
	cout << "Wan Hoi Nam 21030030A 204C" << endl << endl;
	cout << "press ENTER to continue... " << endl;
	cin.ignore(); cin.get();
}

bool isNumber(const string& str)
{
	for (char const& c : str) {
		if (std::isdigit(c) == 0) return false;
	}
	return true;
}


bool CheckValidInput(string& s, int caseNum) { // verify input to be valid in menus
	switch (caseNum) {

		//main menu input
	case 0:
	{
		if (isNumber(s)) {
			int n = stoi(s);
			if (n >= 1 && n <= 5) {
				return true;
			}
		}
		cout << "Invalid Input, press ENTER to return and try again\n";
		cin.ignore(); cin.get();
		return false;
	}

	//setting input
	case 1:
	{
		if (isNumber(s)) {
			int n = stoi(s);
			if (n >= 1 && n <= 3) {
				return true;
			}
		}
		cout << "Invalid Input, press ENTER to return and try again\n";
		cin.ignore(); cin.get();
		return false;
	}

	//numberOfPiecce input
	case 2:
	{
		if (isNumber(s)) {
			int n = stoi(s);
			if (n >= 1 && n <= 25) {
				return true;
			}
		}
		cout << "Invalid Input, press ENTER to return and try again\n";
		cin.ignore(); cin.get();
		return false;
	}
	//range input
	case 3:
	{
		if (isNumber(s)) {
			int n = stoi(s);
			if (n >= 0 && n <= 9) {
				return true;
			}
		}
		cout << "Invalid Input, press ENTER to return and try again\n";
		cin.ignore(); cin.get();
		return false;
	}
	//index input
	case 4:
	{
		if (s.length() == 1) {
			if ((int)toupper(s[0]) >= 65 &&
				(int)toupper(s[0]) <= 90)
			{
				return true;
			}
		}
		cout << "Invalid Input, press ENTER to return and try again\n";
		cin.ignore(); cin.get();
		return false;
	}

	//action input
	case 5:
	{
		if (isNumber(s)) {
			int n = stoi(s);
			if (n >= 1 && n <= 3) {
				return true;
			}
		}
		cout << "Invalid Input, press ENTER to return and try again\n";
		cin.ignore(); cin.get();
		return false;
	}

	//xy coor input
	case 6:
	{
		if (s.length() == 2) {
			if ((int)toupper(s[0]) >= 65 &&
				(int)toupper(s[0]) <= 69)
			{
				int n = stoi(string{ s[1] });
				if (n >= 1 && n <= 5) {
					return true;
				}
			}
		}
		cout << "Invalid Input, press ENTER to return and try again\n";
		cin.ignore(); cin.get();
		return false;
	}

	//quit input
	case 7:
	{
		if (s.length() == 1) {
			if (toupper(s[0]) == 'N' ||
				toupper(s[0]) == 'Y')
			{
				return true;
			}
		}
		cout << "Invalid Input, press ENTER to return and try again\n";
		cin.ignore(); cin.get();
		return false;
	}

	default:
		return true;
	}
}

void Setting()  // stores settings text
{
	bool quitSetting = false;
	while (!quitSetting)
	{
		system("cls");
		cout << "*** Settings Menu ***\n";
		cout << "[1] Number of puzzle pieces\n";
		cout << "[2] Range of random numbers\n";
		cout << "[3] Return to Main Menu\n";
		cout << "*****************\n";
		cout << "Option (1 - 3):";
		string input;
		cin >> input;

		if (CheckValidInput(input, 1))
		{
			int inputNum = stoi(input);
			switch (inputNum) {
			case 1:
			{
				cout << "Current number of pieces in game: " << numberOfPiece << "\n";
				bool validInput = true;
				do {
					cout << "type new value for number of pieces to update: ";
					cin >> input;
					if (CheckValidInput(input, 2)) {
						cout << "New value: " << input << "\n";
						numberOfPiece = stoi(input);
						validInput = true;
					}
					else {
						cout << "Invalid Input, Try again\n";
						validInput = false;
					}system("pause");
				} while (!validInput);
				break;
			}

			case 2:
			{
				cout << "Current range in game: " << minimum << " - " << maximum << "\n";
				bool validInput = true;
				do {
					cout << "type new value for range to update: (e.g. 0 9)";
					string input2;
					cin >> input2;
					cin >> input;
					if (CheckValidInput(input, 3) && CheckValidInput(input2, 3) && input2 < input) {
						cout << "New range: " << input2 << " - " << input << "\n";
						range = stoi(input);
						maximum = stoi(input);
						minimum = stoi(input2);
						validInput = true;
					}
					else {
						validInput = false;
					}system("pause");
				} while (!validInput);
				break;
			}

			case 3:
			{
				quitSetting = true; system("pause");
				break;
			}
			default: {
				system("pause");
				break;
			}

			}
		}
	}
}

void NewGame() { // function for the main game
	bool quitGame = false;
	GameBoard* gameBoard = new GameBoard(numberOfPiece, range);
	while (!quitGame) {
		gameBoard->PrintBoard();
		cout << "input alphabet of the puzzle piece: ";
		string input;
		cin >> input;

		if (CheckValidInput(input, 4)) {

			if (toupper(input[0]) == 'Q') {
				cout << "you sure you want to rage quit?" << "\n";
				do
				{
					cout << "y\\n: ";
					cin >> input;
					if (toupper(input[0]) == 'Y') {
						quitGame = true;
						gameBoard->ShowAnswer();
						cout << "You lose!!\n";
						cout << "press ENTER to return main menu...";
						cin.ignore(); cin.get();
					}
				} while (!CheckValidInput(input, 7));
			}
			else
			{
				switch (gameBoard->SelectPiece(toupper(input[0]))) {
					//inbox
				case 2:
				{
					bool next = false;
					while (!next) {
						gameBoard->PrintBoard();
						cout << "Currently selected:  " << gameBoard->selected.direction[0] << "\n";	//Prompt out instructions for player
						cout << "***Action***" << "\n";
						cout << "[1] Rotate clockwise" << "\n";
						cout << "[2] Rotate anti-clockwise" << "\n";
						cout << "[3] Proceed" << "\n";
						cout << "*****************\n";
						cout << "Option (1 - 3): \n";
						cin >> input;
						if (CheckValidInput(input, 5)) {
							int inputNum = stoi(input);
							switch (inputNum) {
							case 1: {
								gameBoard->selected.rotateClockwise();
								break;
							}
							case 2: {
								gameBoard->selected.rotateAntiClockwise();
								break;
							}
							case 3: {
								next = true;
								break;
							}
							default:
								break;
							}
						}
					}
					gameBoard->PrintBoard();
					bool canPlace = false;
					while (!canPlace) {
						cout << "Please input the corrdinate (e.g.a1) : ";
						cin >> input;
						if (CheckValidInput(input, 6)) {
							gameBoard->PlaceToPlaced(input);
							canPlace = true;
						}
					}
					break;
				}
				//in placed
				case 1:
				{
					gameBoard->PutBackToBox();
					break;
				}
				//not exist
				case 0: {
					cout << "Piece does not exist\n";
					cout << "press ENTER to continue... " << endl;
					cin.ignore(); cin.get();
					break;
				}
				default: {
					break;
				}
				}
			}

			if (!quitGame && gameBoard->CheckWin()) {
				quitGame = true;
				gameBoard->PrintBoard();
				cout << "You WIN!!!\n";
				cout << "here's a cookie" << endl;
				cout << "*gives cookie " << endl << endl;
				cout << "press ENTER to continue... " << endl;
				cin.ignore(); cin.get();
			}
		}

	}
}

int main() // function for the exit mechanism
{
	bool mainMenuExit = false;
	srand(time(NULL));

	while (!mainMenuExit) {
		PrintMainMenu();
		string input;
		cin >> input;
		if (CheckValidInput(input, 0)) {
			int inputNum = stoi(input);
			switch (inputNum) {
			case 1:
				NewGame(); break;
			case 2:
				Setting(); break;
			case 3:
				ShowFeature(); break;
			case 4:
				ShowPersonalDetails(); break; // it has been 3:56...  (._.")
			case 5:
				cout << "Do you want to quit? " << "\n";
				cout << "(y/n): ";
				cin >> input;
				if (toupper(input[0]) == 'Y') {
					mainMenuExit = true;
				}
				else if (toupper(input[0]) == 'N') {
					//nothing
				}
				else {
					cout << "Invalid Input, Try again\n";
					cin.ignore(); cin.get();
				}
				break;
			}
		}
	}

	return 0;
}