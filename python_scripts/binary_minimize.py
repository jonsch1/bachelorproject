# script to minimize full ternary complex

import os, sys

BABEL = os.getenv('BABEL')
MOL2PARAMS = os.getenv('MOL2PARAMS')
MINIMIZE = os.getenv('MINIMIZE')

if BABEL is None:
    print("Need babel path")
    sys.exit()

if MOL2PARAMS is None:
    print("Need Rosetta mol2params path")
    sys.exit()

if MINIMIZE is None:
    print("Need Rosetta minimize path")
    sys.exit()

# takes a comma separated list of ligand names
ligand_names = sys.argv[2].split(',')

# first, read in binary.pdb list

pdb_list = []
pdb_list_file = open(sys.argv[1], 'r')
for line in pdb_list_file:
    name = line.strip()
    pdb_list.append(name)
pdb_list_file.close()


def main():
    for pdb in pdb_list:
        # make ligand param files:
        params_files = []
        for ligand_name in ligand_names:
            pdb_file = open(pdb, "r")
            ligand_file_name = pdb.strip(".pdb") + "_lig_" + ligand_name
            # extract the ligand into a new pdb file
            ligand_pdb_name = ligand_file_name + ".pdb"
            ligand_pdb_file = open(ligand_pdb_name, "w")
            for line in pdb_file:
                if line.startswith("HETATM") and ligand_name in line:
                    print(ligand_name, line)
                    ligand_pdb_file.write(line)

            ligand_pdb_file.close()

            print(ligand_pdb_name + " was succesfully created!")

            # create mol2 file for ligand
            mol2_name = ligand_file_name + ".mol2"
            command = "obabel" + " -h -ipdb " + ligand_pdb_name + " -omol2 -O " + mol2_name
            print("About to run: " + command)
            os.system(command)
            print(mol2_name + " was succesfully created!")

            # create params file from the mol2 file
            command = "python " + MOL2PARAMS + " " + mol2_name + " -n " + ligand_name + " -p " + ligand_file_name + " --no-pdb  --clobber"
            print("About to run: " + command)
            os.system(command)

            params_files.append(ligand_file_name + ".params")

            print(ligand_file_name + ".params" + " was succesfully created!")

            pdb_file.close()

        # use params files to minimize the structure
        command = MINIMIZE + " -s " + pdb + " --extra_res_fa " + params_files[0] + " " + params_files[
            1] + " -ignore_zero_occupancy false" + " >> output.txt"  # --no-param
        print("Currently minimizing: " + pdb)
        os.system(command)


main()
