from reflex_nova.components.model.units import Units, u
from reflex_nova.components.model.fields import IndependentVar, DependentVar
from reflex_nova.components.model.nomenclature import BaseNomenclature

mass = Units(
    si=u.kilogram,
    imp=u.pound,
    opts=[u.kilogram, u.pound],
)

mass_density = Units(
    si=u.kilogram/u.meter,
    imp=u.pound/u.foot,
    opts=[u.kilogram/u.meter],
)

mass_flow = Units(
    si=u.kilogram/u.second,
    imp=u.pound/u.second,
    opts=[u.kilogram/u.second],
)

lenght_time_2 = Units(
    si=u.meter**2/u.second**2,
    imp=u.foot**2/u.second**2,
    opts=[u.meter**2/u.second**2],
)

lenght_time_3 = Units(
    si=u.meter**3/u.second**3,
    imp=u.foot**3/u.second**3,
    opts=[u.meter**3/u.second**3],
)

length = Units(
    si=u.meter,
    imp=u.foot,
    opts=[u.meter, u.foot],
)

density = Units(
    si=u.kilogram/u.meter**3,
    imp=u.pound/u.foot**3,
    opts=[u.kilogram/u.meter**3],
)

power = Units(
    si=u.watt,
    imp=u.horsepower,
    opts=[u.watt],
)

work = Units(
    si=u.joule,
    imp=u.foot_pound,
    opts=[u.joule],
)

acceleration = Units(
    si=u.meter/u.second**2,
    imp=u.foot/u.second**2,
    opts=[u.meter/u.second**2],
)

velocity = Units(
    si=u.km/u.hour,
    imp=u.foot/u.second,
    opts=[u.km/u.hour],
)

area = Units(
    si=u.meter**2,
    imp=u.foot**2,
    opts=[u.meter**2],
)

percent = Units(
    si=u.percent,
    imp=u.percent,
    opts=[u.percent],
)

force = Units(
    si=u.newton,
    imp=u.pound_force,
    opts=[u.newton],
)

dless = Units(
    si=u.dless,
    imp=u.dless,
    opts=[u.dless],
)

