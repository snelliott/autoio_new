""" Physical constants and conversion factors
"""

from qcelemental import constants as qcc

# physical constants
NAVO = 6.0221409e+23
RC = 1.98720425864083  # gas constant in cal/(mol.K)
RC_kcal = 1.98720425864083e-3  # gas constant in kcal/(mol.K)
RC2 = 82.0573660809596  # gas constant in cm^3.atm/(mol.K)

# conversion factors
KCAL2CAL = qcc.conversion_factor('kcal/mol', 'cal/mol')
J2CAL = qcc.conversion_factor('J/mol', 'cal/mol')
KJ2CAL = qcc.conversion_factor('kJ/mol', 'cal/mol')
KEL2CAL = qcc.conversion_factor('kelvin', 'cal/mol')

