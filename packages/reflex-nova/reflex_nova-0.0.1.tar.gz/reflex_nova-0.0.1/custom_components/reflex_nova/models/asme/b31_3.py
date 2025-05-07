from reflex_nova.components.model.units import Units, u
from reflex_nova.components.model.fields import IndependentVar, DependentVar
from reflex_nova.components.model.nomenclature import BaseNomenclature

angle = Units(
    si=u.degree,
    imp=u.degree,
    opts=[u.radian, u.degree]
)

dless = Units(
    si=u.dless,
    imp=u.dless,
    opts=[u.dless]
)

length = Units(
    si=u.mm,
    imp=u.inch,
    opts=[u.inch, u.mm]
)

area = Units(
    si=u.mm**2,
    imp=u.inch**2,
    opts=[u.inch**2, u.mm**2]
)

pressure = Units(
    si=u.MPa,
    imp=u.psi,
    opts=[u.psi, u.Pa, u.kPa, u.MPa]
)


class B313Nomenclature(BaseNomenclature):
    # Variables
    c = IndependentVar(
        sym='c', name='Mechanical Allowances', value=0.0, unit=length,
        doc='The sum of the mechanical allowances (thread or groove depth) plus corrosion and erosion allowances. For threaded components, the nominal thread depth (dimension h of ASME B1.20.1, or equivalent) shall apply. For machined surfaces or grooves where the tolerance is not specified, the tolerance shall be assumed to be 0.5 mm (0.02 in.) in addition to the specified depth of the cut.')
    D = IndependentVar(
        sym='D', name='Outside Diameter', value=0.84, unit=length,
        doc='The outside diameter of pipe as listed in tables of standards or specifications or as measured')
    d = IndependentVar(
        sym='d', name='Inside Diameter', value=0.58275, unit=length,
        doc='The inside diameter of pipe. For pressure design calculation, the inside diameter of the pipe is the maximum value allowable under the purchase specification.')
    E = IndependentVar(
        sym='E', name='Quality Factor', value=0.8, unit=dless,
        doc='The quality factor from Table A-1A or Table A-1B')
    P = IndependentVar(
        sym='P', name='Design Pressure', value=90, unit=pressure,
        doc='The internal design gauge pressure.')
    S = IndependentVar(
        sym='S', name='Allowable Stress', value=20000, unit=pressure,
        doc='The stress value for material from Table A-1 or Table A-1M.')
    W = IndependentVar(
        sym='W',
        name='Weld Joint Strength Reduction Factor',
        value=1,
        unit=dless,
        doc='The weld joint strength reduction factor in accordance with para. 302.3.5(e)'
    )
    Y = IndependentVar(
        sym='Y',
        name='Y Coefficient',
        value=0.4,
        unit=dless,
        doc='The coefficient from Table 304.1.1, valid for t < D/6 and for materials shown. The value of Y may be interpolated for intermediate temperatures.'
    )
    T = DependentVar(
        sym='T',
        name='Pipe Wall Thickness',
        eqn="{T} == ({D} - {d}) / 2",
        unit=length,
        doc='The pipe wall thickness (measured or minimum in accordance with the purchase specification).'
    )
    t = DependentVar(
        sym='t',
        name='Pressure Design Thickness',
        eqn="{t} == ({P}*{D}) / (2*({S}*{E}*{W} + {P}*{Y}))",
        unit=length,
        doc='The pressure design thickness, as calculated in accordance with para. 304.1.2 for internal pressure or as determined in accordance with para. 304.1.3 for external pressure.'
    )
    t_m = DependentVar(
        sym='t_m',
        name='Minimum Required Thickness',
        eqn="{t_m} == {t} + {c}",
        unit=length,
        doc='The minimum required thickness, including mechanical, corrosion, and erosion allowances.'
    )
    P_max = DependentVar(
        sym='P_max',
        name='Pressure, Maximum',
        eqn="{P_max} == (2*({T}-{c})*{S}*{E}*{W}) / ({D} - 2*({T}-{c})*{Y})",
        unit=pressure,
        doc='The maximum allowable working pressure for the pipe.'
    )

