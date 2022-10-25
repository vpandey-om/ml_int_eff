import os
import pandas as pd
cur_dir = os.path.dirname(__file__)

df_full=pd.read_excel(os.path.join(cur_dir,'Data','blood_screen_full_set_data.xlsx'))
df_pheno=pd.read_excel(os.path.join(cur_dir,'Data','blood_screen_phenotype.xlsx'))
