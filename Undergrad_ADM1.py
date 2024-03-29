
#ADM1 Model 
#Madison Kratezr

#WaterTAP package used - adapted from the ADM1 case study and BSM1 tutorial available at
#https://github.com/watertap-org/watertap/blob/main/watertap/examples/flowsheets/case_studies/anaerobic_digester/ADM1_flowsheet.py
### from "Alejandro Garciadiego, Adam Atia"
#and 
#https://github.com/watertap-org/watertap/blob/main/tutorials/BSM2.ipynb



#################################################################################

import pyomo.environ as pyo
from pyomo.environ import (
    units,
)
from idaes.core import FlowsheetBlock
from idaes.core.solvers import get_solver
import idaes.logger as idaeslog
from watertap.unit_models.anaerobic_digester import AD
from watertap.property_models.anaerobic_digestion.adm1_properties import (
    ADM1ParameterBlock,
)
from watertap.property_models.anaerobic_digestion.adm1_properties_vapor import (
    ADM1_vaporParameterBlock,
)
from watertap.property_models.anaerobic_digestion.adm1_reactions import (
    ADM1ReactionParameterBlock,
)

#Create a product block so we can access our treated water characteristics

from idaes.models.unit_models import (
    Product
)

print('Made it to part 1')

#Set up model

m = pyo.ConcreteModel()
m.fs = FlowsheetBlock(dynamic=False)

#Set up parameters

m.fs.props_ADM1 = ADM1ParameterBlock()
m.fs.props_vap = ADM1_vaporParameterBlock()
m.fs.ADM1_rxn_props = ADM1ReactionParameterBlock(property_package=m.fs.props_ADM1)


#Define a model - we're calling this R1, and we're only putting in the anaerobic digester, we're telling it to use the ADM1 properties block
m.fs.R1 = AD(
    liquid_property_package=m.fs.props_ADM1,
    vapor_property_package=m.fs.props_vap,
    reaction_package=m.fs.ADM1_rxn_props,
    has_heat_transfer=True,
    has_pressure_change=False,
)



# Anaerobic digester
# Feed conditions, Don't change the 0s, they're boundary conditions. To change feed conditions change number in the .fix(NUBMER*UNITS)
m.fs.R1.inlet.flow_vol.fix(170 * pyo.units.m**3 / pyo.units.day)
m.fs.R1.inlet.temperature.fix(308.15 * pyo.units.K)
m.fs.R1.inlet.pressure.fix(1 * pyo.units.atm)
m.fs.R1.inlet.conc_mass_comp[0, "S_su"].fix(10 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "S_aa"].fix(1 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "S_fa"].fix(1 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "S_va"].fix(1 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "S_bu"].fix(1 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "S_pro"].fix(1 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "S_ac"].fix(1 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "S_h2"].fix(1e-5 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "S_ch4"].fix(1e-2 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "S_IC"].fix(
    40 * units.mmol / units.liter * 12 * units.mg / units.mmol
)
m.fs.R1.inlet.conc_mass_comp[0, "S_IN"].fix(
    10 * units.mmol / units.liter * 14 * units.mg / units.mmol
)
m.fs.R1.inlet.conc_mass_comp[0, "S_I"].fix(20 * pyo.units.mg / pyo.units.liter)

m.fs.R1.inlet.conc_mass_comp[0, "X_c"].fix(2000 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "X_ch"].fix(5000 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "X_pr"].fix(20000 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "X_li"].fix(5000 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "X_su"].fix(0.0 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "X_aa"].fix(10 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "X_fa"].fix(10 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "X_c4"].fix(10 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "X_pro"].fix(10 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "X_ac"].fix(10 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "X_h2"].fix(10 * pyo.units.mg / pyo.units.liter)
m.fs.R1.inlet.conc_mass_comp[0, "X_I"].fix(25000 * pyo.units.mg / pyo.units.liter)

m.fs.R1.inlet.cations[0].fix(40 * pyo.units.mmol / pyo.units.liter)
m.fs.R1.inlet.anions[0].fix(20 * pyo.units.mmol / pyo.units.liter)

m.fs.R1.volume_liquid.fix(3400 * pyo.units.m**3)
m.fs.R1.volume_vapor.fix(300 * pyo.units.m**3)

m.fs.R1.liquid_outlet.temperature.fix(308.15 * pyo.units.K)

solver = get_solver()

results = solver.solve(m, tee=True)
m.fs.Treated = Product(property_package=m.fs.props_ADM1)

#okay it's going to print freeze report a solid 20+ times, wait it out - I really can't figure out why that's happening, but it happens with every
#iteration of the solver, it will stop and converge, just give it a minute or two 
pyo.assert_optimal_termination(results)
print('did it ')

#Effluent Quality
m.fs.Treated.report()

print('ADM1 Conditions')
m.fs.R1.report()



