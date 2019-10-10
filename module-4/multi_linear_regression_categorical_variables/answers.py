# For income ~ years of education + seniority
X = df_income[['Education', 'Seniority']].values
y = df_income['Income']
X = sm.add_constant(X)

model = sm.OLS(y, X, hasconst=True)
res = model.fit()

res.summary()

# For simple linear regression

X = df_income.Seniority.values
y = df_income.Income.values
X = sm.add_constant(X)
mod = sm.OLS(y, X, hasconst=True)
res = mod.fit()
res.summary()

## Drop the car name as it just have the names of the cars
data.drop(columns=['car name'], inplace=True)

## Finally we get categorical variables as columns - notice that we drop one entry for each category
new_data = pd.get_dummies(data, columns=['cylinders',
                                         'origin'], drop_first=True)

new_data.columns
