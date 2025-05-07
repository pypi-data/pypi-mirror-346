from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vectice.autolog.asset_services.metric_service import MetricService
from vectice.autolog.asset_services.property_service import PropertyService
from vectice.autolog.asset_services.service_types.vectice_types import VecticeType
from vectice.autolog.asset_services.technique_service import TechniqueService
from vectice.autolog.model_library import ModelLibrary
from vectice.models.model import Model
from vectice.models.table import Table
from vectice.utils.common_utils import get_asset_name, temp_directory

if TYPE_CHECKING:
    from pandas import DataFrame

    from vectice.autolog.model_types import ModelTypes


SKLEARN_TEMP_DIR = "sklearn"


def identify_estimator(asset: Any) -> tuple[bool, bool]:
    """Temporary fix for sklearn 1.6.0 and xgboost sklearn integration."""
    try:
        from sklearn.base import is_classifier, is_regressor

        return bool(is_regressor(asset)), bool(is_classifier(asset))
    except Exception:
        pass
    try:
        # sklearn 1.6.0, xgboost does not support this yet
        return (
            asset.__sklearn_tags__().estimator_type == "regressor",
            asset.__sklearn_tags__().estimator_type == "classifier",
        )
    except Exception:
        pass

    try:
        # xgboost temp fallback. Current sklearn integration is behind
        return (
            bool(getattr(asset, "_estimator_type", None) == "regressor"),
            bool(getattr(asset, "_estimator_type", None) == "classifier"),
        )
    except Exception:
        pass

    return False, False


class AutologSklearnService(MetricService, PropertyService, TechniqueService):
    def __init__(
        self,
        key: str,
        asset: Any,
        data: dict,
        custom_metrics_data: set[str | None],
        phase_name: str,
        prefix: str | None = None,
    ):
        self._asset = asset
        self._key = key
        self._temp_dir = temp_directory(SKLEARN_TEMP_DIR)
        self._model_name = get_asset_name(self._key, phase_name, prefix)

        super().__init__(cell_data=data, custom_metrics=custom_metrics_data)

    def get_asset(self):
        # xgboost relies on BaseEstimator
        # lightgbm has Booster and sklearn API which uses BaseEstimator
        try:
            from sklearn.pipeline import Pipeline

            is_regressor, is_classifier = identify_estimator(self._asset)

            if is_regressor or is_classifier or isinstance(self._asset, Pipeline):
                library = ModelLibrary.SKLEARN

                if isinstance(self._asset, Pipeline):
                    library = ModelLibrary.SKLEARN_PIPELINE
                elif str(self._asset.__class__.__module__) == "sklearn.model_selection._search":
                    library = ModelLibrary.SKLEARN_SEARCH

                temp_files = []
                if library is ModelLibrary.SKLEARN_PIPELINE:
                    temp_json_file_path, temp_html_file_path = self._get_sklearn_pipeline(self._asset, self._model_name)
                    if temp_json_file_path:
                        temp_files.append(temp_json_file_path)
                    if temp_html_file_path:
                        temp_files.append(temp_html_file_path)

                elif library is ModelLibrary.SKLEARN_SEARCH:
                    tables = self._get_sklearn_search_results_and_space_tables(self._asset, self._model_name)
                    temp_files.extend(tables)

                try:
                    # TODO fix regex picking up classes
                    # Ignore Initialized variables e.g LogisticRegression Class
                    self._asset.get_params()  # pyright: ignore[reportGeneralTypeIssues]
                    _, params = self._get_sklearn_or_xgboost_or_lgbm_info(self._asset)
                    model = Model(
                        library=library.value,
                        technique=self._get_model_technique(self._asset, ModelLibrary.SKLEARN),
                        metrics=self._get_model_metrics(self._cell_data),
                        properties=params,
                        name=self._model_name,
                        predictor=self._asset,
                        attachments=temp_files,
                    )
                    return {
                        "variable": self._key,
                        "model": model,
                        "asset_type": VecticeType.MODEL,
                    }
                except Exception:
                    pass
        except ImportError:
            pass

    def _get_sklearn_pipeline(self, pipeline: ModelTypes, model_name: str) -> tuple[str, str] | tuple[None, None]:
        try:
            from sklearn.utils import estimator_html_repr

            from vectice.utils.sklearn_pipe_utils import pipeline_to_json

            json_file_name = self._temp_dir / f"{model_name!s}_pipeline.json"
            html_file_name = self._temp_dir / f"{model_name!s}_pipeline.html"
            temp_json_file_path, temp_html_file_path = json_file_name.as_posix(), html_file_name.as_posix()

            pipeline_json = pipeline_to_json(pipeline)
            pipeline_html = estimator_html_repr(pipeline)
            if pipeline_json:
                with open(temp_json_file_path, "w") as json_file:
                    json_file.write(pipeline_json)

            if pipeline_html:
                with open(temp_html_file_path, "w", encoding="utf-8") as html_file:
                    html_file.write(pipeline_html)

            return temp_json_file_path, temp_html_file_path
        except Exception:
            return None, None

    def _get_sklearn_search_results_and_space_tables(self, model: ModelTypes, model_name: str) -> list:
        tables = []
        try:
            import pandas as pd

            results_df = pd.DataFrame(model.cv_results_)  # pyright: ignore
        except Exception:
            return tables
        try:
            tables.append(self._get_sklearn_search_space(model, model_name, results_df))
        except Exception:
            pass
        try:
            tables.append(self._get_sklearn_search_results(model, model_name, results_df))
        except Exception:
            pass
        return tables

    def _get_sklearn_search_results(self, model: ModelTypes, model_name: str, results_df: DataFrame) -> Table:
        sorted_df = results_df.sort_values(by="rank_test_score")
        top_scores_df = sorted_df.head(5)
        return Table(top_scores_df, name=f"{model_name}_search_results")

    def _get_sklearn_search_space(self, model: ModelTypes, model_name: str, results_df: DataFrame) -> Table:
        import pandas as pd

        param_columns = [col for col in results_df.columns if "param" in col and "params" not in col]
        data_dict = {}
        for param in param_columns:
            try:
                data_dict[f"{param} (min,max)"] = [[results_df[param].min(), results_df[param].max()]]
            except Exception:
                data_dict[f"{param} (uniques)"] = [results_df[param].unique()]

        params_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_dict.items()]))
        # Transpose the DataFrame
        df_transposed = params_df.transpose()
        # Reset the index to move row headers into a column
        df_transposed_reset = df_transposed.reset_index()
        # Rename the index column for clarity
        df_transposed_reset = df_transposed_reset.rename(columns={"index": "Parameters", 0: "Values"})
        return Table(df_transposed_reset, name=f"{model_name}_search_space")
