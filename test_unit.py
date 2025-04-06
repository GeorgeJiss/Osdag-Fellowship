import pytest
from bolted_lap_joint_design import design_lap_joint

def test_minimum_bolts():
    """Test that at least two bolts are used for any valid load and plate thickness."""
    loads = range(0, 101, 10)  # Testing loads from 0 to 100 kN in increments of 10
    thicknesses = [6, 8, 10, 12, 16, 20, 24]  # Valid thickness values
    plate_width = 150  # Assumed width for testing

    for P in loads:
        for t1 in thicknesses:
            for t2 in thicknesses:
                try:
                    design = design_lap_joint(P, plate_width, t1, t2)
                    assert design["number_of_bolts"] >= 2, f"Failed for P={P}, t1={t1}, t2={t2}"
                except ValueError:
                    pass  # If no design is possible, it should not break the test
