from plottr.data.datadict import DataDict
from plottr.node.tools import linearFlowchart
from plottr.data.qcodes_dataset import QCodesDSLoader
from plottr.node.data_selector import DataSelector
from plottr.node.grid import DataGridder
from plottr.node.dim_reducer import XYSelector
from plottr.node.filter.correct_offset import SubtractAverage
from plottr.plot import PlotNode


def test_qcodes_flow_shaped_data(qtbot, dataset_with_shape):

    fc = linearFlowchart(
        ('Data loader', QCodesDSLoader),
        ('Data selection', DataSelector),
        ('Grid', DataGridder),
        ('Dimension assignment', XYSelector),
        ('Subtract average', SubtractAverage),
        ('plot', PlotNode)
    )
    loader = fc.nodes()['Data loader']
    selector = fc.nodes()['Data selection']
    selector.selectedData = 'z_0'

    loader.pathAndId = dataset_with_shape.path_to_db, dataset_with_shape.run_id
    loader.update()
    assert 1 == 1


