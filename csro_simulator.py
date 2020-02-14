from csro_nlight import CSRO_Nlight
from csro_dlight import CSRO_Dlight
from csro_motor import CSRO_Motor
from csro_airsys import CSRO_AirSystem

if __name__ == "__main__":
    nlight1 = CSRO_Nlight("abababcdcdcd", "nlight_nb_4k4r", 4)
    nlight1.start()
    print("1 started")

    nlight2 = CSRO_Nlight("abababcdcdce", "nlight_nb_4k4r", 4)
    nlight2.start()
    print("2 started")

    dlight1 = CSRO_Dlight("00075e3e2d3c", "dlight_csro_3k3scr")
    dlight1.start()
    print("3 started")

    motor1 = CSRO_Motor("00075e4e2d3c", "motor_nb_4k4r", 2)
    motor1.start()
    print("4 started")

    airsys1 = CSRO_AirSystem("00075e4e2e3c", "airsys_csro")
    airsys1.start()
    print("5 started")
