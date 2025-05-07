from ..modeling.custom_parser import parser



def test_cbrt(capsys):
    eqn_str = "c_t == (c_r - sqrt(c_q**3 + c_r**2))**(1/3)"
    parsed_eqn = parser.parse(eqn_str, evaluate=False)
    # transformed_eqn = parser.transformations[0](parsed_eqn)

    with capsys.disabled():
        print('')
        print("ACTUAL", parsed_eqn)

def test_arctan(capsys):
    eqn_str = "F_g == g * sin(arctan(G)) * W"
    parsed_eqn = parser.parse(eqn_str, evaluate=False)
    # transformed_eqn = parser.transformations[0](parsed_eqn)

    with capsys.disabled():
        print('')
        print("ACTUAL", parsed_eqn)