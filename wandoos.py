#!/usr/bin/env python3
"""
        A script made by mazunki (2019) to help players with Wandoos in NGU.

        Based on NGU Idle, a game by 4G/paraguayyyy, this script is only a helper
        program for players. All credits for the game goes to the original author, and
        by using this script you are responsible for all actions involved in using/sharing
        it.

        Have fun!
"""

import math, decimal

################
# Name holders #
################

W98, WMEH, WXL = "W98", "WMEH", "WXL"
NORMAL, EVIL = "NORMAL", "EVIL"


###############
# Game values #
###############

FPS = 50

EL_DICT = {
        W98:    1/100, 
        WMEH:   1/5, 
        WXL:    6
}
ML_DICT = {
        W98:    1/25, 
        WMEH:   2, 
        WXL:    40
}
ML_POWER = {
        W98:    0.8,
        WMEH:   1.0, 
        WXL:    1.05
}
BASE_CAPS = {
        W98:    1E9,
        WMEH:   1E12,
        WXL:    1E15
}
BASE_CAPS_EVIL = {
        W98: 1E12,
        WMEH: 1E27,
        WXL: 1E33
}


##############################
######  Configuration  #######
##############################

ONLINE = True
RUNNING_TIME = 60*60  # seconds
VERBOSE = True

EQ = 0
OS_LVL_MOD = 4.36  # I assume this depends on OS.
BOOTUP = 1.1  # no clue why this is 1.1, but
ADV_TR = 0.01
NGU = 1.0
CHAL_100_MOD = 1.0
# use the following if lazy
total_mult = 150.48

ENERGY_INPUT = int(95e6)
MAGIC_INPUT = int(7.5E6)


#################################
###### End of global scope ######
#################################



class Wandoos:
        """
        Configuration and status of a Wandoos machine, allowing the user to 
        simulate events according to their progress.
        """

        def __init__(self,
                                 OS=W98,
                                 el=0,
                                 ml=0,
                                 bootup=1.0,
                                 mode=NORMAL,
                                 allocated_energy=ENERGY_INPUT,
                                 allocated_magic=MAGIC_INPUT
                ):
                self.OS = OS
                self.el = el
                self.ml = ml
                self.bootup = bootup
                self.mode = mode
                self.allocated_energy = allocated_energy
                self.allocated_magic = allocated_magic

        def output(self):
                """Returns the Wandoos multiplier the player would get depending on current levels""" 
                el_ = self.el * EL_DICT[self.OS]
                ml_ = self.ml * ML_DICT[self.OS]
                mlm_ = ML_POWER[self.OS]

                return ((1+el_) * (1+ml_))**mlm_

        def get_cap(self):
                """
                Returns the amount of resource the OS needs to 1-cap levelling
                Check configuration section above to tweak Wandoos multipliers (Same as Wandoos stats breakdown)
                """

                base = 1.0
                multiplier = base * (1+EQ) * (1+OS_LVL_MOD) * (self.bootup) * (1+ADV_TR) * (1+NGU) * (1+CHAL_100_MOD)
                if total_mult is not 0:
                    multiplier = total_mult
                base_cap = BASE_CAPS[self.OS] if self.mode==NORMAL else BASE_CAPS_EVIL[self.OS]
                raw_cap = base_cap / multiplier

                if VERBOSE: print("Multiplier: ", multiplier)
                return raw_cap

        def frames_to_level(self, allocated_resource, res="resource"):
                """
                        Using self.get_cap(), returns the number of frames needed to gain a level. 
                        Takes care about online/offline status.
                """
                fraction_of_cap = allocated_resource / self.get_cap()

                if fraction_of_cap > 1:
                        fraction_of_bar = 1
                        print(f"You don't need that much {res}! You're {(fraction_of_cap-1)*100:.{2}f}% in excess!")
                else:
                        fraction_of_bar = math.floor(1/fraction_of_cap)+1

                if VERBOSE: print("Ticks per level: ", fraction_of_bar, " (", fraction_of_bar/50, " seconds)", sep="")

                return fraction_of_bar if ONLINE else min(fraction_of_cap, 1)

        def energy_per_second(self):
                """ Returns levels of Energy given in one second """
                frames_per_level = self.frames_to_level(self.allocated_energy, res="energy")

                one_second = FPS / frames_per_level
                return one_second

        def magic_per_second(self):
                """ Returns levels of Magic given in one second """
                frames_per_level = self.frames_to_level(self.allocated_magic, res="magic")

                one_second = FPS / frames_per_level
                return one_second

        def leave_running(self, seconds, run_energy=True, run_magic=True):
                """ Simulates running the wandoos machine for `seconds` amount of seconds, and
                updates energy/magic levels accordingly """

                start_el = self.el
                if run_energy:
                        print("Running energy...")
                        self.el += math.floor(self.energy_per_second() * seconds)
                print("\tGot", self.el - start_el, "energy levels")
                print()

                start_ml = self.ml
                if run_magic:
                        print("Running magic...")
                        self.ml += math.floor(self.magic_per_second() * seconds)
                print("\tGot", self.ml - start_ml, "magic levels")
                print()



if __name__ == '__main__':
        My_Wandoos_98 = Wandoos(OS=W98, el=0, ml=0, bootup=1.1)
        My_Wandoos_MEH = Wandoos(OS=WMEH, el=0, ml=0, bootup=1.1)
        My_Wandoos_XL = Wandoos(OS=WXL, el=0, ml=0, bootup=1.1)


        for computer in [My_Wandoos_98, My_Wandoos_MEH, My_Wandoos_XL]:
                print(computer.OS)
                print("="*32)
                print(computer.allocated_energy, "energy")
                print(computer.allocated_magic, "magic")
                print()
                computer.leave_running(RUNNING_TIME)
                print()

                print("Multiplier: {:.2E}".format(decimal.Decimal(computer.output())))
                print("="*64)
                print("="*64,"\n\n")
