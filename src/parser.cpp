#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

struct Data{
	unsigned servers;
	unsigned machines;
	unsigned jobs;
} problem;

using namespace std;

void input(istream& infile) {
	string line;
	string word;
	int servers;
	int jv_pairs;
	int s_cpu;
	int s_ram;
	int s_id;
	
	//num of servers
	getline(infile, line);
	ifstream iss(line)
	if (iss >> servers)
		cout << servers << endl;
	
	for(int tmp = 0; tmp < servers; tmp++){
		getline(infile, line);
		ifstream iss(line);
		//create server object
		if(iss >> s_id >> s_cpu >> s_ram)
				cout << s_id << "/" << s_ram << "/" << s_cpu << endl;
	}
	
	//num of (jobs, machines)
	getline(infile, line);
	if(iss >> jv_pairs)
		cout << "Number of Pairs: " << jv_pairs << endl;
	
	for(int tmp = 0; tmp < jv_pairs; tmp++){
		getline(infile, line);
		//create jv_pair
	}
}

int main(int argc, char* argv[]) {
	const char* filename = argv[1];
	iftream infile(filename);
	input(infile);
	return 0;
}