class PowerSpeed(BaseNomenclature):
    A = IndependentVar(
        sym="A",
        name="Frontal Area",
        value=0.509,
        unit=area,
        doc="Frontal area of the cyclist and bike",
    )
    C_d = IndependentVar(
        sym="C_d",
        name="Coefficient of Drag",
        value=0.63,
        unit=dless,
        doc="Coefficient of drag for the cyclist and bike",
    )
    C_rr = IndependentVar(
        sym="C_rr",
        name="Coefficient of Rolling Resistance",
        value=0.005,
        unit=dless,
        doc="Coefficient of rolling resistance for the bike and rider",
    )
    D = IndependentVar(
        sym="D",
        name="Distance",
        value=1000,
        unit=length,
        doc="Distance travelled by the cyclist and bike",
    )
    eta_dt = IndependentVar(
        sym="eta_dt",
        name="Efficiency, Drivetrain",
        value=0.95,
        unit=dless,
        doc="Efficiency of the drivetrain",
    )
    G = IndependentVar(
        sym="G",
        name="Grade",
        value=1,
        unit=percent,
        doc="The percent grade of a hill",
    )
    g = IndependentVar(
        sym="g",
        name="Acceleration",
        value=9.81,
        unit=acceleration,
        doc="Acceleration due to gravity",
    )
    rho_air = IndependentVar(
        sym="rho_air",
        name="Density of Air",
        value=1.225,
        unit=density,
        doc="Density of air at sea level and 15 degrees Celsius",
    )
    V_gs = IndependentVar(
        sym="V_gs",
        name="Velocity, Ground Speed",
        value=35.41,
        unit=velocity,
        doc="The ground speed of the cyclist and bike",
    )
    V_hw = IndependentVar(
        sym="V_hw",
        name="Velocity, Head Wind",
        value=0,
        unit=velocity,
        doc="The head wind speed acting on the cyclist and bike",
    )
    W_b = IndependentVar(
        sym="W_b",
        name="Weight of Bike",
        value=7.711,
        unit=mass,
        doc="Weight of the bike",
    )
    W_r = IndependentVar(
        sym="W_r",
        name="Weight of Rider",
        value=74.843,
        unit=mass,
        doc="Weight of the cyclist",
    )
    F_d = DependentVar(
        sym="F_d",
        name="Force, Drag",
        eqn="{F_d} == 0.5 * {C_d} * {A} * {rho_air} * {V_as}**2",
        unit=force,
        doc="The force of drag acting on the cyclist and bike",
    )
    F_g = DependentVar(
        sym="F_g",
        name="Force, Gravity",
        eqn="{F_g} == {g} * sin(arctan({G})) * {W}",
        unit=force,
        doc="The force of gravity acting on the cyclist and bike",
    )
    F_r = DependentVar(
        sym="F_r",
        name="Force, Rolling Resistance",
        eqn="{F_r} == {g} * cos(arctan({G})) * {W} * {C_rr}",
        unit=force,
        doc="The force of rolling resistance acting on the cyclist and bike",
    )
    F_t = DependentVar(
        sym="F_t",
        name="Force, Total",
        eqn="{F_t} == {F_d} + {F_g} + {F_r}",
        unit=force,
        doc="The total force acting on the cyclist and bike",
    )
    P_d = DependentVar(
        sym="P_d",
        name="Power, Drag",
        eqn="{P_d} == {F_d} * {V_gs}",
        unit=power,
        doc="The power required to overcome the drag force acting on the cyclist and bike",
    )
    P_g = DependentVar(
        sym="P_g",
        name="Power, Gravity",
        eqn="{P_g} == {F_g} * {V_gs}",
        unit=power,
        doc="The power required to overcome the force of gravity acting on the cyclist and bike",
    )
    P_legs = DependentVar(
        sym="P_legs",
        name="Power, Legs",
        eqn="{P_legs} == ({F_t} * {V_gs}) / ({eta_dt})",
        unit=power,
        doc="The power required to overcome the total force acting on the cyclist and bike",
    )
    P_r = DependentVar(
        sym="P_r",
        name="Power, Rolling Resistance",
        eqn="{P_r} == {F_r} * {V_gs}",
        unit=power,
        doc="The power required to overcome the force of rolling resistance acting on the cyclist and bike",
    )
    P_total = DependentVar(
        sym="P_total",
        name="Power, Total",
        eqn="{P_total} == {F_t} * {V_gs}",
        unit=power,
        doc="The power required to overcome the total force acting on the cyclist and bike",
    )
    V_as = DependentVar(
        sym="V_as",
        name="Velocity, Aerodynamic Speed",
        eqn="{V_as} == {V_gs} + {V_hw}",
        unit=velocity,
        doc="The aerodynamic speed of the cyclist and bike",
    )
    W = DependentVar(
        sym="W",
        name="Weight of System",
        eqn="{W} == {W_r} + {W_b}",
        unit=mass,
        doc="The combined weight of the cyclist and bike",
    )
    W_t = DependentVar(
        sym="W_t",
        name="Total Work",
        eqn="{W_t} == {F_t} * {D}",
        unit=work,
        doc="The total work done by the cyclist and bike",
    )
    a = DependentVar(
        sym="a",
        name="a",
        eqn="{a} == 0.5 * {C_d} * {A} * {rho_air}",
        unit=mass_density,
        doc="a",
    )
    b = DependentVar(
        sym="b",
        name="b",
        eqn="{b} == {V_hw} * {C_d} * {A} * {rho_air}",
        unit=mass_flow,
        doc="b",
    )
    c = DependentVar(
        sym="c",
        name="c",
        eqn="{c} == {F_g} + {F_r} + (0.5 * {C_d} * {A} * {rho_air} * {V_hw}**2)",
        unit=force,
        doc="c",
    )
    d = DependentVar(
        sym="d",
        name="d",
        eqn="{d} == -{eta_dt} * {P_legs}",
        unit=power,
        doc="d",
    )
    c_q = DependentVar(
        sym="c_q",
        name="c_q",
        eqn="{c_q} == (3*{a}*{c} - {b}**2)/(9*{a}**2)",
        unit=lenght_time_2,
        doc="c_q",
    )
    c_r = DependentVar(
        sym="c_r",
        name="c_r",
        eqn="{c_r} == (9*{a}*{b}*{c} - 27*{a}**2*{d} - 2*{b}**3)/(54*{a}**3)",
        unit=lenght_time_3,
        doc="c_r",
    )
    c_s = DependentVar(
        sym="c_s",
        name="c_s",
        eqn="{c_s} == cbrt({c_r} + sqrt({c_q}**3 + {c_r}**2))",
        unit=velocity,
        doc="c_s",
    )
    c_t = DependentVar(
        sym="c_t",
        name="c_t",
        eqn="{c_t} == cbrt({c_r} - sqrt({c_q}**3 + {c_r}**2))",
        unit=velocity,
        doc="c_t",
    )
    V_out = DependentVar(
        sym="V_out",
        name="Velocity, Output",
        eqn="{V_out} == {c_s} + {c_t} - {b}/(3*{a})",
        unit=velocity,
        doc="The output velocity",
    )





