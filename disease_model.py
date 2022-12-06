import random

def infect(infect_prob: float)->bool:
    """takes a float giving the infection probability for the disease,
    and randomly returns True or False,indicating if an infection has occurred."""

    prob = random.uniform(0,1)
    if prob < infect_prob:
        return True
    else:
        return False

def recover(recover_chance: float)->bool:
    """takes a float giving the recover probability for the disease,
    and randomly returns True or False,indicating if a recovering has occurred."""

    prob = random.uniform(0,1)
    if prob < recover_chance:
        return True
    else:
        return False

def contact_indices(pop_size:int, source: int, contact_range: int)->list:
    """It takes three arguments: the size of the population (pop size);
     the index of the infected person (source);
     and a positive integer giving the contact range (contact range), and
     returns the list of indicies of the people."""
    
    contacts =[]
    for i in range(source - contact_range, source+contact_range+1):
        if i >=0 and i < pop_size:
            contacts.append(i)
    return contacts

def apply_recoveries(population:list, recover_chance: float)->None:
    """Takes the list of strings (population) giving the status of the population, and the recovery
     probability for the disease (described in the description of recover)."""

    for index in range (len(population)):
        recovered = recover(recover_chance)
        if recovered:
            population[index] = "R"

def contact(population:list, contact_range:int, source: int, infect_chance: int)->None:
    """It takes four arguments: the list of strings giving the status of the population
    (population); the index of the infected person (source);
    an integer giving the contact range (contact range),
    described in the instructions for contact indices;
    and the infection probability of the disease (infect chance)."""

    contacts = contact_indices(len(population), source, contact_range)
    for index in contacts:
        infected = infect(infect_chance)
        if infected:
            population[index] = "I"
            
def apply_contacts(population:list, contact_range:int, infect_chance:float) -> None:
    """Iterates through population, making a list of currently infected people,
     and possibly infecting each of their neighbors"""

    infected = []
    for index in range(len(population)):
        if population[index] == "I":
            infected.append(index)
    for sick_person in infected:
        contact(population, contact_range, sick_person, infect_chance)

def population_SIR_counts(population:list) -> dict:
    """Takes a population and returns a count of people that are susceptible,
    infected, and recovered in a dictionary"""

    SIR_count = {}
    SIR_count["infected"] = 0
    SIR_count["susceptible"] = 0
    SIR_count["recovered"] = 0
    for index in range(len(population)):
        if population[index] == "I":
            SIR_count["infected"] += 1
        if population[index] == "S":
            SIR_count["susceptible"] += 1
        if population[index] == "R":
            SIR_count["recovered"] += 1
    return SIR_count

def simulate_day(population:list, contact_range:int, infect_chance:float, recover_chance:float) -> None:
     """Takes the inputs (population, contact_rance, infect_chance, and
        recover_chance, and simulates one day in the progression of the disease"""
     apply_recoveries(population, recover_chance)
     apply_contacts(population, contact_range, infect_chance)


def initialize_population(pop_size:int) -> list:
    population = ['S'] * pop_size
    population[0] = 'I'
    return population

def simulate_disease(pop_size:int, contact_range:int, infect_chance:float, recover_chance:float) -> list:
    population = initialize_population(pop_size)
    counts = population_SIR_counts(population)
    all_counts = [counts]
    while counts['infected'] > 0:
        simulate_day(population, contact_range, infect_chance, recover_chance)
        counts = population_SIR_counts(population)
        all_counts.append(counts)
    return all_counts

def peak_infections(all_counts:list) -> int:
    max_infections = 0
    for day in all_counts:
        if day['infected'] > max_infections:
            max_infections = day['infected']
    return max_infections
        
def display_results(all_counts:list) -> None:
    num_days = len(all_counts)
    print("Day".rjust(12) + "Susceptible".rjust(12) + "Infected".rjust(12) + "Recovered".rjust(12))
    for day in range(num_days):
        line = str(day).rjust(12)
        line += str(all_counts[day]["susceptible"]).rjust(12)
        line += str(all_counts[day]["infected"]).rjust(12)
        line += str(all_counts[day]["recovered"]).rjust(12)
        print(line)
    print("\nPeak Infections: {}".format(peak_infections(all_counts)))


