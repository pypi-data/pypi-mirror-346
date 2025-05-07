from reflex_nova.model_components.units import Units, u
from reflex_nova.variables import IndependentVar, DependentVar, BaseNamespace

angle = Units(
    si=u.radian,
    imp=u.degree,
    opts=[u.radian, u.degree]
)

dless = Units(
    si=u.dless,
    imp=u.dless,
    opts=[u.dless]
)

force = Units(
    si=u.N,
    imp=u.lbf,
    opts=[u.N, u.kN, u.lbf]
)


length = Units(
    si=u.mm,
    imp=u.inch,
    opts=[u.mm, u.cm, u.m, u.inch, u.ft]
)

torque = Units(
    si=u.N*u.m,
    imp=u.lbf*u.ft,
    opts=[u.N*u.m, u.lbf*u.ft]
)

big_pressure = Units(
    si=u.GPa,
    imp=u.psi,
    opts=[u.kPa, u.MPa, u.GPa, u.psi, u.ksi]
)

small_pressure = Units(
    si=u.MPa,
    imp=u.psi,
    opts=[u.kPa, u.MPa, u.psi, u.ksi]
)

        # # Constants
        # f_D = "D == (E*t**3)/(12*(1-nu**2))"

        # f_L_11 = [
        #     ("r_o == 0", "L_11 == 1/64"),
        #     ("r_o != 0", "L_11 == (1/64) * (1 + 4 * (r_o/a)**2 - 5 * (r_o/a)**4 - 4 * (r_o/a)**2 * (2 + (r_o/a)**2) * log(a/r_o))")
        # ]

        # f_L_14 = [
        #     ("r_o == 0", "L_14 == 1/16"),
        #     ("r_o != 0", "L_14 == (1/16) * (1 - (r_o/a)**4 - 4 * (r_o/a)**2 * log(a/r_o))")
        # ]

        # f_G_11 = [
        #     ("r == 0", "G_11 == 0"),
        #     ("r_o == 0", "G_11 == 1/64"),
        #     ("r <= r_o", "G_11 == (1/64) * (1 + 4 * (r_o/r)**2 - 5 * (r_o/r)**4 - 4 * (r_o/r)**2 * (2 + (r_o/r)**2) * log(r/r_o)) * (0)**0"),
        #     ("r > r_o", "G_11 == (1/64) * (1 + 4 * (r_o/r)**2 - 5 * (r_o/r)**4 - 4 * (r_o/r)**2 * (2 + (r_o/r)**2) * log(r/r_o)) * (r - r_o)**0")
        # ]

        # f_G_14 = [
        #     ("r == 0", "G_14 == 0"),
        #     ("r_o == 0", "G_14 == 1/16"),
        #     ("r <= r_o", "G_14 == (1/16) * (1 - (r_o/r)**4 - 4 * (r_o/r)**2 * log(r/r_o)) * (0)**0"),
        #     ("r > r_o", "G_14 == (1/16) * (1 - (r_o/r)**4 - 4 * (r_o/r)**2 * log(r/r_o)) * (r - r_o)**0")
        # ]

        # f_G_17 = [
        #     ("r == 0", "G_17 == 0"),
        #     ("r_o == 0", "G_17 == (3 + nu) / 16"),
        #     ("r <= r_o", "G_17 == (1/4) * (1 - ((1 - nu) / 4) * (1 - (r_o/r)**4) - (r_o/r)**2 * (1 + (1 + nu) * log(r/r_o))) * (0)**0"),
        #     ("r > r_o", "G_17 == (1/4) * (1 - ((1 - nu) / 4) * (1 - (r_o/r)**4) - (r_o/r)**2 * (1 + (1 + nu) * log(r/r_o))) * (r - r_o)**0")
        # ]

# # Boundary Conditions
# f_y_c = "y_c == ((-q*a**4)/(2*D)) * (L_14-2*L_11)"
# f_M_c = "M_c == q*a**2 * (1 + nu) * L_14"
# f_M_ra = "M_ra == q*a**2 * (1 + nu) * L_11"

# # Loading Terms
# f_LT_y = "LT_y == (-q*r**4/D) * G_11"
# f_LT_theta = "LT_theta == (-q*r**3/D) * G_14"
# f_LT_M = "LT_M == -q*r**2 * G_17"
# f_LT_Q = [
#     ("r <= r_o", "LT_Q == -q/24 * (r**2-r_o**2) * (0)**0"),
#     ("r > r_o", "LT_Q == -q/24 * (r**2-r_o**2) * (r-r_o)**0")
# ]

