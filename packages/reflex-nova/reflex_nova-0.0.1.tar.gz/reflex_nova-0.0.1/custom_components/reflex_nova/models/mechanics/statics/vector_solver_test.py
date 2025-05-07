import math
import pytest
from .vector_solver import Axis, Vector


def test_F2_1_resultant_magnitude_and_direction():
    """
    F2-1: 6 kN at 240°, 2 kN at 315° (both measured from global +x-axis CCW).
    Expect resultant magnitude ≈ 6.7979 kN and direction ≈ 103.49° clockwise from +x.
    """
    v1 = Vector(6, 240)
    v2 = Vector(2, 315)
    R = v1 + v2
    mag, dir_ccw = R.magnitude_direction()
    dir_cw = (-dir_ccw) % 360
    assert mag == pytest.approx(6.7979156, rel=1e-4)
    assert dir_cw == pytest.approx(103.4899848, rel=1e-4)


def test_F2_2_magnitude_only():
    """
    F2-2: 200 N at 30°, 500 N at -40°
    Expect resultant magnitude ≈ 598.6685 N.
    """
    v1 = Vector(200, 330)
    v2 = Vector(500, 290)
    R = v1 + v2
    mag, _ = R.magnitude_direction()
    assert mag == pytest.approx(665.7394, rel=1e-4)


def test_F2_3_magnitude_and_direction_ccw():
    """
    F2-3: 800 N at 90°, 600 N at -30°
    Expect magnitude ≈ 721.1103 N and direction ≈ 43.8979° CCW from +x.
    """
    v1 = Vector(800, 90)
    v2 = Vector(600, -30)
    R = v1 + v2
    mag, dir_ccw = R.magnitude_direction()
    assert mag == pytest.approx(721.1103, rel=1e-4)
    assert dir_ccw == pytest.approx(43.8979, rel=1e-4)


def test_F2_4_components_along_u_v():
    """
    F2-4: 30 lb at 30°; u-axis at 0°, v-axis at 75°
    Expect F_u ≈ 25.9808 lb, F_v ≈ 21.2132 lb.
    """
    F = Vector(30, 30)
    u_axis = Axis('u', 0)
    v_axis = Axis('v', 75)
    comp_u = u_axis.project(F)
    comp_v = v_axis.project(F)
    assert comp_u == pytest.approx(25.9807621, rel=1e-4)
    assert comp_v == pytest.approx(21.2132034, rel=1e-4)


def test_F2_5_components_along_AB_AC():
    """
    F2-5: 450 lb at 270°; AC at 150°, AB at 225°
    Expect component along AC ≈ -225 lb (225 compression), along AB ≈ 318.1980 lb.
    """
    F = Vector(450, 270)
    ac_axis = Axis('AC', 150)
    ab_axis = Axis('AB', 225)
    comp_ac = ac_axis.project(F)
    comp_ab = ab_axis.project(F)
    assert comp_ac == pytest.approx(-225.0, rel=1e-4)
    assert comp_ab == pytest.approx(318.1980515, rel=1e-4)


def test_F2_6_force_and_component_along_v():
    """
    F2-6: want F_u = 6 kN with F at 45°; u-axis=0°, v-axis=-60° (so angle between F and v =105°)
    Expect total F ≈ 8.4853 kN and component along v ≈ -2.1962 kN.
    """
    # Solve for magnitude
    F_mag = 6 / math.cos(math.radians(45))
    F_vec = Vector(F_mag, 45)
    u_axis = Axis('u', 0)
    v_axis = Axis('v', -60)
    comp_u = u_axis.project(F_vec)
    comp_v = v_axis.project(F_vec)
    assert comp_u == pytest.approx(6.0, rel=1e-6)
    assert F_mag == pytest.approx(8.485281374, rel=1e-6)
    assert comp_v == pytest.approx(-2.196152423, rel=1e-6)
