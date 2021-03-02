import mdtraj as md
import sys
import os


'''
conda install -c conda-forge mdtraj pytraj ambertools
'''

if len(sys.argv[:]) != 3:
    print('Usage : python hbond_analysis.py <trajectory> <topology>')
    exit(0)

traj_file = sys.argv[1]
top_file = sys.argv[2]

cpptraj_md = '''parm temp/top.pdb
trajin temp/traj.nc
hbond Backbone avgout BB_hbond.txt series
runanalysis'''

if __name__ == '__main__':
    traj = md.load(traj_file, top=top_file)

    if not os.path.exists('temp'):
        os.mkdir('temp')

    traj.save('temp/traj.nc')
    traj[0].save('temp/top.pdb')

    with open('temp/cpptraj_md', 'w') as f:
        f.write(cpptraj_md)

    cmd = 'cpptraj < temp/cpptraj_md'
    os.system(cmd)

    cmd_rm = 'rm -rf temp'
    os.system(cmd_rm)

    final_lines = []
    with open('BB_hbond.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.split()
        line.append('\n')
        line = ','.join(line)
        final_lines.append(line)
    final_str = ''.join(final_lines)
    with open('hbond.csv', 'w') as f:
        f.write(final_str)

    cmd_rm = 'rm BB_hbond.txt'
    os.system(cmd_rm)
