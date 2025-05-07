from reflex_nova.primatives.unit import Unit, _in_same_system, ureg
import pytest

def test_unit_repr():
    unit = Unit(selected="N", options=["N", "kN", "lbf"])
    expected = "Unit(selected='N', options=['N', 'kN', 'lbf'])"
    actual = repr(unit)
    assert expected == actual

def test_unit_str():
    unit = Unit(selected="N", options=["N", "kN", "lbf"])
    expected = "N"
    actual = str(unit)
    assert expected == actual

def test_unit_equal():
    unit_1 = Unit(selected="N", options=["N", "kN", "lbf"])
    unit_2 = Unit(selected="N", options=["N", "kN", "lbf"])
    expected = True
    actual = unit_1 == unit_2
    assert expected == actual

def test_unit_not_equal():
    unit_1 = Unit(selected="N", options=["N", "kN", "lbf"])
    unit_2 = Unit(selected="kN", options=["N", "kN", "lbf"])
    expected = False
    actual = unit_1 == unit_2
    assert expected == actual

def test_unit_update_selected():
    unit = Unit(selected="N", options=["N", "kN", "lbf"])
    new_unit = "kN"
    expected = Unit(selected="kN", options=["N", "kN", "lbf"])
    actual = unit.update_selected(new_unit)
    assert expected == actual

def test_unit_update_selected_invalid():
    unit = Unit(selected="N", options=["N", "kN", "lbf"])
    new_unit = "lb"
    
    with pytest.raises(ValueError) as exc_info:
        unit.update_selected(new_unit)

    assert str(exc_info.value) == "'lb' is not a valid option. Valid options: ['N', 'kN', 'lbf']"

def test_unit_multiply_same_dimension():
    unit_1 = Unit(selected="N", options=["N", "kN", "lbf"])
    unit_2 = Unit(selected="N", options=["N", "kN", "lbf"])
    expected = Unit(selected="N²", options=["N²", "kN²", "lbf²"])
    actual = unit_1 * unit_2
    assert expected == actual

def test_unit_multiply_different_dimension(capsys):
    unit_1 = Unit(selected="N", options=["N", "kN", "lbf"])
    unit_2 = Unit(selected="m", options=["m", "cm", "mm"])
    expected = Unit(selected="m·N", options=['cm·N', 'cm·kN', 'cm·lbf', 'kN·m', 'kN·mm', 'lbf·m', 'lbf·mm', 'mm·N', 'm·N'])
    actual = unit_1 * unit_2
    assert expected == actual

def test_dimensionality(capsys):
    with capsys.disabled():

        unit_1 = ureg.parse_units("dless")
        unit_2 = ureg.parse_units("m")
        # expected = True
        actual = unit_1 * unit_2
        # assert expected == actual

    with capsys.disabled():
        print("Unit 1:", unit_1.dimensionality)
        print("Unit 2:", unit_2.dimensionality)
        print(unit_1.dimensionality == ureg.parse_units("dless").dimensionality)
        print("Actual:", actual)
#         print(type(unit_1.dimensionality))
        # print("Actual:", actual.dimensionality)
#         print("Actual:", actual.options)

# def test_in_same_system_same(capsys):
#     unit_1 = ureg.parse_units("N")
#     # unit_2 = "m"
#     # expected = True
#     # actual = _in_same_system(unit_1, unit_2)
#     # assert expected == actual
#     with capsys.disabled():
#         print(unit_1.)
#         # print("Actual:", actual)

#         # print(set(dir(ureg.sys.mks)))









