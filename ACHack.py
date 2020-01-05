from os import system
import threading
from time import sleep
from sys import exit
from ReadWriteMemory import rwm


class ACTrainer:
    # health vars
    healthVar = False
    infHealthValue = False
    healthStatus = 'OFF'
    # ammo vars
    ammoVar = False
    infAmmoValue = False
    ammoStatus = 'OFF'

    # game vars
    gameStatus = 'Offline'

    @staticmethod
    def about():
        system('cls')
        print('=============[Made by SKane]=============')
        print(f'Game Status: [{ACTrainer.gameStatus}]')
        print(f'1. Infinite Health: [{ACTrainer.healthStatus}]')
        print(f'2. Infinite Ammo: [{ACTrainer.ammoStatus}]')
        print('3. Refresh')
        print('4. Exit')

    @staticmethod
    def timer():
        # process handle
        ProcID = rwm.GetProcessIdByName('ac_client.exe')
        hProcess = rwm.OpenProcess(ProcID)

        while True:
            if hProcess == None:
                ACTrainer.gameStatus = 'Offline'
                ACTrainer.healthStatus = '0x0'
                ACTrainer.ammoStatus = '0x0'
            else:
                #Address Variale
                ACTrainer.healthVar = rwm.getPointer(hProcess, 0x00509B74, offsets=[0xF8])
                ACTrainer.ammoVar = rwm.getPointer(hProcess, 0x00509B74, offsets=[0x384,0x14,0x0])
                ACTrainer.gameStatus = 'Online'

                ACTrainer.health = rwm.ReadProcessMemory(hProcess, ACTrainer.healthVar)
                ACTrainer.ammo = rwm.ReadProcessMemory(hProcess, ACTrainer.ammoVar)

                if ACTrainer.infHealthValue == True:
                    rwm.WriteProcessMemory(hProcess, ACTrainer.healthVar, 100)
                    ACTrainer.healthStatus = 'ON'
                else:
                    ACTrainer.healthStatus = 'OFF'

                if ACTrainer.infAmmoValue == True:
                    rwm.WriteProcessMemory(hProcess, ACTrainer.ammoVar, 20)
                    ACTrainer.ammoStatus = 'ON'
                else:
                    ACTrainer.ammoStatus = 'OFF'
            sleep(0.01)


def main():
    while True:
        ACTrainer.about()
        option = input('Toggle Option: ')
        if int(option) == 3:
            pass
        elif int(option) == 4:
            exit()
        else:
            if ACTrainer.gameStatus == 'Online':
                try:
                    if int(option) == 1:
                        ACTrainer.infHealthValue = not ACTrainer.infHealthValue
                    elif int(option) == 2:
                        ACTrainer.infAmmoValue = not ACTrainer.infAmmoValue
                    else:
                        print("That option doesn't exist!")
                        sleep(1)
                except:
                    print('The option must be an integer!')
                    sleep(1)
            elif ACTrainer.gameStatus == 'Offline':
                print("The game isn't running!")
                sleep(1)
            else:
                print('An error has occured')
                exit()


t1 = threading.Thread(target=ACTrainer.timer)
if __name__ == '__main__':
    t1.start()
    main()
