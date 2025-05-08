from dewan_h5_git.dewan_h5 import DewanH5
from pathlib import Path
from tqdm import tqdm


def main():
    data_dir = Path('/mnt/r2d2/11_Data/GoodSniffData')
    h5_files = list(Path(data_dir).glob('*.h5'))

    for h5_file in tqdm(h5_files, total=len(h5_files)):
        try:
            with DewanH5(h5_file) as h5:
                pass
        except Exception as e:
            print(f'Error reading {h5_file}!')
            print(e)
if __name__ == "__main__":
    main()