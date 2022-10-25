import sys,os
from scipy.stats import gmean
import numpy as np
import pandas as pd

# setting path
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from readData import df_full, df_pheno


genes=[]
cloneids=[]
integration_effciencies=[]
left_arm_length_arr=[]
right_arm_length_arr=[]
phenotypes=[]
rgr=[]
rgr_low=[]
rgr_high=[]


for k,locidx in df_full.groupby(['gene','cloneid']).indices.items():

    eff1=df_full.loc[locidx,'normd6toinputA'].to_list()
    eff2=df_full.loc[locidx,'normd6toinputB'].to_list()
    eff3=df_full.loc[locidx,'normd6toinputC'].to_list()
    eff4=df_full.loc[locidx,'normd6toinputD'].to_list()
    left_length=df_full.loc[locidx,'left_arm_length'].to_list()
    right_length=df_full.loc[locidx,'right_arm_length'].to_list()
    if (len(set(left_length))==1) and (len(set(right_length))==1):
        left_arm_length_arr.append(left_length[0])
        right_arm_length_arr.append(right_length[0])
    else:
        import pdb; pdb.set_trace()

    alleff=[eff1,eff2,eff3,eff4]
    flat_eff = [item for sublist in alleff for item in sublist]
    values = np.array(flat_eff)
    values = values[~np.isnan(values)]
    integ_eff=gmean(values)
    integration_effciencies.append(integ_eff)
    genes.append(k[0])
    cloneids.append(k[1])
    tmp=df_pheno[df_pheno['P. berghei previous ID']==k[0]]
    if not tmp.empty:
        rgr_low.append(tmp['RGR CI low'].to_list()[0])
        rgr.append(tmp['Relative growth rate'].to_list()[0])
        rgr_high.append(tmp['RGR CI high'].to_list()[0])
        phenotypes.append(tmp['Phenotype'].to_list()[0])
    else:
        rgr_low.append(np.nan)
        rgr.append(np.nan)
        rgr_high.append(np.nan)
        phenotypes.append('NA')


df=pd.DataFrame()
df['gene']=genes
df['cloneids']=cloneids
df['integration_effciencies']=integration_effciencies
df['left_arm_length']=left_arm_length_arr
df['right_arm_length']=right_arm_length_arr
df['Relative growth rate']=rgr
df['RGR CI high']=rgr_high
df['RGR CI low']=rgr_low
df['Phenotype']=phenotypes

df.to_excel('Intgeration_efficiencies.xlsx')
