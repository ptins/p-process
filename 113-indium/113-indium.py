
# coding: utf-8

# ### read in kadonis data

# In[1]:


import os, glob
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['lines.linewidth'] = .85
plt.style.use('seaborn-whitegrid')
plt.rcParams["figure.figsize"] = (20,10)


# In[2]:


ag_kad_file = './kad_files/113In-ag-YGO09'
an_kad_file = './kad_files/113In-an-YGO09'


# In[3]:


def get_kadonis_df(filename):
    # open kadonis file
    f = open(filename,'r')
    # read lines and close
    lines = f.read().splitlines()
    f.close()
    # strip out lines we want
    lines_imp = lines[19:]
    x = [line.split() for line in lines_imp]
    # get column labels, column data
    headers = x[0]
    data = x[2:]
    # convert to df
    df = pd.DataFrame(data, columns=headers)
    # make numeric
    ene  = pd.to_numeric(df['E(c.m.)'])
    cs_true = pd.to_numeric(df['CS'])
    cs_err  = pd.to_numeric(df['ErrCS'])
    # new df  
    df_new  = pd.DataFrame([ene, cs_true, cs_err]).transpose()
    df_new.columns = ['ene', 'cs_kadonis', 'cs_err']
    df_new = df_new.sort_values('ene', ascending=True)
    return(df_new)


# In[4]:


ag_kad_df = get_kadonis_df(ag_kad_file)
an_kad_df = get_kadonis_df(an_kad_file)
print(ag_kad_df)
print(an_kad_df)


# ### start talys stuff

# In[5]:


# general parameters
symbol = 'in'
mass = 113
z = 49


# In[6]:


# write ag_energies file
ene_kad = []
[ene_kad.append(round(ene,4)) for ene in ag_kad_df['ene']]
[ene_kad.append(round(ene,4)) for ene in an_kad_df['ene']]
ene_kad = sorted(list(set(ene_kad)))
# ene_kad


# In[7]:


f = open('energies','w')
[f.write(str(ene)+'\n') for ene in ene_kad]
f.close()


# In[8]:


def get_talys_df(filename):
    f = open(filename,'r')
    # read lines and close
    lines = f.read().splitlines()
    f.close()
    # strip out lines we want
    lines_imp = lines[5:]
    x = [line.strip().split(' ') for line in lines_imp]
    df = pd.DataFrame(x)
    df.columns = ['ene','cs']
    # make numeric 
    df  = pd.DataFrame([pd.to_numeric(df['ene']),
                        # convert millibarns
                        pd.to_numeric(df['cs'])/1000]).transpose()
    return(df)


# In[9]:


# specify files to keep (still needs work)
ag_talys_file = 'rp0'+str(z+2)+str(mass+4)+'.tot'
an_talys_file = 'rp0'+str(z+2)+str(mass+3)+'.tot'


# In[10]:


# ldmodel = [1,2,3,4,5,6]
# strength = [1,2,3,4,5,6,7,8]
# alphaomp = [1,2,3,4,5,6,7,8]
# jlmomp = ['y','n']
ldmodel = [1,2]
strength = [1,2]
alphaomp = [1,2]
jlmomp = ['y','n']

ag_talys_all_df = pd.DataFrame(ene_kad)
an_talys_all_df = pd.DataFrame(ene_kad)


# In[31]:


col_names = ['ene']

# for tracking purposes
total_iter = len(ldmodel)*len(strength)*len(alphaomp)*len(jlmomp)
current_iter = 1

for l in ldmodel:
    for s in strength:
        for a in alphaomp:
            for j in jlmomp:
                
                # make column name
                col_name = 'l'+str(l)+'s'+str(s)+'a'+str(a)+'j'+j
                col_names.append(col_name)
                
                print('({}/{})\t\tRunning {}...'.format(current_iter,total_iter,col_name))
                
                # write input file contents
                top = 'projectile a\nelement '+symbol+'\nmass '+str(mass)+'\nenergy energies\n'
                mid = 'ldmodel '+str(l)+'\nstrength '+str(s)+'\nalphaomp '+str(a)+'\njlmomp '+j+'\n'
                bottom = 'xseps 1.e-35\npopeps 1.e-35\ntranseps 1.e-35\ncbreak p 0.\ncbreak n 0.\ncstrip p 0.\ncstrip n 0.\ncknock p 0.\ncknock n 0.\ngnorm 1'
                
                # actually write input file
                f = open('input', 'w')
                f.write(top+mid+bottom)
                f.close()
                
                # run talys
                get_ipython().system('talys <input> output')
                 
                # concatenate
                ag_talys_all_df = pd.concat([ag_talys_all_df, get_talys_df(ag_talys_file)['cs']], axis=1)
                an_talys_all_df = pd.concat([an_talys_all_df, get_talys_df(an_talys_file)['cs']], axis=1)
                
                # update iter count
                current_iter = current_iter + 1


# In[29]:


# clean file system
keeping = [ag_talys_file, an_talys_file, 'output', 'total.tot', '113-indium.ipynb','113-indium.py']
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if(f not in keeping):
        os.remove(f)
print('File system clean.')


# In[13]:


ag_talys_all_df.columns = col_names
an_talys_all_df.columns = col_names


# In[14]:


# merge talys with kadonis
ag_mega_df = pd.merge_asof(ag_talys_all_df, ag_kad_df).dropna().set_index('ene')
an_mega_df = pd.merge_asof(an_talys_all_df, an_kad_df).dropna().set_index('ene')


# ## RMSE

# In[15]:


def rmse(predictions, targets):
    return np.sqrt(((predictions - targets)**2).mean())


# In[22]:


def lowest_rmse(df):
    rmse_vals = []
    for col in df.drop('cs_err',axis=1):
        predictions = df[col].values
        targets = df['cs_err']
        rmse_vals.append(rmse(predictions,targets))
    lowest_rmse = df.columns[rmse_vals.index(min(rmse_vals))]
    ld = lowest_rmse[1]
    st = lowest_rmse[3]
    al = lowest_rmse[5]
    jl = lowest_rmse[7]
    return ld, st, al, jl


# In[25]:


print('Alpha-Gamma Parameters: {}'.format(lowest_rmse(ag_mega_df)))
print('Alpha-N Parameters: {}'.format(lowest_rmse(an_mega_df)))


# # Plotting

# ## Alpha-Gamma

# In[21]:


# plot data
ag_mega_df.drop(['cs_kadonis','cs_err'], axis=1).plot(logy=True)
plt.errorbar(ag_mega_df.index, ag_mega_df['cs_kadonis'], yerr=ag_mega_df['cs_err'])

# plot styling
plt.title('Alpha-Gamma')
plt.xlabel('Energy (MeV)')
plt.ylabel('Cross Section (millibarns)')


# ## Alpha-N

# In[20]:


# plot data
an_mega_df.drop(['cs_kadonis','cs_err'], axis=1).plot(logy=True)
plt.errorbar(an_mega_df.index, an_mega_df['cs_kadonis'], yerr=an_mega_df['cs_err'])

# plot styling
plt.title('Alpha-N')
plt.xlabel('Energy (MeV)')
plt.ylabel('Cross Section (millibarns)')

