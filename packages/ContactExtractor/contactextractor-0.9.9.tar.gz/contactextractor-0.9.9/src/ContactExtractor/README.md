Contact Extractor (ContExt), ver. 1.0 (May 2025).


Installation:

  pip instal ContExt

Usage:

  ContExt input=pathto/coordfile [OPTIONS]

As a Python function: 

  see https://github.com/febos/ContExt/blob/main/demo.ipynb

Description:

ContExt outputs pairs of atoms that lie closer to each other
than a specified threshold in angstroms ("range" parameter). 
By default, ContExt searches for atom-atom pairs at a distance 
< 10 angstroms in a structure file specified in the "input" 
parameter. If another structure file is specified under the 
"input2" parameter, ContExt will output only the close atom 
pairs found between the two structures. Subsets of atoms 
of interest can be defined with "atoms" and "atoms2" parameters. 

Requirements:
  
  SciPy
  
Output:

  The found atom-atom pairs are printed into stdout in 
  the following format:
   
  RANGE	ATOM1-DESCRIPTION	ATOM2-DESCRIPTION
  
  The atom descriptions are in the following format:
  
  #MODEL/CHAIN:RESIDUE_RESIDUENUMBER.INSERTIONCODE@ATOM_ATOMNUMBER.ALTLOC
  
  Example output:
  
  5.40291412 #1/A:A_12.@C1'_120. #1/A:G_13.@P_134.
  
  6.24810643 #1/B:C_12.A@C1'_583. #2/B:G_130.@O4'_14401.B

Options:

  input=	- input structure in pdb/mmcif format [REQUIRED]
 
	Path to a coordinate file in PDB or mmCIF format.
	
	input=example.pdb - search atom pairs in example.pdb 

  input2=	- input structure in pdb/mmcif format [DEFAULT: input2=input]
 
	Path to the second coordinate file in PDB or mmCIF format.
	
	input=example.pdb input2=example2.pdb - search 
	atom pairs between example.pdb and example2.pdb 
	
  -help	- type -help / --help / -h / -H to see this message [DEFAULT: FALSE]
  
	See the help message, ignore all other options.
	
  range=	- threshold in angstroms [DEFAULT: range=10.0]
 
	Atom distance threshold in angstroms.
  
  atoms=	- input atoms of interest [DEFAULT: atoms=#]
 
	Specify particular subset of atoms to be used as ATOM1.
	See the format description below.
	
  atoms2=	- input 2 atoms of interest [DEFAULT: atoms2=atoms]
 
	Specify particular subset of atoms to be used as ATOM2.
	See the format description below.
	
  ATOMS SPECIFICATION FORMAT:
  
  [#[INT][_INT]][/[STRING]][:[STRING][_INT[_INT]]][@[STRING][_INT[_INT]]]
  
  ATOMS SPECIFICATION EXAMPLES:
  
  atoms=#1/B:C_-1_10@O2 - O2 atoms of the residues with id 
                          from -1 to 10 of chain B from 
                          model 1
                           
  atoms=#               - equivalent to an empty condition
  
  atoms=/               - equivalent to an empty condition
  
  atoms=:               - equivalent to an empty condition
  
  atoms=@               - equivalent to an empty condition
  
  atoms="@C1' @C2'"     - C1’ and C2' atoms
  
  atoms="/B /C"         - chain B and chain C
  
  atoms=#1:A            - adenines in model 1
  
  atoms=A               - not a keyword, i.e. error
  
  atoms=":C@O4'"        - O4' atoms of cytidines
  
  atoms=#2_3@_1_1000    - atoms with id from 1 to 1000 
                          from model 2 or model 3

Usage examples:

  ContExt input=examples/1ffk_0_kt7.cif range=2.0 atoms="@O3'" atoms2=@P
	
	Find O3'-P pairs at a distance under 2.0 angstroms in the
	examples/1ffk_0_kt7.cif coordinate file. The output
	includes pairs of consecutive nucleotides.

  ContExt input=examples/1ffk_0_kt7.cif input2=examples/3d2g_A_kj.cif range=5 atoms=@P
  
	Find P-P pairs at a distance under 5.0 angstroms
	betweeen the two input coordinate files.

  ContExt input=examples/2fmt.pdb atoms=:A atoms2=:ARG
  
  	Find atom-atom pairs within 10 angstroms (default range)
  	between adenines and arginines in the input file.

