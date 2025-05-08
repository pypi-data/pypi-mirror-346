import numpy as np

class Null_value_transformer:
    def __init__(self):
        pass

    def fit(self, data, categorical_columns, mixed_columns):
        data = data.copy()
        self.nan_placeholder = "__NAN_PLACEHOLDER__"
        self.nan_columns = []
        for column in data.columns:
            data_col = data[column]
            if not data_col.isnull().any(): continue
            self.nan_columns.append(column)
            data[column] = data_col.fillna(self.nan_placeholder)
            if column not in categorical_columns:
                # Append the nan placeholder to the mixed columns such the method knows how to handle it
                if column in mixed_columns:
                    mixed_columns[column].append(self.nan_placeholder)
                else:
                    mixed_columns[column] = [self.nan_placeholder]
        return mixed_columns

        
        
    def transform(self,data):
        data = data.copy()
        for column in self.nan_columns:
            data[column] = data[column].replace(np.nan, self.nan_placeholder)
        return data

    def inverse_transform(self,data):
        data = data.copy()
        for column in self.nan_columns:
            data[column] = data[column].replace(self.nan_placeholder,np.nan)
        return data
