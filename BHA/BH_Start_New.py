from BHA.Get_Starting_Structure import generate_random_structure


def start_new(self):
    """
    If the algotithm is not resuming, this function initialises parts of the algorithm for a brand new run.
    """
    print("Starting new run of the basin hopping algorithm from a randomly generated starting cluster.")
    self.atoms = generate_random_structure(self.cluster_makeup, self.boxtoplaceinlength, self.vacuumAdd)
    self.atoms.set_calculator(self.calculator)
    unrelaxed_positions = self.atoms.get_positions().copy()
    self.positions = 0.0 * self.atoms.get_positions()

    self.Emin = self.get_transformed_energy(self.atoms.get_positions()) or 1.e32
    self.Emin_found_at = 0
    self.reseed_operator.E_to_beat = self.Emin
    self.rmin = self.atoms.get_positions()
    self.positions = unrelaxed_positions.copy()
    self.hops_accepted_since_reseed = True
    self.steps_completed = 0
    self.reseed_operator.steps_since_improvement = 0

    self.targets_found = []
    if self.exit_when_targets_found and self.target_energies is not None:
        for i in range(len(self.target_energies)):
            self.targets_found.append(False)
            self.target_energies[i] = round(self.target_energies[i], self.rounding)