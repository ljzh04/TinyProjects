#include <bits/stdc++.h> // all headers
#include <windows.h> // console cursor stuff
#include <conio.h> // _getch()
//#include <iostream>
//#include <cctype> // isdigit
//#include <stdexcept> // invalid_argument()
//#include <queue>
//#include <stack>
#define ENTER '\r'
#define BACKSPACE '\b'
#define ADD '+'
#define SUB '-'
#define MUL '*'
#define DIV '/'
#define OP '('
#define CP ')'
using namespace std;

// constants
int X, Y; // keeps track of iniital cursor position

// calculator functions
int priority(const string& op);
bool isdigit(const string& str);
double solve_postfix(queue<string> expr);
double solve_str(string input);
vector<string> tokenize(const string& expr);
queue<string> infix_to_postfix(const string& infix_string);

// interface functions
void setCursorPosition(int x, int y);
void getCursorPosition(int &x, int &y);
void gotoxy(const int &x, const int &y);
void display_input(const int &X, const int &Y);
void display_output(const int &X, const int &Y, const string& input);
void ui_control();


// for debugging
template <typename T> // any data type
void print_queue(const queue<T>& q){
    queue<T> temp = q;
    while (!temp.empty()) {
        cout << temp.front()<<" ";
        temp.pop();
    }
    cout << '\n';
}

int main(){
	int curX, curY;
	getCursorPosition(curX, curY);
	X = curX;
	Y = curY;
	ui_control();
	return 0;	
}

// returns the priority of operators
int priority(const string& op){
	if(op == "("){
		return 0;
	}
	else if(op == "+" || op == "-"){
		return 1;
	}
	else if(op == "*" || op == "/"){
		return 2;
	}
	else if(op == "^"){
		return 3;
	}
	else {
		throw invalid_argument("Unimplemented operator.");
	}
}

// separate numbers and operators from expression 
// if digit, append single digit to number string (compile all digits)
// if operator, push number string to queue, then push operator to queue
// finally push remaining number to queue
vector<string> tokenize(const string& expr){
	vector<string> tokens;
	string number = "";

	for (char c : expr){
		if(isdigit(c) or c == '.'){
			number += c;
		}
		else{
			if(number != ""){
				tokens.push_back(number);
				number = "";
			}
			tokens.push_back(string(1,c));
		}
	}

	if(number != ""){
		tokens.push_back(number);
		number = "";
	}

	return tokens;
}
// overloading default function, to allow for checking strings instead of chr
bool isdigit(const string& str) {
    return !str.empty() && all_of(
    	str.begin(), 
    	str.end(), 
		[](char c) { return std::isdigit(c) || c == '.'; });
}
// shunting yard algorithm
// if operator, peek at stack
// --> if peeked operator is ')' pop all operators until '(' and add to queue (discard parenthesis)
// --> else if peeked operator is of higher precedence, enqueue that operator and add the peeked one to stack
// --> else push to stack
// else if number add to queue
// if end of input, pop stack
queue<string> infix_to_postfix(const string& infix_string){
	vector<string> tokens = tokenize(infix_string);
	stack<string> stack;
	queue<string> queue;

	for (string token : tokens){
		//cout << token << stack.empty() << endl; // debug
		if(isdigit(token)){
			queue.push(token);
		}
		else if(token == "("){
			stack.push(token);
		}
		else if(token == ")"){
			while(stack.empty() == false && stack.top() != "("){
				queue.push(stack.top());
				stack.pop();
			}
			stack.pop(); // pop the remaining '('
		}
		else{ // operators
			while(stack.empty() == false && priority(stack.top()) >= priority(token)){
				queue.push(stack.top());
				stack.pop();
			}
			stack.push(token);
		}
	}
	while(stack.empty() == false){
		queue.push(stack.top());
		stack.pop();
	}
	return queue;
}
// postfix solving algorithm
// if number, push into stack
// if operator, pop 2 in stack, evaluate those with operator, then push back
// if end, return the top of stack
double solve_postfix(queue<string> expr){
	stack<double> stack;
	while(expr.empty() == false){
		string token = expr.front();
		// cout << token << " " << stack.top() << endl; // for debugging
		if(isdigit(token)){
			stack.push(stod(token));
		}
		else{
			// taking out two operands |*important -> (b op a) not (a op b)|
			double a = stack.top();
			stack.pop();
			double b = stack.top();
			stack.pop();

			// operator handling
			if(token == "+"){ stack.push(b+a); }
			else if(token == "-"){ stack.push(b-a); }
			else if(token == "/"){ stack.push(b/a); }
			else if(token == "*"){ stack.push(b*a); }
			else if(token == "^"){ stack.push(pow(b,a)); }
		}
		expr.pop();
	}
	return stack.top();
}
double solve_str(string input){
	//string input = "3/3*(3-1)+2.5+343.23123";
	queue<string> postfix = infix_to_postfix(input);
	return solve_postfix(postfix);
}


void setCursorPosition(int x, int y) {
    COORD coord = { (SHORT)x, (SHORT)y };
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}
void getCursorPosition(int &x, int &y) {
    CONSOLE_SCREEN_BUFFER_INFO csbi;
    if (GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi)) {
        x = csbi.dwCursorPosition.X;
        y = csbi.dwCursorPosition.Y;
    } else {
        // Handle error (e.g., invalid handle)
        x = -1;
        y = -1;
    }
}
void gotoxy(const int &x, const int &y){
	setCursorPosition(X+x,Y+y);
}
void display_input(const int &X, const int &Y){
	int x, y;
	gotoxy(0, 1);
	cout << "-INPUT-------------" << endl;
	cout << endl;
	cout << "-------------------" << endl;
}
void display_output(const int &X, const int &Y, const string& input = "0"){
	int x, y;
	gotoxy(0, 3);
	cout << "-OUTPUT------------" << endl;
	
	cout << solve_str(input) << endl;
	
	cout << "-------------------" << endl;
}
void ui_control(){
	string input;
	int inputY = 2;
	int cursorX = 0;

	display_input(X, Y);
	display_output(X, Y);
	gotoxy(cursorX,inputY);

	while(true){
		if(_kbhit()){
			char ch = _getch();
			//gotoxy(0,0); // for debugging
			//cout << input; // for debugging

			display_output(X, Y);
			gotoxy(cursorX,inputY);

			if(ch == 27){ // esc
				return;
			}
			else if(ch == ENTER){ 
				display_output(X, Y, input);
				cursorX = 0;
				break;
			}
			else if(ch == BACKSPACE){
				if(!input.empty()){
					input.erase(cursorX, 1);
					cursorX--;
					gotoxy(cursorX,inputY);
					cout << " ";
					gotoxy(cursorX,inputY);
				}
			}
			else if(ch == 75){//left
				cursorX--;
				gotoxy(cursorX,inputY);
			}
			else if(ch == 77){//right
				cursorX++;
				gotoxy(cursorX,inputY);
			}
			else if(isdigit(ch) || ch == ADD || ch == MUL || ch == SUB || ch == DIV || ch == OP || ch == CP){
				int len = input.length();
				if(cursorX < len){
					string end = input.substr(cursorX,len-1);
					input.insert(cursorX, end);
				}
				else{
					input += ch;
				}
				cout << ch;
				cursorX++;
			}
		}
	}
}
