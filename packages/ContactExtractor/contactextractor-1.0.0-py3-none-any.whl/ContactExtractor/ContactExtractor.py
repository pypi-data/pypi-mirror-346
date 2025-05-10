
import sys
import os
import re
from scipy.spatial import KDTree

ATOMSPATTERN = re.compile(r"^(#(([0-9]+)(_([0-9]+))?)?)?"+\
                          r"(\/([\w]*))?"+\
                          r"(:([A-Za-z0-9]+)?((_(-?[0-9]+))(_(-?[0-9]+))?)?)?"+\
                          r"(@([A-Za-z0-9]+'?)?((_(-?[0-9]+))(_(-?[0-9]+))?)?)?$")

    
def ParseAtomsFormat(kw, pattern = ATOMSPATTERN):

    regsearch = re.findall(ATOMSPATTERN, kw)[0]
    
    modelmin   = regsearch[2]
    modelmax   = regsearch[4]
    chain      = regsearch[6]
    residue    = regsearch[8]
    resnummin  = regsearch[11]
    resnummax  = regsearch[13]
    atom       = regsearch[15]
    atomnummin = regsearch[18]
    atomnummax = regsearch[20]

    res =  {'MODELMIN':   int(modelmin)   if modelmin   else None,
            'MODELMAX':   int(modelmax)   if modelmax   else None,
            'CHAIN':      chain   if chain   else None,
            'RESIDUE':    residue if residue else None,
            'RESNUMMIN':  int(resnummin)  if resnummin  else None,
            'RESNUMMAX':  int(resnummax)  if resnummax  else None,
            'ATOM':       atom    if atom    else None,     
            'ATOMNUMMIN': int(atomnummin) if atomnummin else None,
            'ATOMNUMMAX': int(atomnummax) if atomnummax else None}

    if res['MODELMAX'] is None and not (res['MODELMIN'] is None):
        res['MODELMAX'] = res['MODELMIN']
    if res['RESNUMMAX'] is None and not (res['RESNUMMIN'] is None):
        res['RESNUMMAX'] = res['RESNUMMIN']
    if res['ATOMNUMMAX'] is None and not (res['ATOMNUMMIN'] is None):
        res['ATOMNUMMAX'] = res['ATOMNUMMIN']

    return res


def Allowed(atom, masks):

    for mask in masks:

        condition = (mask['ATOMNUMMIN'] is None or atom['id']                 >= mask['ATOMNUMMIN']) and\
                    (mask['ATOMNUMMAX'] is None or atom['id']                 <= mask['ATOMNUMMAX']) and\
                    (mask['ATOM']       is None or atom['auth_atom_id']       == mask['ATOM'])       and\
                    (mask['RESNUMMIN']  is None or atom['auth_seq_id']        >= mask['RESNUMMIN'])  and\
                    (mask['RESNUMMAX']  is None or atom['auth_seq_id']        <= mask['RESNUMMAX'])  and\
                    (mask['RESIDUE']    is None or atom['auth_comp_id']       == mask['RESIDUE'])    and\
                    (mask['CHAIN']      is None or atom['auth_asym_id']       == mask['CHAIN'])      and\
                    (mask['MODELMIN']   is None or atom['pdbx_PDB_model_num'] >= mask['MODELMIN'])   and\
                    (mask['MODELMAX']   is None or atom['pdbx_PDB_model_num'] <= mask['MODELMAX'])
        
        if condition:
            return True
    return False


def ParseAtomPDB(line, model):
    '''https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html'''
    
    atom = {}
    atom["id"]                 = int(line[6:11])
    atom["auth_atom_id"]       = line[12:16].strip()
    atom["label_alt_id"]       = line[16].strip()
    atom["auth_comp_id"]       = line[17:20].strip()
    atom["auth_asym_id"]       = line[20:22].strip()
    atom["auth_seq_id"]        = int(line[22:26])
    atom["pdbx_PDB_ins_code"]  = line[26].strip()
    atom["Cartn_x"]            = float(line[30:38])
    atom["Cartn_y"]            = float(line[38:46])
    atom["Cartn_z"]            = float(line[46:54])
    atom["pdbx_PDB_model_num"] = model

    if atom["pdbx_PDB_ins_code"] == '?':
        atom["pdbx_PDB_ins_code"] = ''

    return atom


