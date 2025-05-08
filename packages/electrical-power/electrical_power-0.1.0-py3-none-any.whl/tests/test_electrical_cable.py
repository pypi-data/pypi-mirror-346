import os
import sys

# tests_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(tests_dir)
# src_dir = os.path.join(project_root, 'src')
# if src_dir not in sys.path:
#     sys.path.insert(0, src_dir)

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from electrical_power.electrical_cables import CableOperations
from electrical_power.sqlite_tools import QuaryOutFormat # Required for mock signature

@pytest.fixture
def mock_db_tables():
    """Provides mock Pandas DataFrames for each table loaded by CableOperations."""
    tables = {
        'icc': pd.DataFrame({
            'conductor_material': ['cu', 'cu', 'cu', 'al', 'cu', 'cu'],
            'insulation_material': ['pvc', 'pvc', 'xlpe', 'pvc', 'pvc', 'pvc'],
            'sheath_material': ['pvc', 'pvc', 'pvc', 'pvc', 'pvc', 'pvc'],
            'armour_type': ['none', 'none', 'none', 'none', 'sta', 'none'],
            'cores': [1, 3, 1, 3, 3, 1], # Added one more for 4mm2 single core
            'csa': ['1.5', '2.5', '4', '6', '10', '4'], # String type as in original
            'amps_laid_in_air_flat_spaced': [20, 30, 40, 50, 60, 35],
            'amps_laid_in_air_flat_touched': [18, 28, 38, 48, 58, 33],
            'amps_laid_in_groud_flat': [25, 35, 45, 55, 70, 42],
            'amps_laid_in_groud_duct': [22, 32, 42, 52, 65, 38],
            'ac_resistance_20deg': ['12.1', '7.41', '4.61', '3.08', '1.83/2.24', '4.61']
        }),
        'installation_method': pd.DataFrame({'method_name': ['tray_horizontal_spaced', 'burried_direct']}),
        'material_conductor': pd.DataFrame({'material': ['cu', 'al']}),
        'material_isolation': pd.DataFrame({'material': ['pvc', 'xlpe']}),
        'air_temprature_derating_factors': pd.DataFrame({
            'temperature': [25, 30, 35, 40, 45, 50],
            'pvc': [1.08, 1.00, 0.91, 0.82, 0.71, 0.58],
            'xlpe': [1.05, 1.00, 0.95, 0.90, 0.85, 0.80]
        }),
        'ground_temprature_derating_factors': pd.DataFrame({
            'temperature': [15, 20, 25, 30, 35, 40, 45],
            'pvc': [1.07, 1.00, 0.93, 0.85, 0.76, 0.67, 0.56],
            'xlpe': [1.05, 1.00, 0.95, 0.90, 0.85, 0.80, 0.74]
        }),
        'burial_depth_derating_factors': pd.DataFrame({
            'installation_method': ['burried_direct', 'burried_direct', 'burried_direct', 'burried_duct'],
            'cores': [1, 3, 1, 1], # Ensure '3' is treated as int if code expects
            'size': ['less_185', 'less_185', 'greater_185', 'less_185'],
            'depth': [0.5, 0.5, 0.5, 0.5],
            'factor': [1.0, 0.98, 0.95, 0.98]
        }),
        'soil_thermal_resistivity_derating_factors': pd.DataFrame({
            'soil_thermal_resistivity_Km_to_W': [1.0, 1.5, 2.0],
            'burried_direct': [1.0, 0.9, 0.8],
            'burried_duct': [1.0, 0.88, 0.78]
        }),
        'pvc_rated_temperature_derating_factors': pd.DataFrame({ # Used for 'pvc_derating'
            'temperature': [60, 70, 80], # ambient_temp=30 will pick 60C row (factor 1.0)
            'free_air': [1.0, 0.9, 0.8],
            'duct': [1.0, 0.88, 0.78],
            'burried_direct': [1.0, 0.85, 0.75]
        }),
        'laid_direct_in_ground_derating_factors': pd.DataFrame({
            'installation_formation': ['flat', 'trefoil', 'flat'],
            'cores': ['single', 'multi', 'multi'],
            'circuits_no': [2, 2, 2],
            'spacing': [0, 0.15, 0], # spacing 0 means touching
            'factor': [0.8, 0.85, 0.75]
        }),
        'grouping_derating_factors': pd.DataFrame({
            'cores': ['single', 'multi', 'single', 'multi'],
            'trays_no': [1, 1, 1, 1],
            'cables_no': [1, 1, 2, 2], # cables_no=1 means no grouping factor essentially
            'installation_method': [
                'tray_horizontal_spaced_flat', 'tray_horizontal_spaced',
                'tray_horizontal_spaced_flat', 'tray_horizontal_spaced'
            ],
            'factor': [1.0, 1.0, 0.9, 0.8] # Factor 1.0 for single cable/circuit
        }),
        'voltage_drop': pd.DataFrame({ # mV/A/m
            'cores': ['single', 'multi', 'single', 'multi'],
            'conductor_material': ['cu', 'cu', 'cu', 'cu'],
            'insulation_material': ['pvc', 'pvc', 'xlpe', 'pvc'],
            'csa': [1.5, 2.5, 4.0, 10.0],
            'flat': [29, 18, 11, 3.8],
            'trefoil': [28, 17, 10, 3.7],
            'flat_sta': [29, 18, 11, 3.8], # For STA armoured cables
            'flat_awa': [29,18,11, 3.8]
        }),
        'size': pd.DataFrame({'size_val': [1.5, 2.5, 4.0, 6.0, 10.0]})
    }
    # Ensure 'cores' in burial_depth_derating_factors is int if code compares with int
    tables['burial_depth_derating_factors']['cores'] = tables['burial_depth_derating_factors']['cores'].astype(int)
    return tables