# f_y = "y == y_c + ((M_c * r**2) / (2*D*(1+nu))) + LT_y"

# f_theta = "theta == ((M_c * r) / (D*(1+nu))) + LT_theta"

# f_M_r = "M_r == M_c + LT_M"

# f_M_t = [
#     ("r == 0", "M_t == q*a**2 * (1 + nu) * L_14"),
#     ("r != 0", "M_t == ((theta*D * (1+nu**2)) / r) + nu * M_r")
# ]
    
# f_Q_r = "Q_r == LT_Q"


# 'a' : ScalarVar(sym='a', val=1000, unit='millimeter', unit_opts=['millimeter', 'meter']),
# 'E': ScalarVar(sym='E', val=200, unit='gigapascal', unit_opts=['pascal', 'gigapascal']),
# 'nu': ScalarVar(sym='nu', val=0.3, unit='dimensionless', unit_opts=['dimensionless']),
# 'q': ScalarVar(sym='q', val=100, unit='pascal', unit_opts=['pascal']),
# 'r': IndexedVar(sym='r', val=np.arange(-1000, 1001, 100), unit='millimeter', unit_opts=['millimeter', 'meter']),
# 'r_o': ScalarVar(sym='r_o', val=0, unit='millimeter', unit_opts=['millimeter', 'meter']),
# 't': ScalarVar(sym='t', val=100, unit='millimeter', unit_opts=['millimeter', 'meter']),

 
# # Constants
# 'D': ScalarVar(sym='D', eqn="D == (E*t**3)/(12*(1-nu**2))", unit='newton meter', unit_opts=['newton meter']),
# 'L_11': ScalarVar(sym='L_11', eqn=f_L_11, unit='dimensionless', unit_opts=['dimensionless']),
# 'L_14': ScalarVar(sym='L_14', eqn=f_L_14, unit='dimensionless', unit_opts=['dimensionless']),
# 'G_11': IndexedVar(sym='G_11', eqn=f_G_11, unit='dimensionless', unit_opts=['dimensionless']),
# 'G_14': IndexedVar(sym='G_14', eqn=f_G_14, unit='dimensionless', unit_opts=['dimensionless']),
# 'G_17': IndexedVar(sym='G_17', eqn=f_G_17, unit='dimensionless', unit_opts=['dimensionless']),

# # Boundary Conditions
# 'theta_a': ScalarVar(sym='theta_a', val=0, unit='radian', unit_opts=['radian', 'degree']),
# 'y_a': ScalarVar(sym='y_a', val=0, unit='meter', unit_opts=['meter', 'millimeter']),

# 'y_c': ScalarVar(sym='y_c', eqn=f_y_c, unit='meter', unit_opts=['meter', 'millimeter']),
# 'M_c': ScalarVar(sym='M_c', eqn=f_M_c, unit='newton', unit_opts=['newton']),
# 'M_ra': ScalarVar(sym='M_ra', eqn=f_M_ra, unit='newton', unit_opts=['newton']),

# # Loading Terms
# 'LT_y': IndexedVar(sym='LT_y', eqn=f_LT_y, unit='millimeter', unit_opts=['millimeter']),
# 'LT_theta': IndexedVar(sym='LT_theta', eqn=f_LT_theta, unit='radian', unit_opts=['radian']),
# 'LT_M': IndexedVar(sym='LT_M', eqn=f_LT_M, unit='newton', unit_opts=['newton']),
# 'LT_Q': IndexedVar(sym='LT_Q', eqn=f_LT_Q, unit='newton', unit_opts=['newton']),

        # # Results
        # 'y': IndexedVar(sym='y', eqn=f_y, unit='micrometer', unit_opts=['micrometer', 'meter', 'millimeter']),
        # 'theta': IndexedVar(sym='theta', eqn=f_theta, unit='radian', unit_opts=['radian', 'degree']),
        # 'M_r': IndexedVar(sym='M_r', eqn=f_M_r, unit='newton', unit_opts=['newton']),
        # 'M_t': IndexedVar(sym='M_t', eqn=f_M_t, unit='newton', unit_opts=['newton']),
        # 'Q_r': IndexedVar(sym='Q_r', eqn=f_Q_r, unit='newton', unit_opts=['newton']),

