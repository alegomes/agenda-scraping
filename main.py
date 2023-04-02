import ams_carre
import ams_dekleine
import ams_delamar
import ams_meervaart

from file_saver import FileSaver

def main():
    ams_carre.main(FileSaver('ams-carre'))
    ams_dekleine.main(FileSaver('ams-dekleine'))
    ams_delamar.main(FileSaver('ams-delamar'))
    ams_meervaart.main(FileSaver('ams-meervaart'))

if __name__ == '__main__':
    main()