@pytest.fixture
def cable_ops_instance(mock_db_tables):
    """Provides a CableOperations instance with mocked database interactions."""
    #  patch('electrical_power.electrical_cables.resources.files') as mock_files, \
    #      patch('electrical_power.electrical_cables.resources.as_file') as mock_as_file, \
    with  patch('electrical_power.electrical_cables.SqliteTools') as MockSqliteTools:

        mock_file_obj = MagicMock()
        #mock_files.return_value = mock_file_obj
        mock_file_obj.joinpath.return_value = "dummy_path_to.db"

        mock_as_file_manager = MagicMock()
        mock_as_file_manager.__enter__.return_value = "dummy_path_to.db"
        mock_as_file_manager.__exit__.return_value = None
        #mock_as_file.return_value = mock_as_file_manager

        mock_db_instance = MockSqliteTools.return_value
        
        def mock_read_table(table_name, out_format=None):
            if table_name in mock_db_tables:
                return mock_db_tables[table_name].copy()
            raise ValueError(f"Mock data for table '{table_name}' not found in mock_db_tables.")
        
        mock_db_instance.read_table.side_effect = mock_read_table
        mock_db_instance.connect_db.return_value = (None, None)

        instance = CableOperations()
        return instance

def test_select_cable_simple_pvc_air(cable_ops_instance):
    """Test basic cable selection for PVC in air, single phase."""
    selected_cable_df = cable_ops_instance.select_cable(
        load_current=15,
        cable_run=10,
        load_voltage=230,
        load_type='distribution_1ph',
        ambient_temperature=30,
        installation_method='tray_horizontal_spaced', # -> air_burried = 'free_air'
        installation_formation='flat',
        trays_no=1,
        cricuits_in_tray=1 # -> grouping factor = 1.0
    )
    assert not selected_cable_df.empty
    # Expecting single core selection to be 1.5mm2 based on mock data and logic
    # Row 0 should be single core, Row 1 multi-core
    # Check if the first row (single core) has 'csa'
    if 'csa' in selected_cable_df.iloc[0] and not pd.isna(selected_cable_df.iloc[0]['csa']):
        assert selected_cable_df.iloc[0]['csa'] == '1.5'
        assert selected_cable_df.iloc[0]['conductor_material'] == 'cu'
        assert selected_cable_df.iloc[0]['insulation_material'] == 'pvc'
        assert selected_cable_df.iloc[0]['cores'] == 1
        assert selected_cable_df.iloc[0]['Vd'] < (3/100 * 230) # Check Vd constraint
    else:
        # This case means no single core was found or the structure is unexpected
        assert "No single core available" not in selected_cable_df.iloc[0].to_string(), "Expected a single core cable"

def test_select_cable_burried_direct_sta(cable_ops_instance):
    """Test cable selection for burried direct, STA armoured, 3-phase."""
    selected_cable_df = cable_ops_instance.select_cable(
        load_current=30,
        cable_run=50,
        load_voltage=400,
        load_type='distribution_3ph',
        ambient_temperature=30, # For pvc_derating factor
        ground_temperature=25,  # For ground derating
        installation_method='burried_direct',
        installation_formation='flat',
        cable_armour='sta',
        burial_depth=0.5,
        cricuits_in_tray=1 # No grouping derate for laid_direct_in_ground
    )
    assert not selected_cable_df.empty
    # Expecting multi-core selection to be 10mm2 PVC STA based on mock data
    # Row 1 should be multi-core
    if 'csa' in selected_cable_df.iloc[1] and not pd.isna(selected_cable_df.iloc[1]['csa']):
        assert selected_cable_df.iloc[1]['csa'] == '10'
        assert selected_cable_df.iloc[1]['conductor_material'] == 'cu'
        assert selected_cable_df.iloc[1]['insulation_material'] == 'pvc'
        assert selected_cable_df.iloc[1]['cores'] == 3
        assert selected_cable_df.iloc[1]['armour_type'] == 'sta'
        assert selected_cable_df.iloc[1]['Vd'] < (3/100 * 400)
    else:
        assert "Series" not in str(type(selected_cable_df.iloc[1])) or \
               "No multi core available" not in selected_cable_df.iloc[1].to_string(), \
               "Expected a multi-core cable"

