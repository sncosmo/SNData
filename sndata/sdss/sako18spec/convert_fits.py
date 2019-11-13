"""
To Install IRAF on Mac
conda config --add channels http://ssb.stsci.edu/astroconda
conda create -n iraf27 python=2.7 iraf-all pyraf-all stsci
conda activate iraf27

The IRAF commands are as follows. Specify xgterm as the terminal type.
$ mkiraf
$ xgterm -fn 10*20 -sbr -e cl
ecl> task $convert_fits = convert_fits.cl
ecl> echo = yes
ecl> convert_fits
"""

from pathlib import Path

parent = Path(__file__).parent
out_dir = parent / 'data/Spectra_txt/'
in_dir = parent / 'data/Spectra/'
out_cl_file = out_dir / 'convert_fits.cl'
in_dir_relative = in_dir.relative_to(out_cl_file.parent.parent)

if __name__ == '__main__':

    file_list = in_dir.glob('*.fits')

    out_dir.mkdir(exist_ok=False)
    with open(out_cl_file, 'w') as ofile:
        for file_path in file_list:
            ofile.write(
                f'wspectext ../{in_dir_relative / file_path.stem}.fits[*,1] {file_path.stem}.txt header=no\n'
            )