# TODO: There is a problem with calculating P_max. The header and branch pressure can be valid while the reinforcement area is not.
class BranchConnectionNomenclature(BaseNomenclature):
    # Variables
    # A_4 = IndependentVar(
    #     sym='A_4',
    #     name='Reinforcement Added',
    #     value=1651,
    #     unit=area,
    #     doc='The area A_4 is the area resulting from the reinforcing ring or saddle.'
    # )
    # A_r = IndependentVar(
    #     sym='A_r',
    #     name='Reinforcement Area',
    #     value=0,
    #     unit=area,
    #     doc='The area of the reinforcing ring or saddle.'
    # )
    A_w = IndependentVar(
        sym='A_w',
        name='Weld Area',
        value=225,
        unit=area,
        doc='The area of the weld joint. The weld area is the area of the weld joint, which is the sum of the areas of the welds on both sides of the branch pipe.'
    )
    beta = IndependentVar(
        sym='beta',
        name='Branch Angle',
        value=90,
        unit=angle,
        doc='The angle between the branch pipe and the header pipe.'
    )
    c_b = IndependentVar(
        sym='c_b',
        name='Mechanical Allowance, Branch',
        value=0,
        unit=length,
        doc='The sum of the mechanical allowances (thread or groove depth) plus corrosion and erosion allowances for the branch pipe. For threaded components, the nominal thread depth (dimension h of ASME B1.20.1, or equivalent) shall apply. For machined surfaces or grooves where the tolerance is not specified, the tolerance shall be assumed to be 0.5 mm (0.02 in.) in addition to the specified depth of the cut.'
    )
    c_h = IndependentVar(
        sym='c_h',
        name='Mechanical Allowance, Header',
        value=0,
        unit=length,
        doc='The sum of the mechanical allowances (thread or groove depth) plus corrosion and erosion allowances for the header pipe. For threaded components, the nominal thread depth (dimension h of ASME B1.20.1, or equivalent) shall apply. For machined surfaces or grooves where the tolerance is not specified, the tolerance shall be assumed to be 0.5 mm (0.02 in.) in addition to the specified depth of the cut.'
    )
    D_b = IndependentVar(
        sym='D_b',
        name='Outside Diameter, Branch',
        value=219.1,
        unit=length,
        doc='The outside diameter of the branch pipe as listed in tables of standards or specifications or as measured.'
    )
    D_h = IndependentVar(
        sym='D_h',
        name='Outside Diameter, Header',
        value=323.8,
        unit=length,
        doc='The outside diameter of the header pipe as listed in tables of standards or specifications or as measured.'
    )
    D_r = IndependentVar(
        sym='D_r',
        name='Outside Diameter, Reinforcement',
        value=350,
        unit=length,
        doc='The outside diameter of the reinforcing ring.'
    )
    E_h = IndependentVar(
        sym='E_h',
        name='Quality Factor, Header',
        value=1,
        unit=dless,
        doc='The quality factor from Table A-1A or Table A-1B for the header pipe.'
    )
    E_b = IndependentVar(
        sym='E_b',
        name='Quality Factor, Branch',
        value=1,
        unit=dless,
        doc='The quality factor from Table A-1A or Table A-1B for the branch pipe.'
    )
    P = IndependentVar(
        sym='P',
        name='Pressure, Design',
        value=4,
        unit=pressure,
        doc='The internal design gauge pressure.'
    )
    S_b = IndependentVar(
        sym='S_b',
        name='Allowable Stress, Branch',
        value=55.2,
        unit=pressure,
        doc='The stress value for material from Table A-1 or Table A-1M for the branch pipe.'
    )
    S_h = IndependentVar(
        sym='S_h',
        name='Allowable Stress, Header',
        value=55.2,
        unit=pressure,
        doc='The stress value for material from Table A-1 or Table A-1M for the header pipe.'
    )
    S_r = IndependentVar(
        sym='S_r',
        name='Allowable Stress, Reinforcement',
        value=39.3,
        unit=pressure,
        doc='The stress value for material for the reinforcing ring.'
    )
    T_b = IndependentVar(
        sym='T_b',
        name='Pipe Thickness, Branch',
        value=11.1,
        unit=length,
        doc='The branch pipe thickness (measured or minimum in accordance with the purchase specification).'
    )
    T_h = IndependentVar(
        sym='T_h',
        name='Pipe Thickness, Header',
        value=15.3,
        unit=length,
        doc='The header pipe thickness (measured or minimum in accordance with the purchase specification).'
    )
    T_r = IndependentVar(
        sym='T_r',
        name='Reinforcement Thickness',
        value=15.3,
        unit=length,
        doc='The minimum thickness of reinforcing ring or saddle made from pipe (use nominal thickness if made from plate) = 0 if there is no reinforcing ring or saddle.'
    )
    W_b = IndependentVar(
        sym='W_b',
        name='Weld Joint Strength Reduction Factor, Branch',
        value=1,
        unit=dless,
        doc='The weld joint strength reduction factor in accordance with para. 302.3.5(e) for the branch pipe.'
    )
    W_h = IndependentVar(
        sym='W_h',
        name='Weld Joint Strength Reduction Factor, Header',
        value=1,
        unit=dless,
        doc='The weld joint strength reduction factor in accordance with para. 302.3.5(e) for the header pipe.'
    )
    Y_b = IndependentVar(
        sym='Y_b',
        name='Y Coefficient, Branch',
        value=0.4,
        unit=dless,
        doc='The coefficient from Table 304.1.1, valid for t < D/6 and for materials shown. The value of Y may be interpolated for intermediate temperatures for the branch pipe.'
    )
    Y_h = IndependentVar(
        sym='Y_h',
        name='Y Coefficient, Header',
        value=0.4,
        unit=dless,
        doc='The coefficient from Table 304.1.1, valid for t < D/6 and for materials shown. The value of Y may be interpolated for intermediate temperatures for the header pipe.'
    )
    # Equations
    A_1 = DependentVar(
        sym='A_1',
        name='Reinforcement Area Required',
        eqn="{A_1} == {t_h}*{d_1} * (2-sin({beta}))",
        unit=area,
        doc='The reinforcement area required for a branch connection under internal pressure.'
    )
    A_2 = DependentVar(
        sym='A_2',
        name='Reinforcement Area Run',
        eqn="{A_2} == (2*{d_2}-{d_1})*({T_h}-{t_h}-{c_h})",
        unit=area,
        doc='The reinforcement area for the run pipe.'
    )
    A_3 = DependentVar(
        sym='A_3',
        name='Reinforcement Area Branch',
        eqn="{A_3} == 2*{L_4}*({T_b}-{t_b}-{c_b})/sin({beta})",
        unit=area,
        doc='The reinforcement area for the branch pipe.'
    )
    A_4 = DependentVar(
        sym='A_4',
        name='Reinforcement Area',
        eqn="{A_4} == {A_r} + {A_w}",
        unit=area,
        doc='The area of the reinforcement added.'
    )
    A_r = DependentVar(
        sym='A_r',
        name='Reinforcement Area',
        eqn="{A_r} == {T_r}*({D_r}-{D_b})*({S_r}/{S})",
        unit=area,
        doc='The area of the reinforcing ring.'
    )
    c = DependentVar(
        sym='c',
        name='Corrosion Allowance',
        eqn="{c} == max({c_b}, {c_h})",
        unit=length,
        doc='The corrosion allowance.'
    )
    d_1 = DependentVar(
        sym='d_1',
        name='Effective Length Removed',
        eqn="{d_1} == ({D_b} - 2*({T_b}-{c_b})) / sin({beta})",
        unit=length,
        doc='The effective length removed from pipe at branch. For branch intersections where the branch opening is a projection of the branch pipe inside diameter (e.g., pipe-to-pipe fabricated branch).'
    )
    d_2 = DependentVar(
        sym='d_2',
        name='Reinforcement Zone Radius',
        eqn="{d_2} == max({d_1}, ({T_b}-{c_b})+({T_h}-{c_h})+{d_1}/2)",
        unit=length,
        doc='The half width or radius of the reinforcement zone.'
    )
    d_h = DependentVar(
        sym='d_h',
        name='Inside Diameter, Header',
        eqn="{d_h} == {D_h} - 2*{T_h}",
        unit=length,
        doc='The inside diameter of the header pipe. For pressure design calculation, the inside diameter of the pipe is the maximum value allowable under the purchase specification.'
    )
    d_b = DependentVar(
        sym='d_b',
        name='Inside Diameter, Branch',
        eqn="{d_b} == {D_b} - 2*{T_b}",
        unit=length,
        doc='The inside diameter of the branch pipe. For pressure design calculation, the inside diameter of the pipe is the maximum value allowable under the purchase specification.'
    )
    E = DependentVar(
        sym='E',
        name='Quality Factor',
        eqn="{E} == min({E_b}, {E_h})",
        unit=dless,
        doc='The quality factor from Table A-1A or Table A-1B for the branch and header pipes.'
    )
    L_4 = DependentVar(
        sym='L_4',
        name='Reinforcement Zone Height',
        eqn="{L_4} == min(2.5*({T_h}-{c_h}), 2.5*({T_b}-{c_b}) + {T_r})",
        unit=length,
        doc='The height of reinforcement zone outside of the run pipe.'
    )
    P_max = DependentVar(
        sym='P_max',
        name='Pressure, Maximum',
        eqn="{P_max} == 2*{E}*{S}*{W}*({A_4}*sin({beta}) + 2*{L_4}*{T_b} - 2*{L_4}*{c} - {T_h}*{d_1}*sin({beta}) + 2*{T_h}*{d_2}*sin({beta}) + {c}*{d_1}*sin({beta}) - 2*{c}*{d_2}*sin({beta}))/(-2*{A_4}*{Y}*sin({beta}) + 2*{D_b}*{L_4} - {D_h}*{d_1}*sin({beta})**2 + {D_h}*{d_1}*sin({beta}) + 2*{D_h}*{d_2}*sin({beta}) - 4*{L_4}*{T_b}*{Y} + 4*{L_4}*{Y}*{c} + 2*{T_h}*{Y}*{d_1}*sin({beta}) - 4*{T_h}*{Y}*{d_2}*sin({beta}) - 2*{Y}*{c}*{d_1}*sin({beta}) + 4*{Y}*{c}*{d_2}*sin({beta}))",
        unit=pressure,
        doc='The maximum pressure in the system.'
    )
    P_max_b = DependentVar(
        sym='P_max_b',
        name='Pressure, Maximum, Branch',
        eqn="{P_max_b} == (2*({T_b}-{c_b})*{S_b}*{E_b}*{W_b}) / ({D_b} - 2*({T_b}-{c_b})*{Y_b})",
        unit=pressure,
        doc='The maximum pressure in the branch pipe.'
    )
    P_max_h = DependentVar(
        sym='P_max_h',
        name='Pressure, Maximum, Header',
        eqn="{P_max_h} == (2*({T_h}-{c_h})*{S_h}*{E_h}*{W_h}) / ({D_h} - 2*({T_h}-{c_h})*{Y_h})",
        unit=pressure,
        doc='The maximum pressure in the header pipe.'
    )
    S = DependentVar(
        sym='S',
        name='Allowable Stress',
        eqn="{S} == min({S_b}, {S_h})",
        unit=pressure,
        doc='The minimum allowable stress.'
    )
    t_b = DependentVar(
        sym='t_b',
        name='Pressure Design Thickness, Branch',
        eqn="{t_b} == ({P}*{D_b}) / (2*({S_b}*{E_b}*{W_b} + {P}*{Y_b}))",
        unit=length,
        doc='The pressure design thickness of the branch pipe, according to the appropriate wall thickness equation or procedure.'
    )
    t_h = DependentVar(
        sym='t_h',
        name='Pressure Design Thickness, Header',
        eqn="{t_h} == ({P}*{D_h}) / (2*({S_h}*{E_h}*{W_h} + {P}*{Y_h}))",
        unit=length,
        doc='The pressure design thickness of the header pipe, according to the appropriate wall thickness equation or procedure.'
    )
    t_m_b = DependentVar(
        sym='t_m_b',
        name='Minimum Required Thickness, Branch',
        eqn="{t_m_b} == {t_b} + {c_b}",
        unit=length,
        doc='The minimum required thickness of the branch pipe, including mechanical, corrosion, and erosion allowances.'
    )
    t_m_h = DependentVar(
        sym='t_m_h',
        name='Minimum Required Thickness, Header',
        eqn="{t_m_h} == {t_h} + {c_h}",
        unit=length,
        doc='The minimum required thickness of the header pipe, including mechanical, corrosion, and erosion allowances.'
    )
    W = DependentVar(
        sym='W',
        name='Weld Joint Strength Reduction Factor',
        eqn="{W} == min({W_b}, {W_h})",
        unit=dless,
        doc='The weld joint strength reduction factor in accordance with para. 302.3.5(e) for the branch and header pipes.'
    )
    Y = DependentVar(
        sym='Y',
        name='Y Coefficient',
        eqn="{Y} == min({Y_b}, {Y_h})",
        unit=dless,
        doc='The minimum Y coefficient from Table 304.1.1 for the branch and header pipes.'
    )


    