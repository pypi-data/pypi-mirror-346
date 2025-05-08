class PipelineComponent:
        
    def generate_schema(self) -> dict:
        raise NotImplementedError("Use one of the subclasses for your specific need")

class PipelineField(PipelineComponent):
    
    def __init__(self, field_name: str, field_type: str, required: bool, description: str, section_name: str = "base"):
        self.name = field_name
        self.type = field_type
        self.required = required
        self.description = description
        self.section = section_name
        
    def generate_schema(self):
        return {
            "name": self.name,
            "type": self.type,
            "required": self.required,
            "description": self.description
        }
        
    def get_name(self) -> str:
        return self.name
        
    def get_section(self) -> str:
        return self.section
    
class Query(PipelineComponent):
    
    def __init__(self, query_name: str, connector_name: str):
        self.name = query_name
        self.connector = connector_name
    
    def get_name(self) -> str:
        return self.name

class SQLQuery(Query):
    
    def __init__(self, query_name: str, connector_name: str):
        super().__init__(query_name,connector_name)
        self.clauses = []
        
    def add_clause(self, sql_clause: str, optional: bool, field_required: str = None):
        clause = {
            "sql": sql_clause,
            "optional": optional
        }
        if optional:
            clause["field"] = field_required
        self.clauses.append(clause)
        
    def generate_schema(self) -> dict:
        query_dict = {
            "name": self.name,
            "connector": self.connector,
            "sql_clauses": self.clauses
        }
        return query_dict
        
class ErrorSQLQuery(SQLQuery):
    
    def __init__(self, query_name: str, connector_name: str, min_results: int, error_message: str):
        super().__init__(query_name,connector_name)
        self.min_results = min_results
        self.error_message = error_message
        
    def generate_schema(self) -> dict:
        query_dict = super().generate_schema()
        query_dict["min_results"] = self.min_results
        query_dict["error"] = self.error_message
        return query_dict
    
class Filter(PipelineComponent):
    
    def __init__(self, filter_name: str, display_name: str, column_name: str, query_name: str, include_any: bool = True):
        self.name = filter_name
        self.display_name = display_name
        self.column_name = column_name
        self.query = query_name
        self.include_any = include_any
        
    def get_name(self) -> str:
        return self.filter_name
    
    def generate_schema(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
            "column_name": self.column_name,
            "include_any": self.include_any,
            "query": self.query
        }    
        
class Dataset(PipelineComponent):
    
    def __init__(self, dataset_name: str):
        self.name = dataset_name
        self.create_schema = None
        self.operations = []
        
    def get_name(self) -> str:
        return self.name
        
    def create_from_query(self, query_name: str):
        if self.create_schema is not None:
            raise ValueError("A dataset can only have one create operation.")
            
        self.create_schema = {
            "type": "query",
            "name": query_name
        }
    
    def create_from_dataset(self, dataset_name: str):
        if self.create_schema is not None:
            raise ValueError("A dataset can only have one create operation.")
        
        self.create_schema = {
            "type": "query",
            "name": dataset_name
        }
        
    def merge_two_datasets(self, dataset1_name: str, dataset2_name: str, how: str, left_on: str, right_on: str, nan_replace = None):
        if self.create_schema is not None:
            raise ValueError("A dataset can only have one create operation (create from query/dataset or merge two datasets).")
        
        how = how.lower()
        if how not in ["left","right","inner","outer"]:
            raise AttributeError('how must be one of "left","right","inner","outer"')
        self.create_schema = {
            "type": "merge",
            "dataset1": dataset1_name,
            "dataset2": dataset2_name,
            "how": how,
            "left_on": left_on,
            "right_on": right_on
        }
        if nan_replace is not None:
            self.create_schema["nan_replace"] = nan_replace
        
    def add_function(self, function_name: str, function_fields_dict: dict = None, function_params_dict: dict = None, required_fields: list[str] = None):
        function_dict = {
            "type" : "function",
            "name" : function_name
        }
        
        if required_fields is not None:
            function_dict["required_fields"] = required_fields
            
        if function_fields_dict is not None:
            function_dict["fields"] = function_fields_dict
            
        if function_params_dict is not None:
            function_dict["params"] = function_params_dict
            
        self.operations.append(function_dict)
    
    def add_filter(self, columns_to_filter: list[str]):
        self.operations.append({
            "type": "filter",
            "filters": columns_to_filter
        })
        
    def add_arithmetic_operation(self, arithmetic_operation: str, column: str, by: float):
        if arithmetic_operation not in ["+","-","*","/"]:
            raise AttributeError('arithmetic_operation must be one of "+","-","*","/"')
        
        self.operations.append({
            "type": "arithmetic",
            "column": column,
            "operation": arithmetic_operation,
            "by": by
        })
        
    def generate_schema(self):
        if self.create_schema is None:
            raise ValueError("A dataset must have a create operation (create from query/dataset or merge two datasets).")
        
        schema = {
            "name": self.name,
            "create": [self.create_schema]
        }
        schema["create"].extend(self.operations)
        
        return schema
        
