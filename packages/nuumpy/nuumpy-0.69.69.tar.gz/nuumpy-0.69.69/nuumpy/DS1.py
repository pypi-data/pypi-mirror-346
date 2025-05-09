def DS1():
    print("""

#!/usr/bin/env python
# coding: utf-8

# # Data Wrangling - I
# 
# ## Aim
# Perform the following operations using Python on any open source dataset (e.g., data.csv):
# 
# 1. **Import all the required Python libraries.**
# 
# 2. **Locate an open source dataset from the web**  
#    Example source: [https://www.kaggle.com](https://www.kaggle.com)  
#    - Provide a clear description of the dataset.  
#    - Include the URL of the website.
# 
# 3. **Load the dataset into a Pandas DataFrame.**
# 
# 4. **Data Preprocessing**  
#    - Check for missing values using `isnull()`.  
#    - Use `describe()` to get initial statistics.  
#    - Provide variable descriptions, types of variables, etc.  
#    - Check the dimensions of the DataFrame using `.shape`.
# 
# 5. **Data Formatting and Normalization**  
#    - Summarize types of variables by checking their data types using `dtypes`.  
#    - Apply type conversions where necessary.
# 
# 6. **Convert categorical variables into quantitative variables**  
#    - Use encoding methods such as one-hot encoding or label encoding.
# 

# In[1]:


#Import required libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv("titanic_dataset.csv")
df


# In[3]:


df.head()


# In[4]:


df.info()


# In[5]:


df.isnull().sum()


# In[6]:


print("\nStatistical Summary:")
df.describe()


# In[7]:


print("\nData Types of Each Column")
df.dtypes


# In[8]:


df['Sex'] = df['Sex'].astype('category')
df['Embarked'] = df['Embarked'].astype('category')


# In[9]:


df.dtypes


# In[10]:


df['Sex'] = df['Sex'].cat.codes


# In[11]:


df.dtypes


# In[12]:


df.head()


# In[13]:


df['Embarked'] = df['Embarked'].cat.codes


# In[14]:


df.dtypes


# In[15]:


df.head()


# In[17]:


sns.heatmap(df.isnull(), cmap='viridis')
plt.title('Missing Values Heatmap')
plt.show()


# In[ ]:


df.head()

""")
    
DS1()