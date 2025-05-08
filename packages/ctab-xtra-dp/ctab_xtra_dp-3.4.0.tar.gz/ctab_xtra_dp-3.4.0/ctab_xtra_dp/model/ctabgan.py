"""
Generative model training algorithm based on the CTABGANSynthesiser

"""
import pandas as pd
import time
from .pipeline.data_preparation import DataPrep
from .synthesizer.ctabgan_synthesizer import CTABGANSynthesizer

from .pipeline.data_type_assigner import Data_type_assigner
from .pipeline.data_preparation import DataPrep as DataPrep
from .pipeline.null_value_transformer import Null_value_transformer


import warnings

warnings.filterwarnings("ignore")

class CTAB_XTRA_DP():

    def __init__(self,
                 df,
                 categorical_columns = [], 
                 log_columns = [],
                 mixed_columns= {},
                 general_columns = [],
                 non_categorical_columns = [],
                 integer_columns = [],
                 problem_type= {},
                 dp_constraints = {}
                 ):

        self.__name__ = 'CTABGAN'
              
        self.synthesizer = CTABGANSynthesizer()
        self.raw_df = df
        self.dp_constraints = dp_constraints
        self.categorical_columns = categorical_columns
        self.log_columns = log_columns
        self.mixed_columns = mixed_columns
        self.general_columns = general_columns
        self.non_categorical_columns = non_categorical_columns
        self.integer_columns = integer_columns
        self.problem_type = problem_type
                
    def fit(self,epochs= 100):
        
        start_time = time.time()
        
        self.data_type_assigner = Data_type_assigner(self.raw_df, self.categorical_columns,self.mixed_columns)
        
        self.null_value_transformer = Null_value_transformer()
        self.mixed_columns = self.null_value_transformer.fit(self.raw_df, self.categorical_columns, self.mixed_columns)
        self.raw_df = self.null_value_transformer.transform(self.raw_df)

        self.data_prep = DataPrep(self.raw_df,self.categorical_columns,self.log_columns)
        self.prepared_data = self.data_prep.preprocesses_transform(self.raw_df)

        self.synthesizer.fit(train_data=self.prepared_data,
                    dp_constraints=self.dp_constraints, 
                     categorical=self.categorical_columns, 
                     mixed=self.mixed_columns, 
                     general=self.general_columns, 
                     non_categorical=self.non_categorical_columns, 
                     type=self.problem_type, 
                     epochs=epochs)
        end_time = time.time()
        print('Finished training in',end_time-start_time," seconds.")


    def generate_samples(self,n=1000,conditioning_column=None, conditioning_value=None):

        column_index = None
        column_value_index = None
        if conditioning_column and conditioning_value:
            column_index = self.prepared_data.columns.get_loc(conditioning_column) if conditioning_column in self.prepared_data.columns else ValueError("Conditioning column", conditioning_column, "not found in the data columns")
            column_value_index = self.data_prep.get_label_encoded(column_index, conditioning_value)
        
        sample_transformed = self.synthesizer.sample2(n)#self.synthesizer.sample(n, column_index, column_value_index)
        sample_transformed = pd.DataFrame(sample_transformed, columns=self.prepared_data.columns)
        
        sample = self.data_prep.preprocesses_inverse_transform(sample_transformed)
        sample = self.null_value_transformer.inverse_transform(sample)
        sample_with_data_types = self.data_type_assigner.assign(sample)
        
        return sample_with_data_types