class SummaryDataset(Dataset):
    
    def __init__(self, dataset_name: str, summary_by_row: str, summary_prefix: str = None, summary_suffix: str = None, remove_comma: bool = False):
        super().__init__(dataset_name)
        self.prefix = summary_prefix
        self.summary = summary_by_row
        self.suffix = summary_suffix
        self.remove_comma = remove_comma
        
    def generate_schema(self):
        dataset_schema = super().generate_schema()
        if self.prefix is not None:
            dataset_schema["prefix"] = self.prefix
        dataset_schema["summary"] = self.summary
        if self.suffix is not None:
            dataset_schema["suffix"] = self.suffix
        dataset_schema["remove_comma"] = self.remove_comma
        return dataset_schema
        
class Summary(PipelineComponent):
    
    def __init__(self, datasets: list[Dataset]):
        self.datasets = datasets
        
    def generate_schema(self):
        if len(self.datasets) == 0:
            raise ValueError("There must be at least one dataset to generate a summary.")
        
        summary_schema = {
            "datasets": []
        }        
        for dataset in self.datasets:
            summary_schema["datasets"].append(dataset.get_name())
        
        return summary_schema
        
class Visualization(PipelineComponent):
    
    def __init__(self, dataset: Dataset, title: str, description: str):
        self.dataset = dataset.get_name()
        self.title = title
        self.description = description
        
class PieChart(Visualization):
    
    def __init__(self, dataset: Dataset, title: str, description: str, value_column: str, label_column: str):
        super().__init__(dataset, title, description)
        self.value_column = value_column
        self.label_column = label_column
        
    def generate_schema(self):
        return {
            "type": "pie",
            "dataset": self.dataset,
            "title": self.title,
            "value_column": self.value_column,
            "label_column": self.label_column
        }
        
class LineGraph(Visualization):
    
    def __init__(self, dataset: Dataset, title: str, description: str, x_axis: str, y_axis: str):
        super().__init__(dataset, title, description)
        self.x_axis = x_axis
        self.y_axis = y_axis
        
    def generate_schema(self):
        return {
            "type": "line",
            "dataset": self.dataset,
            "title": self.title,
            "x_axis": self.x_axis,
            "y_axis": self.y_axis
        }
        
class MultiLineGraph(Visualization):
    
    def __init__(self, dataset: Dataset, title: str, description: str, x_axis: str, columns: list[str], y_axis: str):
        super().__init__(dataset, title, description)
        self.x_axis = x_axis
        self.y_axis = columns
        self.y_axis_name = y_axis
        
    def generate_schema(self):
        return {
            "type": "line",
            "dataset": self.dataset,
            "title": self.title,
            "x_axis": self.x_axis,
            "y_axis": self.y_axis,
            "y_axis_name": self.y_axis_name
        }
        
class Histogram(Visualization):
    
    def __init__(self, dataset: Dataset, title: str, description: str, value_column: str):
        super().__init__(dataset, title, description)
        self.value_column = value_column
        
    def generate_schema(self):
        return {
            "type": "histogram",
            "dataset": self.dataset,
            "title": self.title,
            "value_column": self.value_column
        }
        
class StackedBarChart(Visualization):
    
    def __init__(self, dataset: Dataset, title: str, description: str, value_column: str, label_column: str, color_column: str):
        super().__init__(dataset, title, description)
        self.value_column = value_column
        self.label_column = label_column
        self.color_column = color_column
        
    def generate_schema(self):
        return {
            "type": "stacked_bar",
            "dataset": self.dataset,
            "title": self.title,
            "value_column": self.value_column,
            "label_column": self.label_column,
            "color_column": self.color_column
        }
        
