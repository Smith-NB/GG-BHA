from BHA.Lock import lock_check_and_set
from BHA.Search_Strategies.Get_Search_Strategy import get_search_strategy
from BHA.Reseed_Operators.Get_Reseed_Operator import get_reseed_operator
from BHA.Get_Starting_Structure import get_calculator
from BHA.Timer import Timer
from ase.io.trajectory import Trajectory
from os import path
import sys

def initialise(self):
    """
    Initialize the BHA.
    """
    lock_check_and_set()
    print_banner()
    print_self_information(self)
    

    self.calculator = get_calculator(self.calculator_information)
    self.reseed_operator = get_reseed_operator(self.reseed_operator_information)

    if path.exists("information_for_resuming.txt"):
        from BHA.BH_Resume import resume
        resume(self)
    else:
        from BHA.BH_Start_New import start_new
        start_new(self)
    

    #Get Calculator from calculator information
    

    if self.adjust_cm:
        self.cm = self.atoms.get_center_of_mass()
    else:
        self.cm = None

    if isinstance(self.lm_trajectory, str):
        self.lm_trajectory = Trajectory(self.lm_trajectory, 'a', self.atoms)
    if isinstance(self.lowest_trajectory, str):
        self.lowest_trajectory = Trajectory(self.lowest_trajectory, 'a', self.atoms)
    if isinstance(self.logfile, str):
        if self.logfile == '-':
            self.logfile = sys.stdout
        elif not path.exists(self.logfile):
            self.logfile = open(self.logfile, 'a')
            self.log(-1, self.Emin, self.Emin, True, None)
        else:
            self.logfile = open(self.logfile, 'a')
    if isinstance(self.cnalog, str):
        self.cnalog = open(self.cnalog, 'a')



    self.positions = self.atoms.get_positions() #sets positions to relaxed state of starting structure.
    self.cell = self.atoms.get_cell()
    #opens up a two way line of communication between the search strategy Object and the reseed operator Object 
    self.search_strategy_information['reseed_operator_pointer'] = self.reseed_operator
    self.search_strategy = get_search_strategy(self.search_strategy_information)

    self.cluster_chemical_formula = ''
    self.timer = Timer(self.total_length_of_running_time)
    for element, no_of_element in self.cluster_makeup.items():
        self.cluster_chemical_formula += str(element+str(no_of_element))


