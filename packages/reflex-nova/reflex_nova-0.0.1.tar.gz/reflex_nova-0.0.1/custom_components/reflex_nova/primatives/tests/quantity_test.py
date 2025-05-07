from reflex_nova.primatives import Qty, ureg, length, angle, dimensionless, force
import numpy as np
import pytest


def test_less_than_float():
    q1 = Qty(value=5, unit=length)
    expected = True
    actual = q1 < 10.00
    assert expected == actual

def test_less_than_qty_same_unit():
    q1 = Qty(value=5, unit=length)
    q2 = Qty(value=10, unit=length)
    expected = True
    actual = q1 < q2
    assert expected == actual

def test_equal_same_unit():
    q1 = Qty(value=5, unit=length)
    q2 = Qty(value=5, unit=length)
    expected = True
    actual = q1 == q2
    assert expected == actual

def test_equal_different_unit():
    q1 = Qty(value=5, unit=length)
    q2 = Qty(value=5, unit=length.update_selected('cm'))
    expected = False
    actual = q1 == q2
    assert expected == actual

def test_as_pint():
    q = Qty(value=5, unit=length)
    expected = ureg.Quantity(5, 'm')
    actual = q.qty_as_pint()
    assert expected == actual

def test_add_same_units():
    q1 = Qty(value=5, unit=length)
    q2 = Qty(value=3, unit=length)
    result = q1 + q2
    assert result.value == 8
    assert result.unit == 'm'

def test_add_different_units(capsys):
    u1 = length
    u2 = length.update_selected('cm')

    q1 = Qty(value=5, unit=u1)
    q2 = Qty(value=300, unit=u2)
    result = q1 + q2
    
    expected = ureg.Quantity(8, 'm')
    actual = result.convert_to('m')

    assert expected == actual.qty_as_pint()
    # result = result.to_unit('m')
    # assert result.value == 8
    # assert result.unit == 'm'


def test_multiply_same_units(capsys):
    q1 = Qty(value=5, unit=length)
    q2 = Qty(value=3, unit=length)
    expected = Qty(value=15, unit=length * length)
    actual = q1 * q2

    assert expected == actual


def test_multiply_different_units(capsys):
    q1 = Qty(value=5, unit=length)
    q2 = Qty(value=5, unit=force)
    expected = Qty(value=25, unit=length * force)
    actual = q1 * q2

    assert expected == actual


def test_cosine_radian(capsys):
    q = Qty(value=np.pi/4, unit=angle)

    expected = Qty(value=np.sqrt(2)/2, unit=dimensionless)
    actual = np.cos(q)

    assert expected == actual

def test_cosine_degree(capsys):
    q = Qty(value=45, unit=angle.update_selected('deg'))

    expected = Qty(value=np.sqrt(2)/2, unit=dimensionless)
    actual = np.cos(q)

    assert expected == actual

def test_sine_radian(capsys):
    q = Qty(value=np.pi/4, unit=angle)

    expected = Qty(value=np.sqrt(2)/2, unit=dimensionless)
    actual = np.sin(q)

    assert expected == actual

def test_sine_degree(capsys):
    q = Qty(value=45, unit=angle.update_selected('deg'))

    expected = Qty(value=np.sqrt(2)/2, unit=dimensionless)
    actual = np.sin(q)

    assert expected == actual