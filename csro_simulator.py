from csro_nlight import CSRO_Nlight
from csro_dlight import CSRO_Dlight
from csro_motor import CSRO_Motor
from csro_airsys import CSRO_AirSystem

if __name__ == "__main__":
    CSRO_Nlight("ca34bb4e4797", "nlight_nb_4k4r", 4).start()
    CSRO_Nlight("286af026507e", "nlight_nb_4k4r", 4).start()
    CSRO_Nlight("da34bb4e5797", "nlight_nb_4k4r", 4).start()
    CSRO_Nlight("186aa026607e", "nlight_nb_4k4r", 4).start()
    CSRO_Dlight("45ad0904a51a", "dlight_csro_3k3scr").start()
    CSRO_Dlight("46aa0904a614", "dlight_csro_3k3scr").start()
    CSRO_Dlight("47af0904a715", "dlight_csro_3k3scr").start()
    CSRO_Dlight("48ae0904a914", "dlight_csro_3k3scr").start()
    CSRO_Motor("1dee0e45d498", "motor_nb_4k4r", 2).start()
    CSRO_Motor("1dee0e45d408", "motor_nb_4k4r", 2).start()
    CSRO_Motor("1dee0e45d4aa", "motor_nb_4k4r", 2).start()
    CSRO_Motor("1dee0e45d4bb", "motor_nb_4k4r", 2).start()
    CSRO_Motor("1dee0e45d49c", "motor_nb_4k4r", 2).start()
    CSRO_Motor("1dee0e45d49d", "motor_nb_4k4r", 2).start()
    CSRO_AirSystem("dd2faa48e5fc", "airsys_csro").start()
    CSRO_AirSystem("dd2faa48e5fd", "airsys_csro").start()
    CSRO_AirSystem("dd2faa48e5fe", "airsys_csro").start()
    CSRO_AirSystem("dd2faa48e5ff", "airsys_csro").start()
