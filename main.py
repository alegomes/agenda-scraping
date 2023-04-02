import ams_carre
import ams_dekleine
import ams_delamar
import ams_meervaart

from file_saver import FileSaver

def main():
    ams_carre.main(FileSaver('ams-carre'))
    ams_dekleine.main()
    ams_delamar.main()
    ams_meervaart.main()

if __name__ == '__main__':
    main()
