import os
import sys

pdb_list = []
pdb_file = open(sys.argv[1], 'r')
for line in pdb_file:
    name = line.strip()
    pdb_list.append(name)
pdb_file.close


def main():
    for pdb in pdb_list:
        file_name = pdb

        # takes a comma separated list of ligands
        ligand_names = sys.argv[2].split(',')
        # compatible with the following atoms:

        file = open(file_name, 'r')
        output = open("edited_" + file_name, "w")
        print(file_name, ligand_names)

        C_counter = 1
        O_counter = 1
        N_counter = 1
        S_counter = 1
        F_counter = 1
        H_counter = 1

        # initialize variable
        remember_residue = 'initial'

        for line in file:
            residue_name = line[17:20]
            # count for each atom type separately (C1,C2, N1, N2 ...)
            if residue_name in ligand_names:

                if residue_name != remember_residue:
                    C_counter = 1
                    O_counter = 1
                    N_counter = 1
                    S_counter = 1
                    F_counter = 1
                    H_counter = 1

                atom_name = line[77:78].strip()
                # generate an atom_counter for each atom type
                # f"{atom_name}_counter"+=1
                if atom_name == "C":
                    atom_number = C_counter
                    C_counter += 1
                if atom_name == "O":
                    atom_number = O_counter
                    O_counter += 1
                if atom_name == "N":
                    atom_number = N_counter
                    N_counter += 1
                if atom_name == "S":
                    atom_number = S_counter
                    S_counter += 1
                if atom_name == "F":
                    atom_number = F_counter
                    F_counter += 1
                if atom_name == "H":
                    atom_number = H_counter
                    H_counter += 1

                # makes sure that atom name is 4 characters long
                new_atom_name = f"{atom_name + str(atom_number):<4}"
                new_line = 'HETATM' + line[6:12] + new_atom_name + line[12 + len(new_atom_name):]
                output.write(new_line)

                # keep track of last residue, since want to reset counters for each residue
                remember_residue = residue_name
            else:

                output.write(line)

        file.close()
        output.close()

    # add a command that removes the original file


if __name__ == '__main__':
    main()
