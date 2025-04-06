import pytest
from bolted_lap_joint_design import design_lap_joint, calculate_bolt_strength

def test_minimum_bolts():
    """Test that at least two bolts are used for any valid load and plate thickness."""
    loads = range(0, 101, 20)  # Testing loads from 0 to 100 kN in increments of 20
    thicknesses = [6, 10, 16, 24]  # Sample thickness values
    plate_width = 150  # Assumed width for testing
    
    for P in loads:
        for t1 in thicknesses:
            for t2 in thicknesses:
                try:
                    design = design_lap_joint(P, plate_width, t1, t2)
                    assert design["number_of_bolts"] >= 2, f"Failed for P={P}, t1={t1}, t2={t2}"
                except ValueError:
                    pass  # If no design is possible, it should not break the test

def test_zero_load():
    """Test that the function handles zero load appropriately."""
    try:
        design = design_lap_joint(0, 150, 10, 10)
        # Check if design has reasonable values for zero load
        assert design["number_of_bolts"] >= 2
    except ValueError as e:
        pytest.fail(f"Function raised ValueError for zero load: {e}")

def test_negative_load():
    """Test that function raises ValueError for negative loads."""
    with pytest.raises(ValueError):
        design_lap_joint(-10, 150, 10, 10)

def test_invalid_dimensions():
    """Test that function handles invalid plate dimensions."""
    # Test negative thickness
    with pytest.raises(ValueError):
        design_lap_joint(50, 150, -5, 10)
    
    # Test negative width
    with pytest.raises(ValueError):
        design_lap_joint(50, -150, 10, 10)
    
    # Test zero thickness
    with pytest.raises(ValueError):
        design_lap_joint(50, 150, 0, 10)

def test_utilization_ratio():
    """Test that utilization ratio is always less than or equal to 1."""
    loads = [20, 50, 80, 100]
    for P in loads:
        design = design_lap_joint(P, 150, 10, 12)
        assert design["efficiency_of_connection"] <= 1.0, f"Utilization ratio exceeds 1.0 for load {P}kN"

def test_bolt_strength_calculator():
    """Test the bolt strength calculation function."""
    # Test different bolt grades
    fu, fy = calculate_bolt_strength(3.6)
    assert fu == 300.0
    assert fy == 180.0
    
    fu, fy = calculate_bolt_strength(4.6)
    assert fu == 400.0
    assert fy == 200.0
    
    fu, fy = calculate_bolt_strength(5.8)
    assert fu == 500.0
    assert fy == 350.0

def test_consistent_design():
    """Test that function produces consistent results for the same inputs."""
    design1 = design_lap_joint(80, 150, 10, 12)
    design2 = design_lap_joint(80, 150, 10, 12)
    
    for key in design1:
        assert design1[key] == design2[key], f"Inconsistent results for key: {key}"

def test_increasing_load_effect():
    """Test that increasing load leads to stronger design."""
    load1 = 50
    load2 = 100
    
    design1 = design_lap_joint(load1, 150, 10, 12)
    design2 = design_lap_joint(load2, 150, 10, 12)
    
    # More bolts or higher bolt grade or larger diameter
    stronger_design = (design2["number_of_bolts"] > design1["number_of_bolts"] or
                      design2["bolt_grade"] > design1["bolt_grade"] or
                      design2["bolt_diameter"] > design1["bolt_diameter"])
    
    assert stronger_design, "Increasing load did not result in stronger design"

def test_output_structure():
    """Test that the function returns the expected dictionary structure."""
    design = design_lap_joint(80, 150, 10, 12)
    expected_keys = [
        "bolt_diameter", "bolt_grade", "number_of_bolts", "pitch_distance",
        "gauge_distance", "end_distance", "edge_distance", "number_of_rows",
        "number_of_columns", "hole_diameter", "strength_of_connection",
        "yield_strength_plate_1", "yield_strength_plate_2",
        "length_of_connection", "efficiency_of_connection"
    ]
    
    for key in expected_keys:
        assert key in design, f"Missing key in output: {key}"

# Parametrized test for different configurations
@pytest.mark.parametrize("load,width,t1,t2", [
    (50, 150, 10, 10),
    (75, 180, 12, 14),
    (100, 200, 16, 16),
    (25, 120, 8, 10)
])
def test_various_configurations(load, width, t1, t2):
    """Test that function works for various configurations."""
    design = design_lap_joint(load, width, t1, t2)
    assert design is not None
    assert design["efficiency_of_connection"] <= 1.0

# Test edge cases with fixture
@pytest.fixture
def edge_case_params():
    return [
        (1, 150, 6, 6),  # Very small load
        (100, 100, 24, 24),  # Maximum thickness with high load
        (100, 300, 10, 10),  # Wide plates
    ]

def test_edge_cases(edge_case_params):
    """Test edge cases of the design function."""
    for params in edge_case_params:
        try:
            design = design_lap_joint(*params)
            assert design["efficiency_of_connection"] <= 1.0
        except ValueError as e:
            # Some edge cases might legitimately fail to find a design
            print(f"Edge case {params} failed with: {e}")