class PipelineSchema:
    
    def __init__(self, pipeline_name: str, fields: list[PipelineField]):
        self.name = pipeline_name
        self.fields = fields
        self.schema = {
            "pipeline_name": self.name
        }
        
    def build_pipeline_schema(self):
        self.build_fields_schema()
    
    def build_fields_schema(self):
        fields_schema = {}
        for field in self.fields:
            section = field.get_section()
            sections = section.split('.')
            sub_schema = fields_schema
            for sect in sections:
                if section not in sub_schema.keys():
                    sub_schema[sect] = {}
                sub_schema = sub_schema[sect]
            sub_schema[field.get_name()] = field.generate_schema()
            
        self.schema["fields"] = fields_schema
            
    def get_schema(self):
        self.build_pipeline_schema()
        return self.schema
        
class BasicPipelineSchema:
    
    def __init__(self, pipeline_name: str, fields: list[PipelineField], queries: list[Query], datasets: list[Dataset]):
        self.name = pipeline_name
        self.fields = fields
        self.queries = queries
        self.filters: list[Filter] = None
        self.datasets = datasets
        self.schema = {
            "pipeline_name": self.name
        }
        
    def build_pipeline_schema(self):
        self.build_fields_schema()
        self.build_queries_schema()
        self.build_dataset_schema()
    
    def build_fields_schema(self):
        fields_schema = {}
        for field in self.fields:
            section = field.get_section()
            sections = section.split('.')
            sub_schema = fields_schema
            for sect in sections:
                if section not in sub_schema.keys():
                    sub_schema[sect] = {}
                sub_schema = sub_schema[sect]
            sub_schema[field.get_name()] = field.generate_schema()
            
        self.schema["fields"] = fields_schema
        
    def build_queries_schema(self):
        if len(self.queries) > 0:
            self.schema["queries"] = {}
        for query in self.queries:
            self.schema["queries"][query.get_name()] = query.generate_schema()
            
    def build_filters_schema(self):
        if self.filters is None:
            return
        if len(self.filters) > 0:
            self.schema["filters"] = {}
        for filter in self.filters:
            self.schema["filters"][filter.get_name()] = filter.generate_schema()
            
    def build_dataset_schema(self):
        if len(self.datasets) > 0:
            self.schema["datasets"] = {}
        for dataset in self.datasets:
            self.schema["datasets"][dataset.get_name()] = dataset.generate_schema()
            
class StandardPipelineSchema(BasicPipelineSchema):
    
    def __init__(self, pipeline_name: str, fields: list[PipelineField], queries: list[Query], datasets: list[Dataset], scope: str, scope_description: str, summary: Summary = None, visualizations: list[Visualization] = None):
        super().__init__(pipeline_name, fields, queries, datasets)
        self.scope = scope
        self.scope_description = scope_description
        self.summary = summary
        self.visualizations = visualizations
        
    def build_pipeline_schema(self):
        self.schema["scope"] = self.scope
        self.schema["scope_description"] = self.scope_description
        super().build_pipeline_schema()
        if self.summary is not None:
            self.build_summary_schema()
            
        if self.visualizations is not None and len(self.visualizations) > 0:
            self.build_visualizations_schema()
        
    def build_summary_schema(self):
        self.schema["summary"] = self.summary.generate_schema()
        
    def build_visualizations_schema(self):
        self.schema["visualizations"] = []
        for visualization in self.visualizations:
            self.schema["visualizations"].append(visualization.generate_schema())
            
class DashboardPipelineSchema(StandardPipelineSchema):
    
    def __init__(self, pipeline_name: str, fields: list[PipelineField], queries: list[Query], filters: list[Filter], datasets: list[Dataset], scope: str, scope_description: str, summary: Summary = None, visualizations: list[Visualization] = None):
        super
        super().__init__(pipeline_name, fields, queries, datasets, scope, scope_description, summary, visualizations)
        self.filters = filters
        
    def build_pipeline_schema(self):
        super().build_pipeline_schema()
        super().build_filters_schema()