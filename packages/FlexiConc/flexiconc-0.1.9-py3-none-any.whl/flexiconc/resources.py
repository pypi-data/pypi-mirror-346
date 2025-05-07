from typing import Any, Dict, List
import pandas as pd

class ResourceRegistry:
    def __init__(self):
        # { resource_type: { name: (resource_obj, details) } }
        self._registry: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, resource: Any, *,
                 resource_type: str, details: Dict[str, Any] = None):
        """Register a resource under a given type."""
        if resource_type == "frequency_list":
            df = resource
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Frequency lists must be a pandas DataFrame.")
            if df.shape[1] < 2:
                raise ValueError("Frequency lists must have at least two columns.")
            required_cols = {"f", "ipm", "rel_f"}
            if not required_cols.intersection(df.columns):
                raise ValueError("Frequency lists must include at least one of the columns: 'f', 'ipm', or 'rel_f'.")

        self._registry.setdefault(resource_type, {})[name] = (resource, details or {})

    def list(self, resource_type: str = None) -> List[str] | Dict[str, List[str]]:
        """List resource names, optionally filtered by type."""
        if resource_type:
            return list(self._registry.get(resource_type, {}).keys())
        return {rtype: list(entries.keys()) for rtype, entries in self._registry.items()}

    def get(self, resource_type: str, name: str, parameters: Dict[str, Any] = None) -> Any:
        """Retrieve a specific resource, with optional transformation for frequency lists."""
        resource, details = self._registry[resource_type][name]
        parameters = parameters or {}

        if resource_type == "frequency_list":
            freq_cols = parameters.get("frequency_columns")
            if not freq_cols:
                return resource

            df = resource.copy()

            def compute_rel_f_from_ipm():
                df["rel_f"] = df["ipm"] / 1_000_000

            def compute_ipm_from_rel_f():
                df["ipm"] = df["rel_f"] * 1_000_000

            def compute_rel_f_from_f():
                sample_size = details.get("sample_size")
                if not sample_size:
                    sample_size = df["f"].sum()
                df["rel_f"] = df["f"] / sample_size

            def compute_ipm_from_f():
                compute_rel_f_from_f()
                compute_ipm_from_rel_f()

            def compute_f_from_rel_f():
                sample_size = details.get("sample_size")
                if not sample_size:
                    raise ValueError("sample_size must be specified in details to compute 'f'")
                df["f"] = df["rel_f"] * sample_size

            for col in freq_cols:
                if col in df.columns:
                    continue
                if col == "rel_f":
                    if "ipm" in df.columns:
                        compute_rel_f_from_ipm()
                    elif "f" in df.columns:
                        compute_rel_f_from_f()
                elif col == "ipm":
                    if "rel_f" in df.columns:
                        compute_ipm_from_rel_f()
                    elif "f" in df.columns:
                        compute_ipm_from_f()
                elif col == "f":
                    if not "rel_f" in df.columns:
                        compute_rel_f_from_ipm()
                    compute_f_from_rel_f()

            token_attrs = parameters.get("token_attribute_columns", [])
            if isinstance(token_attrs, list) and len(token_attrs) >= 1:
                agg_cols = [col for col in ["f", "rel_f", "ipm"] if col in df.columns]
                df = df.groupby(token_attrs, as_index=False)[agg_cols].sum()

            sort_col = next((col for col in ["f", "rel_f", "ipm"] if col in freq_cols and col in df.columns), None)
            if sort_col:
                df = df.sort_values(by=sort_col, ascending=False)

            return df[[col for col in df.columns if col in freq_cols or not col in ["f", "ipm", "rel_f"]]]

        return resource


    def details(self, resource_type: str, name: str) -> Dict[str, Any]:
        """Get metadata about a resource."""
        return self._registry[resource_type][name][1]
