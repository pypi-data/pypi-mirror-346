from mammoth_commons.models import ONNX, ONNXEnsemble
from mammoth_commons.integration import loader
from mammoth_commons.externals import prepare
import re
import numpy as np
import zipfile


@loader(
    namespace="mammotheu", version="v0042", python="3.12", packages=("onnxruntime",)
)
def model_onnx_ensemble(path: str = "") -> ONNXEnsemble:
    """<p>This ONNX Ensemble Module enables predictions using a <a href="https://scikit-learn.org/stable/modules/ensemble.html" target="_blank">boosting ensemble</a> mechanism, ideal for combining multiple weak learners to improve prediction accuracy. Boosting, a powerful technique in machine learning, focuses on training a series of simple models (weak learners) – often single-depth <a href="https://scikit-learn.org/stable/modules/tree.html#classification" target="_blank">decision trees</a> – and combining them into a strong ensemble model.</p>
    <p><b>Usage Instructions:</b> To load a model, users need to supply a zip file path. This zip file should include multiple weak learners, each saved in the ONNX format, as well as parameters, such as weights (often denoted as ‘alphas’), that define each learner’s contribution to the final model. For an example of preparing this file, please see <a href="https://github.com/mammoth-eu/mammoth-commons/blob/dev/tests/test-mfppb-onnx-ensemble.ipynb" target="_blank">our notebook</a>.</p>
    <p>The module currently supports the MMM-Fair Boosting Post Pareto (MFBPP) model, which is a specialized approach that applies fairness-aware boosting. In particular, the MFBPP model leverages multi-fairness metric MMM-fair (Multi-Max Mistreatment) to ensure that prediction outcomes remain unbiased across different demographic groups (defined by protected attributes) and achieves <i>Pareto optimality</i> by balancing fairness and predictive performance across different class. For a detailed explanation of MFBPP, you can refer to <a href="https://link.springer.com/chapter/10.1007/978-3-031-18840-4_21" target="_blank">the paper</a>.</p>

    <p><b>Train and upload: </b> To create and integrate your own MFBPP trained on your intended data, please follow the instructions given in our <a href="https://github.com/mammoth-eu/mammoth-commons/blob/dev/tests/test_mfppb_onnx_ensemble.ipynb" target="_blank">Test instructions</a> notebook.</p>

    Args:
        path: A zip file containing the ensemble elements such as weak learners, weight parameters, etc.
    """

    models = []
    model_names = []
    params = None

    def myk(name):
        return int(re.findall(r"[+-]?\d+", name)[0])

    # Read the zip file
    with zipfile.ZipFile(prepare(path)) as myzip:
        # Extract and load the weights file
        for file_name in myzip.namelist():
            if file_name.endswith(".npy"):
                with myzip.open(file_name) as param_file:
                    params = np.load(param_file, allow_pickle=True)
            elif file_name.endswith(".onnx"):
                model_names.append(file_name)

        model_names.sort(key=myk)

        for file_name in model_names:
            with myzip.open(file_name) as model_file:
                model_bytes = model_file.read()
                models.append(ONNX(model_bytes, np.float32))
    return ONNXEnsemble(models, **dict(params.item()))
