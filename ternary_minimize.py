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

# first, read in ternary.pdb list
pdb_list = []
pdb_list_file = open(sys.argv[1], 'r')
for line in pdb_list_file:
    name = line.strip()
    pdb_list.append(name)
pdb_list_file.close()


def main():
    for pdb in pdb_list:

        # make protac param file:
        pdb_file = open(pdb, "r")
        protac_file_name = pdb.strip(".pdb") + "_protac"
        # extract the protac into a new pdb file
        protac_pdb_name = protac_file_name + ".pdb"
        protac_pdb_file = open(protac_pdb_name, "w")
        for line in pdb_file:
            if line.startswith("HETATM") and "LG1" in line:
                protac_pdb_file.write(line)

        protac_pdb_file.close()

        print(protac_pdb_name + " was succesfully created!")

        # create mol2 file for protac
        mol2_name = protac_file_name + ".mol2"
        command = "obabel" + " -h -ipdb " + protac_pdb_name + " -omol2 -O " + mol2_name
        print("About to run: " + command)
        os.system(command)
        print(mol2_name + " was succesfully created!")

        # create params file from the mol2 file
        command = "python " + MOL2PARAMS + " " + mol2_name + " -n LG1" + " -p " + protac_file_name + " --no-pdb  --clobber"
        print("About to run: " + command)
        os.system(command)

        params_file = protac_file_name + ".params"

        print(protac_file_name + ".params" + " was succesfully created!")

        # remove mol2 file, as it was only needed to generate a params file
        command = "rm *.mol2"
        print("About to run: " + command)
        os.system(command)

        pdb_file.close()

        # use params files to minimize the structure
        command = MINIMIZE + " -s " + pdb + " --extra_res_fa " + params_file + " -ignore_zero_occupancy false" + " >> output.txt"  # --no-param
        print("Currently minimizing: " + pdb)
        os.system(command)


main()
