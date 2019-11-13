from pathlib import Path

out_cl_file = 'convert_fits.cl'
file_list = Path(__file__).parent.glob('data/Spectra/*.fits')

with open(out_cl_file, 'w') as ofile:
    for file_path in file_list:
        command = f'wspectext {file_path.stem}.fits[*,1] {file_path.stem}.txt\n'
        ofile.write(command)

# The IRAF commands are as follows. Specify xgterm as the terminal type
# $ make iraf
# $ xgterm -fn 10*20 -sbr -e cl
# ecl> task convert_fits = convert_fits.cl
# ecl> echo = yes
# ecl> convert_fits