class PlateNamespace(BaseNamespace):
    # Variables
    a = IndependentVar(
        sym='a',
        name='Outside Radius',
        val=1000,
        unit=length,
        doc='The outside radius of the plate.',
    )
    E = IndependentVar(
        sym='E',
        name='Modulus of Elasticity',
        val=200,
        unit=big_pressure,
        doc='The modulus of elasticity of the material.',
    )
    nu = IndependentVar(
        sym='nu',
        name='Poisson\'s Ratio',
        val=0.3,
        unit=dless,
        doc='The Poisson\'s ratio of the material.',
    )
    q = IndependentVar(
        sym='q',
        name='Load per Unit Area',
        val=100,
        unit=small_pressure,
        doc='The load per unit area applied to the plate.',
    )
    r = IndependentVar(
        sym='r',
        name='Radial Location, Evaluation',
        val=0,
        unit=length,
        doc='The radial location of the quantity being evaluated.',
    )
    r_o = IndependentVar(
        sym='r_o',
        name='Radial Location, Load',
        val=0,
        unit=length,
        doc='The radial location of unit line loading or the start of a distributed load.',
    )
    t = IndependentVar(
        sym='t',
        name='Thickness',
        val=100,
        unit=length,
        doc='The thickness of the plate.',
    )

    # Boundary Condition Variables
    theta_a = IndependentVar(
        sym='theta_a',
        name='Radial Slope, Outer Radius',
        val=0,
        unit=angle,
        doc='The radial slope at the outer radius of the plate.',
    )
    y_a = IndependentVar(
        sym='y_a',
        name='Vertical Displacement, Outer Radius',
        val=0,
        unit=length,
        doc='The vertical displacement at the outer radius of the plate.',
    )

    # Boundary Condition Equations
    M_c = DependentVar(
        sym='M_c',
        eqn="{M_c} == {q}*{a}**2 * (1 + {nu}) * {L_14}",
        unit=force,
        doc='The moment at the center of the plate.',
    )
    M_ra = DependentVar(
        sym='M_ra',
        eqn="{M_ra} == {q}*{a}**2 * (1 + {nu}) * {L_11}",
        unit=force,
        doc='The moment at the radial location of the plate.',
    )
    y_c = DependentVar(
        sym='y_c',
        eqn="{y_c} == ((-{q}*{a}**4)/(2*{D})) * ({L_14}-2*{L_11})",
        unit=length,
        doc='The vertical displacement at the center of the plate.',
    )

    # Loading Term Equations
    LT_M = DependentVar(
        sym='LT_M',
        eqn="{LT_M} == -{q}*{r}**2 * {G_17}",
        unit=force,
        doc='The moment due to the applied load.',
    )
    LT_Q = DependentVar(
        sym='LT_Q',
        eqn=[
            ("{r} <= {r_o}", "{LT_Q} == -{q}/24 * ({r}**2-{r_o}**2) * (0)**0"),
            ("{r} > {r_o}", "{LT_Q} == -{q}/24 * ({r}**2-{r_o}**2) * ({r}-{r_o})**0"),
        ],
        unit=force,
        doc='The shear force due to the applied load.',
    )
    LT_theta = DependentVar(
        sym='LT_theta',
        eqn="{LT_theta} == (-{q}*{r}**3/{D}) * {G_14}",
        unit=u.radian,
        doc='The radial slope due to the applied load.',
    )
    LT_y = DependentVar(
        sym='LT_y',
        eqn="{LT_y} == (-{q}*{r}**4/{D}) * {G_11}",
        unit=length,
        doc='The vertical displacement due to the applied load.',
    )

    # Constants
    D = DependentVar(
        sym='D',
        eqn="{D} == ({E}*{t}**3)/(12*(1-{nu}**2))",
        unit=torque,
        doc='The flexural rigidity of the plate.',
    )
    L_11 = DependentVar(
        sym='L_11',
        eqn=[
            ("{r_o} == 0", "{L_11} == 1/64"),
            ("{r_o} != 0", "{L_11} == (1/64) * (1 + 4 * ({r_o}/{a})**2 - 5 * ({r_o}/{a})**4 - 4 * ({r_o}/{a})**2 * (2 + ({r_o}/{a})**2) * log({a}/{r_o}))"),
        ],
        unit=dless,
        doc='The constant L_11.',
    )
    L_14 = DependentVar(
        sym='L_14',
        eqn=[
            ("{r_o} == 0", "{L_14} == 1/16"),
            ("{r_o} != 0", "{L_14} == (1/16) * (1 - ({r_o}/{a})**4 - 4 * ({r_o}/{a})**2 * log({a}/{r_o}))"),
        ],
        unit=dless,
        doc='The constant L_14.',
    )
    G_11 = DependentVar(
        sym='G_11',
        eqn=[
            ("{r} == 0", "{G_11} == 0"),
            ("{r_o} == 0", "{G_11} == 1/64"),
            ("{r} <= {r_o}", "{G_11} == (1/64) * (1 + 4 * ({r_o}/{r})**2 - 5 * ({r_o}/{r})**4 - 4 * ({r_o}/{r})**2 * (2 + ({r_o}/{r})**2) * log({r}/{r_o})) * (0)**0"),
            ("{r} > {r_o}", "{G_11} == (1/64) * (1 + 4 * ({r_o}/{r})**2 - 5 * ({r_o}/{r})**4 - 4 * ({r_o}/{r})**2 * (2 + ({r_o}/{r})**2) * log({r}/{r_o})) * ({r} - {r_o})**0"),
        ],
        unit=dless,
        doc='The constant G_11.',
    )
    G_14 = DependentVar(
        sym='G_14',
        eqn=[
            ("{r} == 0", "{G_14} == 0"),
            ("{r_o} == 0", "{G_14} == 1/16"),
            ("{r} <= {r_o}", "{G_14} == (1/16) * (1 - ({r_o}/{r})**4 - 4 * ({r_o}/{r})**2 * log({r}/{r_o})) * (0)**0"),
            ("{r} > {r_o}", "{G_14} == (1/16) * (1 - ({r_o}/{r})**4 - 4 * ({r_o}/{r})**2 * log({r}/{r_o})) * ({r} - {r_o})**0"),
        ],
        unit=dless,
        doc='The constant G_14.',
    )
    G_17 = DependentVar(
        sym='G_17',
        eqn=[
            ("{r} == 0", "{G_17} == 0"),
            ("{r_o} == 0", "{G_17} == (3 + {nu}) / 16"),
            ("{r} <= {r_o}", "{G_17} == (1/4) * (1 - ((1 - {nu}) / 4) * (1 - ({r_o}/{r})**4) - ({r_o}/{r})**2 * (1 + (1 + {nu}) * log({r}/{r_o})) * (0)**0"),
            ("{r} > {r_o}", "{G_17} == (1/4) * (1 - ((1 - {nu}) / 4) * (1 - ({r_o}/{r})**4) - ({r_o}/{r})**2 * (1 + (1 + {nu}) * log({r}/{r_o})) * ({r} - {r_o})**0"),
        ],
        unit=dless,
        doc='The constant G_17.',
    )

    # Results
    M_r = DependentVar(
        sym='M_r',
        eqn="{M_r} == {M_c} + {LT_M}",
        unit=force,
        doc='The moment at the radial location of the plate.',
    )
    M_t = DependentVar(
        sym='M_t',
        eqn=[
            ("{r} == 0", "{M_t} == {q}*{a}**2 * (1 + {nu}) * {L_14}"),
            ("{r} != 0", "{M_t} == (({theta}*{D} * (1+{nu}**2)) / {r}) + {nu} * {M_r}"),
        ],
        unit=force,
        doc='The moment tangent to the radial location of the plate.',
    )
    Q_r = DependentVar(
        sym='Q_r',
        eqn="{LT_Q}",
        unit=force,
        doc='The shear force at the radial location of the plate.',
    )
    theta = DependentVar(
        sym='theta',
        eqn="((({M_c} * {r}) / ({D}*(1+{nu}))) + {LT_theta})",
        unit=angle,
        doc='The radial slope at the radial location of the plate.',
    )
    y = DependentVar(
        sym='y',
        eqn="{y_c} + (({M_c} * {r}**2) / (2*{D}*(1+{nu}))) + {LT_y}",
        unit=length,
        doc='The vertical displacement at the radial location of the plate.',
    )


