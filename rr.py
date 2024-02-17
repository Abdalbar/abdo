'''Rules:
IF Room Temperature IS Low AND Humidity IS Low AND Number of People IS Few  THEN Thermostat Temperature IS Very High
IF Room Temperature IS Low AND Humidity IS Low AND Number of People IS Many   THEN Thermostat Temperature IS High
IF Room Temperature IS Low AND Humidity IS Medium                            THEN Thermostat Temperature IS High
IF Room Temperature IS Low AND Humidity IS High                              THEN Thermostat Temperature IS Moderately High
IF Room Temperature IS Medium AND Humidity IS Low AND Number of People IS Few THEN Thermostat Temperature IS Moderately Low
IF Room Temperature IS Medium AND Humidity IS Low AND Number of People IS Many THEN Thermostat Temperature IS Low
IF Room Temperature IS Medium AND Humidity IS Medium                          THEN Thermostat Temperature IS Very Low
IF Room Temperature IS Medium AND Humidity IS High AND Number of People IS Few THEN Thermostat Temperature IS Low
IF Room Temperature IS Medium AND Humidity IS High AND Number of People IS Many THEN Thermostat Temperature IS Moderately Low
IF Room Temperature IS High AND Humidity IS Low AND Number of People IS Few   THEN Thermostat Temperature IS Moderately Very Low
IF Room Temperature IS High AND Humidity IS Low AND Number of People IS Many  THEN Thermostat Temperature IS Very Low
IF Room Temperature IS High AND Humidity IS Medium                            THEN Thermostat Temperature IS Very Low
IF Room Temperature IS High AND Humidity IS High AND Number of People IS Few   THEN Thermostat Temperature IS Very Low
IF Room Temperature IS High AND Humidity IS High AND Number of People IS Many  THEN Thermostat Temperature IS Extremely Low
=====================================================================
 
'''
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def sqrt(num):
    return num**0.5
    
def square(num):
    return num**2
    
# Generate the universe of discourse for fuzzy sets as numpy arrays
temperature = ctrl.Antecedent(np.arange(15, 36, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
people = ctrl.Antecedent(np.arange(0, 31, 1), 'people')
thermostat = ctrl.Consequent(np.arange(15, 36, 1), 'thermostat')

# Generate membership function values with trimf to create triangular membership functions for temperature
temperature['low'] = fuzz.trimf(temperature.universe, [15, 15, 25])
temperature['medium'] = fuzz.trimf(temperature.universe, [23, 25, 29])
temperature['high'] = fuzz.trimf(temperature.universe, [27, 35, 36])

# Generate membership function values with trimf to create triangular membership functions for humidity
humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 41])
humidity['medium'] = fuzz.trimf(humidity.universe, [35, 55, 76])
humidity['high'] = fuzz.trimf(humidity.universe, [70, 100, 101])

# Generate membership function values with trimf to create triangular membership functions for people
people['few'] = fuzz.trimf(people.universe, [0, 0, 21])
people['many'] = fuzz.trimf(people.universe, [10, 30, 31])

# Generate membership function values with trimf to create triangular membership functions for people
thermostat['slightly low'] = np.array(list(map(sqrt, fuzz.trimf(temperature.universe, [15, 15, 25]))))
thermostat['low'] = fuzz.trimf(temperature.universe, [15, 15, 25])
thermostat['very low'] = np.array(list(map(square, fuzz.trimf(temperature.universe, [15, 15, 25]))))
thermostat['slightly medium'] = np.array(list(map(sqrt, fuzz.trimf(temperature.universe, [23, 26, 30]))))
thermostat['medium'] = fuzz.trimf(temperature.universe, [23, 26, 30])
thermostat['very medium'] = np.array(list(map(square, fuzz.trimf(temperature.universe, [23, 26, 30]))))
thermostat['slightly high'] = np.array(list(map(sqrt, fuzz.trimf(temperature.universe, [27, 35, 36]))))
thermostat['high'] = fuzz.trimf(temperature.universe, [27, 35, 36])
thermostat['very high'] = np.array(list(map(square, fuzz.trimf(temperature.universe, [27, 35, 36]))))

# Create a list of fuzzy rules using ctrl.Rule
rulebase = [ctrl.Rule(temperature['low'] & humidity['low'] & people['few'], thermostat['very high']),
            ctrl.Rule(temperature['low'] & humidity['low'] & people['many'], thermostat['high']),
            ctrl.Rule(temperature['low'] & humidity['medium'], thermostat['high']),
            ctrl.Rule(temperature['low'] & humidity['high'], thermostat['slightly high']),
            ctrl.Rule(temperature['medium'] & humidity['low'] & people['few'], thermostat['slightly medium']),
            ctrl.Rule(temperature['medium'] & humidity['low'] & people['many'], thermostat['medium']),
            ctrl.Rule(temperature['medium'] & humidity['medium'], thermostat['very medium']),
            ctrl.Rule(temperature['medium'] & humidity['high'] & people['few'], thermostat['medium']),
            ctrl.Rule(temperature['medium'] & humidity['high'] & people['many'], thermostat['slightly medium']),
            ctrl.Rule(temperature['high'] & humidity['low'] & people['few'], thermostat['slightly low']),
            ctrl.Rule(temperature['high'] & humidity['low'] & people['many'], thermostat['low']),
            ctrl.Rule(temperature['high'] & humidity['medium'], thermostat['low']),
            ctrl.Rule(temperature['high'] & humidity['high'] & people['few'], thermostat['low']),
            ctrl.Rule(temperature['high'] & humidity['high'] & people['many'], thermostat['very low'])
            
            ]

# Create a Control System for the Consequent variable and its Simulation
thermostat_ctrl = ctrl.ControlSystem(rulebase)
thermostat_ctrl_sim = ctrl.ControlSystemSimulation(thermostat_ctrl)

# Accept input
inp_temperature = float(input('Room temperature (15-35): '))
inp_humidity = float(input('Humidity (0-100): '))
inp_people = float(input('Number of people (0-30): '))

# Input the values into the simulation
thermostat_ctrl_sim.input['temperature'] = inp_temperature
thermostat_ctrl_sim.input['humidity'] = inp_humidity
thermostat_ctrl_sim.input['people'] = inp_people

# Perform computation
thermostat_ctrl_sim.compute()

# Display the defuzzified result (centroid method)
print('Thermostat temperature: {:.2f}'.format(thermostat_ctrl_sim.output['thermostat']))
thermostat.view(sim=thermostat_ctrl_sim)
input('Press any key to exit...')
