#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <TFile.h>
#include <TChain.h>
#include <TStopwatch.h>
#include<fstream>
#include <iostream>


using namespace std;

std::vector<std::string> split(const std::string &s, char delim) {
  std::vector<std::string> elems;
  std::stringstream ss(s);
  std::string item;
  while(std::getline(ss, item, delim)) {
    elems.push_back(item);
  }
  return elems;
}

TDirectory* make_dir_ifneeded(TDirectory* dir, string name){
  //cout << "called make_dir_ifneeded on: ( " << dir->GetName() << ", " << name <<")" << endl; 
  TDirectory* ret = dynamic_cast<TDirectory*>( dir->Get(name.c_str()) );

  if( ret ){
    //cout << "directory already exists, returning it" << endl; 
    return ret;
  }
  else{
    //cout << "directory does not exists, creating and returning it" << endl; 
    return dir->mkdir(name.c_str());
  }
}

TDirectory* make_dirs_and_enter(TFile *f, std::vector<std::string> dir_tree){
  TDirectory* dir = f;
  for( unsigned int i=0; i < (dir_tree.size() -1) /*the last is the name of the object!*/; i++){
    // cout << "calling make_dir_ifneeded, "<< dir_tree[i] << endl;     
    // cout << "dir: "<< dir->GetName() << endl;
    dir = make_dir_ifneeded(dir, dir_tree[i]);
  }
  // cout << "cd into dir" << endl;     
  dir->cd();
  return dir;
}

std::vector<std::string> read_file(const std::string &path) { 
  ifstream myfile;
  myfile.open(path.c_str());
  string line;
  std::vector<std::string> ret;
  if (myfile.is_open()) {
    while (myfile.good()) {
      getline(myfile,line);
      ret.push_back(line);
    }
  }
  myfile.close();
  return ret;
}

inline bool fexists(string path)
{
  ifstream ifile(path.c_str());
  bool ret = (bool) ifile;
  ifile.close();
  return ret;
}

double getTimeWithoutStopping( TStopwatch* watch )
{
  double ret = watch->RealTime();
  watch->Start(true);
  //watch.Continue();
  return ret;
}


int main(int argc, char* argv[]) {

  // only allow one argument for this which should be the python cfg file
  if ( argc < 4 ) {
    std::cout << __LINE__ << " Usage : " << argv[0] << " [directory with lists] [output_file_name] [input_files]+" << std::endl;
    return 42;
  }
  cout << "argv read by .cc "; 
  for (unsigned int i = 0; i< sizeof(argv); i++){
    cout << argv[i] << " " ;
  }
  cout << endl;
  TStopwatch *global_watch = new TStopwatch();
  TStopwatch *watch = new TStopwatch();
  string lists_dir = argv[1];
  string outf_name = argv[2];
  string input_file_list = argv[3];
  vector<string> inputs = split(input_file_list,',');

  if( !fexists( (lists_dir+"/trees_location.list") ) ){
    cout << __LINE__ << " Cannot stat " << lists_dir << "/trees_location.list no such file" << endl;
    return 42;
  }

  vector<string> trees_locations = read_file( (lists_dir+"/trees_location.list") );
  // cout << getTimeWithoutStopping( watch ) << ": spent reading trees locations..." << endl;
  
  //Create output file
  TFile* file = TFile::Open(outf_name.c_str(), "RECREATE");
  for( vector<string>::const_iterator location = trees_locations.begin(); location != trees_locations.end(); ++location){
    cout << "Merging.. " << *location << endl;
    string loc_copy = *location;
 
    TChain *chain = new TChain(location->c_str());
    for(vector<string>::const_iterator input = inputs.begin(); input != inputs.end(); ++input) {
      if( !fexists( ("/hdfs"+*input).c_str())) {
	cout << __LINE__ << " Cannot stat /hdfs"<< (*input)<< " no such file" << endl;
	return 42;
      }
      chain->Add(("/hdfs"+*input).c_str());

//       cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << chain->GetEntries()<< endl;
    }

    //properly sets the branches
    if( fexists( (lists_dir+"/"+loc_copy+".list") ) ){
      vector<string> branches = read_file((lists_dir+"/"+loc_copy+".list"));
      chain->SetBranchStatus("*",0); //deactivate all branches
      for(vector<string>::const_iterator branch = branches.begin(); branch != branches.end(); ++branch) chain->SetBranchStatus(branch->c_str(),1); //activate this branch
    }
    else{
      chain->SetBranchStatus("*",1); //activate all branches
    }


    TDirectory* current_dir = make_dirs_and_enter(file, split(*location, '/') );
//     long int input_entries = input_tree->GetEntriesFast();

    chain->Merge(file,0, "fast keep"); // keep->prevents file from beeing closed
    
//     long int input_entries = chain->GetEntries();
//     TTree * outtree = (TTree*) file->Get(location->c_str());
    

//     If(outtree->GetEntries() != input_entries){
//       cout << "Something wrong happened during merging, input and output trees have different number of entries. Exiting..." << endl;
//       delete outtree;
//       file->Close();
//       return 42;
//     }
//     delete outtree;
    //file = TFile::Open(outf_name.c_str(), "UPDATE"); //Open it again because root is stupid and will close it when the TChain gets deleted. Looking for a better way though
  }

  cout << "Done!" << endl;
  file->Close();
  cout << "Total time used: " << global_watch->RealTime() << endl;
  delete global_watch;
  delete watch;
  return 0;}


//To replace in a string replace( s.begin(), s.end(), ' ', '~' );
