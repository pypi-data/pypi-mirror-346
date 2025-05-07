
import warnings

class Data_type_assigner:
    def __init__(self, data,integer_columns = [],mixed_columns = {}):
    
        self.data_type = data.dtypes
        self.integer_columns = integer_columns + data.select_dtypes(include=['int64']).columns.tolist()
        self.mixed_columns = mixed_columns
        for column in integer_columns:
            if column not in self.data_type: 
                warnings.warn(f"Column {column} not found in data, ignoring integer assignment")
                continue
            if data[column].isna().any(): continue # If we have nan values, we cant assign the column to interger, however we still treat it as integer
            data[column] = data[column].astype(int)
        
        self.number_of_decimals = self.get_column_desimal(data)
        

        

    def assign(self, data):
        for column in data.columns:
            if column in self.number_of_decimals and self.number_of_decimals[column] is not None:
                exclude_values = self.mixed_columns.get(column, [])
                data[column] = data[column].apply(
                    lambda x: round(x, self.number_of_decimals[column]) if x not in exclude_values else x
                )
        
        data = data.astype(self.data_type)
        return data

    
    def get_column_desimal(self, data):
        decimals = {}
        for column in data.columns:
            if data[column].dtype != 'int64':
                exclude_values = self.mixed_columns.get(column, [])
                decimals[column] = data[column].apply(
                    lambda x: len(str(x).split('.')[1]) if '.' in str(x) and float(f"0.{str(x).split('.')[1]}") not in exclude_values else 0
                ).max()
            else:
                decimals[column] = 0  # Integer columns have 0 decimals by default

        for column in self.integer_columns:  # Ensure integer columns are explicitly set to 0 decimals
            decimals[column] = 0
        return decimals
