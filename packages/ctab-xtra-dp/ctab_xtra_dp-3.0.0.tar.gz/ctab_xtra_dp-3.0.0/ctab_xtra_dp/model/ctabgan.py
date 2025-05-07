"""
Generative model training algorithm based on the CTABGANSynthesiser

"""
import pandas as pd
import time
from model.pipeline.data_preparation import DataPrep
from model.synthesizer.ctabgan_synthesizer import CTABGANSynthesizer

from model.pipeline2.data_type_assigner import Data_type_assigner
from model.pipeline2.data_preparation import DataPrep as DataPrep2
from model.pipeline2.null_value_transformer import Null_value_transformer


import warnings

warnings.filterwarnings("ignore")

class CTABGAN():

    def __init__(self,
                 df,
                 test_ratio = 0.20,
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
        self.test_ratio = test_ratio
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
        
        self.data_type_assigner = Data_type_assigner(self.raw_df, self.integer_columns,self.mixed_columns)
        
        self.null_value_transformer = Null_value_transformer()
        self.mixed_columns = self.null_value_transformer.fit(self.raw_df, self.categorical_columns, self.mixed_columns)
        self.raw_df = self.null_value_transformer.transform(self.raw_df)

        self.data_prep2 = DataPrep2(self.raw_df,self.categorical_columns,self.log_columns)
        self.prepared_data = self.data_prep2.preprocesses_transform(self.raw_df)

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


    def generate_samples(self,n=1000):
        
        sample_transformed = self.synthesizer.sample(n)#self.synthesizer.sample(n, column_index, column_value_index)
        sample_transformed = pd.DataFrame(sample_transformed, columns=self.prepared_data.columns)
        
        sample = self.data_prep2.preprocesses_inverse_transform(sample_transformed)
        sample = self.null_value_transformer.inverse_transform(sample)
        sample_with_data_types = self.data_type_assigner.assign(sample)
        
        return sample_with_data_types
