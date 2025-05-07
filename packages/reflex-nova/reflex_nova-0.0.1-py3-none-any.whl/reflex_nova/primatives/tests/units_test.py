from reflex_nova.primatives.units import force


# def test_angle():
#     """Test the angle unit factory."""
#     assert angle.selected == "deg"
#     assert angle.options == ["deg", "rad"]
    
def test_force():
    """Test the force unit factory."""
    assert force.selected == "N"
    assert force.options == ["N", "kN", "lbf"]