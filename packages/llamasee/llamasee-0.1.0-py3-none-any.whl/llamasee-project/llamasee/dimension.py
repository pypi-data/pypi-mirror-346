from typing import List, Dict, Optional

class Dimension:
    def __init__(self, name: str, type: str, hierarchy: Optional[List[str]] = None):
        self.name = name
        self.type = type  # 'temporal', 'categorical', 'numerical', 'hierarchical'
        self.hierarchy = hierarchy or []
        self.aggregation_levels = []
        self.comparison_methods = []

    def add_aggregation_level(self, level: str):
        self.aggregation_levels.append(level)

    def add_comparison_method(self, method: str):
        self.comparison_methods.append(method)

class DimensionConfig:
    def __init__(self):
        self.dimensions: Dict[str, Dimension] = {
            'time': Dimension(
                name='time',
                type='temporal',
                hierarchy=['year', 'quarter', 'month', 'week', 'day']
            ),
            'location': Dimension(
                name='location',
                type='hierarchical',
                hierarchy=['country', 'region', 'store']
            ),
            'product': Dimension(
                name='product',
                type='categorical',
                hierarchy=['category', 'subcategory', 'sku']
            ),
            'metric': Dimension(
                name='metric',
                type='numerical',
                hierarchy=None
            )
        }

    def get_dimension(self, name: str) -> Optional[Dimension]:
        return self.dimensions.get(name)

    def add_dimension(self, dimension: Dimension):
        self.dimensions[dimension.name] = dimension 