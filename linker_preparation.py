import sys,os

ligand_editor = os.path.join(os.path.dirname(__file__), "ligand_editor.py")
location_of_script = os.path.dirname(__file__)
def main():

    linker_name = sys.argv[1]
    smiles_string = sys.argv[2]

    print('creating 3D molecule from Smiles String')
    file_name = linker_name+'.sdf'
    command = 'obabel -:"'+ smiles_string +'" -O '+file_name+' --gen3D'
    print('using the command ', command)
    os.system(command)

    print('generating conformers')
    command = 'obabel '+file_name+' -O '+file_name+' --confab'
    print('using the command ', command)
    os.system(command)

    print('creating pymol script file')
    pymol_script_file = open('pymol_script.pml', 'w')
    pymol_script_file.write('load ' + file_name + ' \n')
    pymol_script_file.write('multifilesave {name}-{state}.pdb, state=0')
    pymol_script_file.close()

    print('running pymol script file')
    command = 'pymol -c pymol_script.pml'
    os.system(command)

    print('deleting pymol script file')
    command = 'rm pymol_script.pml'
    os.system(command)

    print('generating linker_list.txt file')
    command = 'ls *.pdb > linker_list.txt'
    os.system(command)

    print('altering atom_names')
    command = '{} {} {}'.format('python', ligand_editor, 'linker_list.txt UNK')
    os.system(command)

    # printf '../alkylC6_conformers/%s\n' edited * > linker_list.txt
    print('updating linker_list.txt file')
    command = 'ls edited*.pdb > linker_list.txt'
    os.system(command)

main()