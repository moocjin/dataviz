# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:57:26 2016

"""

import pandas
import seaborn
import matplotlib.pyplot as plt

#made display a bit wider than I'm getting as default
pandas.set_option('display.width', 500)

data = pandas.read_csv('gapminder.csv', low_memory=False)

#convert to numeric
data['suicideper100th']= data['suicideper100th'].convert_objects(convert_numeric=True)
data['employrate']= data['employrate'].convert_objects(convert_numeric=True)
data['femaleemployrate']= data['femaleemployrate'].convert_objects(convert_numeric=True)


print "observations"
print (len(data)) #number of observations (rows)
print "columns"
print (len(data.columns)) # number of variables (columns)

#remove rows with missing data for suicide/employment/female-employment rates
sub1=data[(data['suicideper100th'].notnull()) & (data['employrate'].notnull()) & (data['femaleemployrate'].notnull())]

#make a copy of my new subsetted data
sub2 = sub1.copy()

print "after removing nulls, rows:"
print len(sub2)





#secondary variable showing female employment rate as a % of overall employment rate
#we multiple by 100 to match the employment rates that are also shown *100
sub2['relative_female']= sub2['femaleemployrate']/sub2['employrate'] * 100

print "range of data:"
print "max suicides per 100,000:", sub2['suicideper100th'].max()
print "min suicides per 100,000:", sub2['suicideper100th'].min()
print "max employment rate:", sub2['employrate'].max()
print "min employment rate:", sub2['employrate'].min()
print "max female employment rate:", sub2['femaleemployrate'].max()
print "min female employment rate:", sub2['femaleemployrate'].min()
print "max relative female employment rate:", sub2['relative_female'].max()
print "min relative female employment rate:", sub2['relative_female'].min()




#counts and percentages (i.e. frequency distributions) for each variable
print "counts for 2005 suicides per 100,000, age adjusted"
c1 = sub2['suicideper100th'].value_counts(sort=False, dropna=False).sort_index()
#print (c1)

print "percentages for 2005 suicides per 100,000, age adjusted"
p1 = sub2['suicideper100th'].value_counts(sort=False, dropna=False, normalize=True).sort_index()
#print (p1)

print "counts for 2007 employment rates above age 15"
c2 = sub2['employrate'].value_counts(sort=False, dropna=False).sort_index()
#print(c2)

print "percentages for 2007 employment rates above age 15"
p2 = sub2['employrate'].value_counts(sort=False, dropna=False, normalize=True).sort_index()
#print (p2)

print "counts for 2007 employment rates for females above age 15"
c3 = sub2['femaleemployrate'].value_counts(sort=False, dropna=False).sort_index()
#print(c3)

print "percentages for 2007 employment rates for females above age 15"
p3 = sub2['femaleemployrate'].value_counts(sort=False, dropna=False, normalize=True).sort_index()
#print (p3)

print "counts for relative female employment rates"
c3 = sub2['relative_female'].value_counts(sort=False, dropna=False).sort_index()
#print(c3)

print "percentages relative female employment rates"
p3 = sub2['relative_female'].value_counts(sort=False, dropna=False, normalize=True).sort_index()
#print (p3)

# categorize quantitative variable based on customized splits using cut function
# splits into 5 groups - remember that Python starts counting from 0, not 1
sub2['suicide_bins'] = pandas.cut(sub2.suicideper100th, [0,5,10,15,20,25,30,35,40])
b1 = sub2['suicide_bins'].value_counts(sort=False, dropna=True)
print "binned suicide frequencies per 100,000 population"
print(b1)

q1 = sub2['suicide_bins'].value_counts(sort=False, dropna=True,normalize=True)
print "fraction of countries falling into into each suicide rate bin"
print q1

#crosstabs evaluating which suicide rates were put into which bin
#print (pandas.crosstab(sub2['suicideper100th'], sub2['suicide_bins']))

#now categorize the employment rates
sub2['emprate_bins'] = pandas.cut(sub2.employrate, [0,10,20,30,40,50,60,70,80,90,100])
b2 = sub2['emprate_bins'].value_counts(sort=False, dropna=True)
print "binned employment rates"
print(b2)

#crosstabs 
#print (pandas.crosstab(sub2['employrate'], sub2['emprate_bins']))

q2 = sub2['emprate_bins'].value_counts(sort=False, dropna=True,normalize=True)
print "fraction of countries falling into into each employment rate bin"
print q2

#now categorize the female employment rates
sub2['female_employrate_bins'] = pandas.cut(sub2.femaleemployrate, [0,10,20,30,40,50,60,70,80,90,100])
b3 = sub2['female_employrate_bins'].value_counts(sort=False, dropna=True)
print "binned female employment rates"
print(b3)

#crosstabs 
#print (pandas.crosstab(sub2['femaleemployrate'], sub2['female_employrate_bins']))

q3 = sub2['female_employrate_bins'].value_counts(sort=False, dropna=True,normalize=True)
print "fraction of countries falling into into each female employment rate bin"
print q3


#now categorize the ratio of female employment rates to overall employment rates
#note that this can go over 100% (if female employment rates are higher than overall rates)
sub2['relative_female_bins'] = pandas.cut(sub2.relative_female, [0,10,20,30,40,50,60,70,80,90,100,110])
b4 = sub2['relative_female_bins'].value_counts(sort=False, dropna=True)
print "binned relative female employment rates"
print(b4)

#crosstabs 
#print (pandas.crosstab(sub2['relative_female'], sub2['relative_female_bins']))

q4 = sub2['relative_female_bins'].value_counts(sort=False, dropna=True,normalize=True)
print "fraction of countries falling into into each relative female employment rate bin"
print q4

# bivariate scatterplots:  Q->Q
chart1, ax1 = plt.subplots()
scat1 = seaborn.regplot(x="employrate", y="suicideper100th", fit_reg=True, data=sub2, ax=ax1)
plt.xlabel('Employment Rate')
plt.ylabel('Suicide per 100,000 population')
plt.title('Scatterplot for the Association Between Employment Rate and Suicides per 100,000 Population')


chart2, ax2 = plt.subplots()
scat2 = seaborn.regplot(x="femaleemployrate", y="suicideper100th", fit_reg=True, data=sub2, ax=ax2)
plt.xlabel('Female Employment Rate')
plt.ylabel('Suicide per 100,000 population')
plt.title('Scatterplot for the Association Between Female Employment Rate and Suicides per 100,000 Population')


chart3, ax3 = plt.subplots()
scat3 = seaborn.regplot(x="relative_female", y="suicideper100th", fit_reg=True, data=sub2, ax=ax3)
plt.xlabel('Relative Female Employment Rate')
plt.ylabel('Suicide per 100,000 population')
plt.title('Scatterplot for the Association Between Relative Female Employment Rate and Suiciides per 100,000 Population')

#Univariate histogram for quantitative variables:

chart4, ax4 = plt.subplots()
seaborn.distplot(sub2["suicideper100th"].dropna(), kde=False, ax=ax4);
plt.xlabel('Suicides per 100,000 population')
plt.title('Suicides per 100,000 population')

chart5, ax5 = plt.subplots()
seaborn.distplot(sub2["employrate"].dropna(), kde=False, ax=ax5);
plt.xlabel('Employment rate')
plt.title('Employment Rate')

chart6, ax6 = plt.subplots()
seaborn.distplot(sub2["femaleemployrate"].dropna(), kde=False, ax=ax6);
plt.xlabel('Female employment rate')
plt.title('Female Employment Rate')

chart7, ax7 = plt.subplots()
seaborn.distplot(sub2["relative_female"].dropna(), kde=False, ax=ax7);
plt.xlabel('Relative female employment rate')
plt.title('Relative Female Employment Rate')