def ParsePDB(inpfile, masks):

    atoms = []
    model = 1

    with open(inpfile) as file:
        for line in file:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                atom = ParseAtomPDB(line, model)
                if Allowed(atom, masks):
                    atoms.append(atom)
            elif line.startswith('MODEL'):
                model = int(line.strip().split()[-1])
    return atoms


def ParseAtomCIF(line,title):

    linesplit = line.strip().split()
    atom = {title[i]:linesplit[i] for i in range(len(title))}

    for frag in ("atom", "comp", "asym", "seq"):

        auth  =  "auth_{}_id".format(frag)
        label = "label_{}_id".format(frag)
        
        if auth not in atom and label in atom:
            atom[auth] = atom[label]

    for int_token in ("id", "auth_seq_id", "pdbx_PDB_model_num"):
        atom[int_token] = int(atom[int_token]) if int_token in atom else float("nan")

    for float_token in ("Cartn_x", "Cartn_y", "Cartn_z","occupancy","B_iso_or_equiv"):
        atom[float_token] = float(atom[float_token]) if float_token in atom else float("nan")
    
    if      "auth_atom_id" not in atom: atom["auth_atom_id"]      = ''
    if     "label_atom_id" not in atom: atom["label_atom_id"]     = ''
    if      "label_alt_id" not in atom: atom["label_alt_id"]      = ''
    if      "auth_comp_id" not in atom: atom["auth_comp_id"]      = ''
    if      "auth_asym_id" not in atom: atom["auth_asym_id"]      = ''
    if "pdbx_PDB_ins_code" not in atom: atom["pdbx_PDB_ins_code"] = ''

    if atom["pdbx_PDB_ins_code"] == '?':
        atom["pdbx_PDB_ins_code"] = ''

    atom["auth_atom_id"] = atom["auth_atom_id"].strip('"')
    atom["label_atom_id"] = atom["label_atom_id"].strip('"')

    return atom


def ParseCIF(inpfile, masks):

    atoms = []
    title = []

    with open(inpfile) as file:
        for line in file:
            if line.startswith("_atom_site."):
                title.append(line.strip().split('.')[-1])
            elif line.startswith('ATOM') or line.startswith('HETATM'):
                atom = ParseAtomCIF(line, title)
                if Allowed(atom, masks):
                    atoms.append(atom)
    return atoms


def GuessFormat(inpfile):

    pdb = 0
    cif = 0

    with open(inpfile) as file:
        for line in file:
            if line.startswith('#'):
                cif += 1
            elif line.startswith('_atom.site'):
                cif += 1
            elif line.startswith('END'):
                pdb += 1
            elif line.startswith('MODEL'):
                pdb += 1

    return int(cif > pdb)


def ParseAtoms(inpfile, masks):

    return (ParsePDB, ParseCIF)[GuessFormat(inpfile)](inpfile, masks)


def Atompairs(n1, n2, limit):

    tree1 = KDTree(n1)
    tree2 = KDTree(n2)

    dist = tree1.sparse_distance_matrix(tree2,
                                        limit,
                                        p=2,
                                        output_type='ndarray')
    dist.sort()
    return dist


def FormatAtom(atom):

    atomformat = "#{model}/{chain}:{residue}_{resnum}.{inscode}@{atomname}_{atomnum}.{altloc}"

    return atomformat.format(model    =atom["pdbx_PDB_model_num"],
                             chain    =atom["auth_asym_id"],
                             residue  =atom["auth_comp_id"],
                             resnum   =atom["auth_seq_id"],
                             inscode  =atom["pdbx_PDB_ins_code"],
                             atomname =atom["auth_atom_id"],
                             atomnum  =atom["id"],
                             altloc   =atom["label_alt_id"])


def PrintContacts(contacts, atoms1, atoms2,
                  printing = False, onesetflag = False):

    printed_flag = False

    ready_contacts = [] 

    for i,j,d in contacts:
        if onesetflag and i==j:
            continue
        printed_flag = True
        if printing:
            print(d, FormatAtom(atoms1[i]), FormatAtom(atoms2[j]),sep='\t')
        else:
            ready_contacts.append([d, FormatAtom(atoms1[i]), FormatAtom(atoms2[j])])

    if printing and not printed_flag:
        print("No contacts found")

    return ready_contacts


