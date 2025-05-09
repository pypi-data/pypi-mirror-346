from multiprocessing import freeze_support

from topoly import homfly, alexander, jones

if __name__ == '__main__':
    freeze_support()
    print(homfly('data/knots/1j85.xyz', run_parallel=False, tries=1))