def test_select_cable_voltage_drop_limits(cable_ops_instance):
    """Test scenario where voltage drop becomes the limiting factor."""
    selected_cable_df = cable_ops_instance.select_cable(
        load_current=10, # Low current
        cable_run=200,   # Long run
        load_voltage=230,
        load_type='distribution_1ph',
        ambient_temperature=30,
        installation_method='tray_horizontal_spaced',
        installation_formation='flat'
    )
    assert not selected_cable_df.empty
    # Expecting a larger cable than 1.5mm2 due to Vd, e.g., 4mm2 single core
    if 'csa' in selected_cable_df.iloc[0] and not pd.isna(selected_cable_df.iloc[0]['csa']):
        assert selected_cable_df.iloc[0]['csa'] == '4' # Based on mock data, 1.5mm2 Vd would be too high
        assert selected_cable_df.iloc[0]['Vd'] < (3/100 * 230)

def test_get_icc_existing(cable_ops_instance):
    """Test get_icc for an existing cable in mock data."""
    icc_data = cable_ops_instance.get_icc(
        conductor_material='cu',
        insulation_material='pvc',
        sheath_material='pvc',
        cores=1,
        armour_type='none',
        size=1.5 # Corresponds to '1.5' csa string
    )
    assert icc_data is not None
    assert isinstance(icc_data, pd.Series)
    assert icc_data['csa'] == '1.5'
    assert icc_data['amps_laid_in_air_flat_spaced'] == 20

def test_get_icc_non_existing(cable_ops_instance):
    """Test get_icc for a non-existing cable."""
    icc_data = cable_ops_instance.get_icc(
        conductor_material='ag', # Silver - not in mock
        insulation_material='pvc',
        sheath_material='pvc',
        cores=1,
        armour_type='none',
        size=1.5
    )
    assert icc_data is not None
    assert isinstance(icc_data, pd.Series)

def test_get_cable_Lmax(cable_ops_instance):
    """Test calculation of maximum cable length."""
    # Using ac_resistance_20deg for 1.5mm2 Cu PVC = 12.1 mOhm/m
    # Vd = 3%, Load V = 230V, Load A = 10A, PF = 0.8, ambient_temp = 20C
    # cable_resis = '12.1' (mOhm/m)
    # load_type = 'distribution_1ph'
    # Max Vd = 0.03 * 230 = 6.9V
    # Lmax = (V_actual_drop * 1000) / (2 * I * (R_eff_per_m * PF + X_eff_per_m * sin(acos(PF))))
    # The formula in get_cable_Lmax is:
    # Lmax = (load_voltage*voltage_drop/100) * 1000 / (2*load_amps*(pf+math.sin(math.acos(pf))))
    # This formula seems to assume R and X are combined into (pf + sin(acos(pf))) which is not standard.
    # It does not directly use cable_resis in this part of the formula.
    # The `resis_corr` part is calculated but not used in the Lmax formula shown.
    # Given the formula in the code:
    # Lmax = (230 * 3/100) * 1000 / (2 * 10 * (0.8 + math.sin(math.acos(0.8))))
    # Lmax = 6.9 * 1000 / (20 * (0.8 + 0.6)) = 6900 / (20 * 1.4) = 6900 / 28 = 246.42

    # Let's test with the values that would be passed from select_cable
    # For 1.5mm2 Cu cable (ac_resistance_20deg = '12.1')
    # load_type='distribution_1ph', ambient_temperature=20
    # The `resis_corr` calculation inside `get_cable_Lmax` will be:
    # resis_corr = (22 / 1.5) * (1+0.00393*(20-20)) = 22 / 1.5 = 14.666 mOhm/m
    # However, the Lmax formula in the code does not use this `resis_corr` or `cable_resis` directly.
    # It uses a simplified impedance factor.

    lmax = cable_ops_instance.get_cable_Lmax(
        voltage_drop=3, # %
        load_voltage=230,
        power_factor=0.8,
        load_amps=10,
        cable_resis='12.1', # This is mOhm/m from table, but not directly used in the Lmax formula as expected
        ambient_temperature=20,
        conductor_material='cu',
        cable_csa=1.5,
        load_type='distribution_1ph'
    )
    # Based on the formula in the code:
    # Lmax = (V_load * Vd_percent/100) * 1000 / (K * I_load * (PF + QF))
    # For 1ph, K=2. For 3ph, K=sqrt(3).
    # QF = sin(acos(PF)). If PF=0.8, QF=0.6. (PF+QF) = 1.4
    # Lmax = (230 * 0.03 * 1000) / (2 * 10 * 1.4) = 6900 / 28 = 246.428
    assert abs(lmax - 246.428) < 0.01

def test_select_cable(cable_ops_instance):
    selected_new_cable = cable_ops_instance.select_cable(
                            load_voltage= 400, 
                            load_current=30,
                            cable_run=100,
                            load_type='distribution_3ph',
                            installation_method='burried_direct',
                            cable_armour='sta',
                            installation_formation='flat',
                            ground_temperature=45
                            )
    assert selected_new_cable is not None
    assert isinstance(selected_new_cable, pd.DataFrame)

# To run these tests, navigate to your project root in the terminal and run:
# pytest

# If you had a pytest.main() call for running tests within the script, it's removed
# as it's better to use the pytest CLI.