def print_banner():
    """
    Print the algorithm banner.
    """

    banner = ''
    banner += '================================================\n'
    banner += '\n'
    banner += '______           _                              \n'
    banner += '| ___ \\         (_)                             \n'
    banner += '| |_/ / __ _ ___ _ _ __                         \n'
    banner += '| ___ \\/ _` / __| | \'_ \\                        \n'
    banner += '| |_/ / (_| \\__ \\ | | | |                       \n'
    banner += '\\____/ \\__,_|___/_|_| |_|                       \n'
    banner += '                                                \n'
    banner += '                                                \n'
    banner += ' _   _                   _                      \n'
    banner += '| | | |                 (_)                     \n'
    banner += '| |_| | ___  _ __  _ __  _ _ __   __ _          \n'
    banner += '|  _  |/ _ \\| \'_ \\| \'_ \\| | \'_ \\ / _` |         \n'
    banner += '| | | | (_) | |_) | |_) | | | | | (_| |         \n'
    banner += '\\_| |_/\\___/| .__/| .__/|_|_| |_|\\__, |         \n'
    banner += '            | |   | |             __/ |         \n'
    banner += '            |_|   |_|            |___/          \n'
    banner += '  ___  _                  _ _   _               \n'
    banner += ' / _ \\| |                (_) | | |              \n'
    banner += '/ /_\\ \\ | __ _  ___  _ __ _| |_| |__  _ __ ___  \n'
    banner += '|  _  | |/ _` |/ _ \\| \'__| | __| \'_ \\| \'_ ` _ \\ \n'
    banner += '| | | | | (_| | (_) | |  | | |_| | | | | | | | |\n'
    banner += '\\_| |_/_|\\__, |\\___/|_|  |_|\\__|_| |_|_| |_| |_|\n'
    banner += '          __/ |                                 \n'
    banner += '         |___/                                  \n'
    banner += '\n'
    banner += '================================================\n'

    banner += 'X    .    .    .    .    .     .    .  .    .      .   .  .    .  .   .  .   .   .   .   .   \n'
    banner += 'X  .  .  . .  .  . .  .  . .  .:X@%. .  .  . .  .  . . %@X@: . :@@@S. . .%@@: .  . . X@SSSS::\n'
    banner += 'X      .       .       .      :X  S8.    .       .   .8S. .@@.:X   @@  .8S .8S     .8S       \n'
    banner += 'X   .    .  .    .  .    .  . 8S   8X .    .  .    . @@     @8X    .8. :8  .:8. .  :8  . . . \n'
    banner += 'X    .       .       .       :8.   :8.  .      .    :8.  ____S_____ 8S X .   8%   .8%        \n'
    banner += 'X  .   .  .    .  .    .  ..SX   .  X@    . .    .  8%   |   .    | :8S8  . .:8   :8   .  .  \n'
    banner += 'X8888 .    . ..  .  .   . %@S.      :8. .     .   .:8    | .  .   |_________  X   X@        .\n'
    banner += 'X .:8X  .  .XXX8.     . .8X.   . .  .X     .    .  X .   |    .   .   .    |  8  .X  . . .   \n'
    banner += 'X    .8%  .8%  :8.  .  :X   .     .  S8. .   .    .X     |  .   .    .     |  %8 :8.       . \n'
    banner += 'X   . :8  %8. . 8%     8S .   .      :8        .  :8     |    .  .  .  .   |  .8 %8   .  .   \n'
    banner += 'X      8S X     %8. . :8.   .   .  . .X  . . .   .X      |  .   .    .   . | . X 8% .      . \n'
    banner += 'X   . .:88X  .  .X    @X  .      .    @X       .  X . .  |    .   .    .   | ..%@8.     .   .\n'
    banner += 'X______________  @X   X      . .    . :8.  .     :8      |  .       .     .|_________________\n'
    banner += 'X . .  .    . |  %8  :8  .  .     .   :8 .   .   %8.  .  |     . .    .  .  .    .     .   . \n'
    banner += 'X    .  .  .  | ..8  @S   .    .     . X      .  8S      |   .     .    .   .  . .   .  .  . \n'
    banner += 'X       . .   |   @S  X  .    .   .  . @X . .   .8. .    |  .   .    .    .        .     .   \n'
    banner += 'X  .  .   .   |.  cX 8     .   .       %8     . :8    .  |    .   .    .    . .  .   . .     \n'
    banner += 'X   .    . .  |   .88S   .        .  . :8  .    %8 .     |  .       .    .         .      .  \n'
    banner += 'X      .      |_____8_____________      X    .  8%   .   |     . .    .    .  . .     .    . \n'
    banner += 'X  .  .   .  .    .    .   .   . |  .   8% .   .X  .     |   .     .    .         .  .  .    \n'
    banner += 'X       .      .     . . .  . .  |    . X@     :8    .   |     .    .     . .  .   .      .  \n'
    banner += 'X   .      .     .  .        . . |  .   :8  .  S8  .     |  .    .    . .       .     .  .  .\n'
    banner += 'X    . .  .  . .       .  .    . |    . .8.  . 8%.    .  |    .   .        . .    .     .    \n'
    banner += 'X                . .     .  .    |  .    X    .X    .    |  .   .   . .  .     .    . .    . \n'
    banner += 'X  .  . .  . .       . .      .  |     . X: .  8  .      |              .   .    .       .   \n'
    banner += 'X         .    .  .       .      |  .    :8   S@     .   | .  .  . .  .   .   .    .  .     .\n'
    banner += 'X   .  .     .      .  .    . .  |    . . 8. .8%  .   .  |     .                .   .   .  . \n'
    banner += 'X    .   .     . .    .  .       |  .     8X :8.    .    |  .    .  . . .  . .    .      .   \n'
    banner += 'X  .       . .     .       .  .  |     .  :8.8S  .       |    .    .      .    .     . .     \n'
    banner += 'X     . .       .    .  .   .    |  .      888.      .   |  .   .     .      .   . .      .  \n'
    banner += 'X   .     .  .    .    .  .  .   |__________8____________|    .   .     .  .   .      .  .  .\n'
    banner += 'X     .    .   .    .        .  .   .     .    .    .   . . .       . .   .       .  .       \n'
    banner += 'X   .   .    .   .    .  .  .   . . .  .  .  .  . . . .        . .      .   . . .      .  .  \n'
    banner += 'X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X\n'
    print(banner)

def print_self_information(self):
    """
    Print parameter values recieved by the algorithm. This does not include search strategy information.
    """
    to_print = ''
    to_print += '\nCluster makeup: ' + str(self.cluster_makeup)
    to_print += '\nfmax: ' + str(self.fmax)
    to_print += '\nStep-width (dr): ' + str(self.dr)
    to_print += '\nBox to place in length: ' + str(self.boxtoplaceinlength)
    to_print += '\nVacuum Add: ' + str(self.vacuumAdd)
    to_print += '\nEnd algorithm when GM found? '
    if self.exit_when_targets_found:
        to_print += 'Yes'
        to_print += '\nGM Energy: ' + str(self.target_energies) + ' eV'
        to_print += '\nGM Energy rounding: ' + str(self.rounding) + ' dp'
    else:
        to_print += 'No'
    s = 'Yes' if self.adjust_cm else 'No'
    to_print += '\nAdjust centre of masss? ' + s
    to_print += '\nTotal Lenghth of Running Time: ' + str(self.total_length_of_running_time) + ' hrs'
    print(to_print)