def ContExt(inpfile1, inpfile2 = None, RANGE = 10.0, mask1 = "#", mask2 = None,
                     printing = False):

    HOME_DIR = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(inpfile1) and\
       os.path.exists(os.path.join(HOME_DIR, inpfile1)):
        inpfile1 = os.path.join(HOME_DIR, inpfile1)

    elif not os.path.exists(inpfile1):
        raise ValueError("ERROR: something is wrong with your input file")

    if inpfile2 is None:
        inpfile2 = inpfile1

    if not os.path.exists(inpfile2) and\
       os.path.exists(os.path.join(HOME_DIR, inpfile2)):
        inpfile2 = os.path.join(HOME_DIR, inpfile2)

    elif not os.path.exists(inpfile2):
        raise ValueError("ERROR: something is wrong with your input2 file")

    try:
        RANGE = float(RANGE)
    except:
        raise ValueError("ERROR: something is wrong with your range value")
    
    if mask2 is None:
        mask2 = mask1

    mask1 = mask1.split()
    mask2 = mask2.split()

    for kw in mask1:
        if not ATOMSPATTERN.match(kw):
            raise ValueError("ERROR: something is wrong with your atoms/mask1 value")

    for kw in mask2:
        if not ATOMSPATTERN.match(kw):
            raise ValueError("ERROR: something is wrong with your atoms2/mask2 value")

    mask1 = [ParseAtomsFormat(kw) for kw in mask1]
    mask2 = [ParseAtomsFormat(kw) for kw in mask2]

    if not mask1:
        mask1 = [ParseAtomsFormat(''),]
    if not mask2:
        mask2 = [ParseAtomsFormat(''),]

    atoms1 = ParseAtoms(inpfile1,mask1)

    onesetflag = False

    if inpfile1!=inpfile2 or mask1!=mask2:
        atoms2 = ParseAtoms(inpfile2,mask2)
    else:
        atoms2 = atoms1
        onesetflag = True

    if not atoms1:
        print("No atoms found")
        return []

    if not atoms2:
        print("No atoms2 found")
        return []

    contacts = Atompairs([(a1['Cartn_x'],a1['Cartn_y'],a1['Cartn_z']) for a1 in atoms1],
                         [(a2['Cartn_x'],a2['Cartn_y'],a2['Cartn_z']) for a2 in atoms2],
                         RANGE)       

    if not contacts.shape[0]:
        print("No contacts found")
        return []

    contacts = PrintContacts(contacts, atoms1, atoms2,
                             printing, onesetflag)

    return contacts
    

def Main():

    def PrintUsage():
        print()
        print("Usage:")
        print()
        print("ContExt input=pathto/coordfile [OPTIONS]")
        print()
        print("try --help for a detailed description")
        print()
        exit(1)

    INPFILE1 = None
    INPFILE2 = None
    RANGE    = 10.0
    ATOMS1   = "#"
    ATOMS2   = None

    args = sys.argv[1:]

    if "--help" in args or "-help" in args or "help" in args or\
       "--h" in args or "-h" in args or "h" in args or\
       "--H" in args or "-H" in args or "H" in args:

        HOME_DIR = os.path.dirname(os.path.abspath(__file__))
        
        with open(os.path.join(HOME_DIR,"README.md")) as helpfile:
            print(helpfile.read())
        exit(0)

    for arg in args:

        if arg.startswith("input="):
            INPFILE1 = arg[6:]

        elif arg.startswith("input2="):
            INPFILE2 = arg[7:]

        elif arg.startswith("range="):
            RANGE = arg[6:]

        elif arg.startswith("atoms="):
            ATOMS1 = arg[6:]

        elif arg.startswith("atoms2="):
            ATOMS2 = arg[7:]

    if INPFILE1 is None:
        PrintUsage()

    ContExt(INPFILE1, INPFILE2, RANGE, ATOMS1, ATOMS2, printing = True)


if __name__ == "__main__":

    Main()




