"""Simple functions to help parse and plot Garmin Fit data"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fitparse
import copy
from datetime import datetime


def GetFitDf(filepath):
	"""Parse a Garmin Fit file and  return a DataFrame
	
	Args:
		filepath: String. Path and file corresponding with a Garmin Fit file
		
	Returns:
		df: DataFrame. DataFrame with corresponding Garmin Fit data
	"""
	fitfile = fitparse.FitFile(filepath)
	
	df = pd.DataFrame({})
	
	for idx, record in enumerate(fitfile.get_messages('record')):
		
		# Go through all the data entries in this record
		for record_data in record:
			key = record_data.name
			key = key.replace('_', ' ')
			val = record_data.value
			unit = record_data.units
			
			key = '%s [%s]' % (key.title(), unit)
			
			df.loc[idx, key] = val
	
	return df


def PlotFitData(df, x_var, y_var):
	"""Plot Garmin Fit data

	Args:
		df: DataFrame. Dataframe from GetFitDf
		x_var: String. String corresponding with column in df to plot on x-axis
		y_var: String. String corresponding with column in df to plot on y-axis
	"""
	x = df[x_var].values
	y = df[y_var].values
	
	dates = df['Timestamp [None]'].values
	dates = [datetime.fromtimestamp(x.astype(datetime) / 1e9).strftime('%m/%d/%Y') for x in dates]
	date = dates[0]
	
	plt.plot(x, y, markersize=0, linewidth=1, label=date)
	plt.grid(True)
	plt.xlabel('%s' % x_var, fontsize=14)
	plt.ylabel('%s' % y_var, fontsize=14)
	plt.title('%s Vs %s' % (y_var, x_var), fontsize=18)
	plt.legend(loc='best', fontsize=18)
	
	
def MakeConversions(df):
	"""Make common conversions to Garmin Fit DataFrame

	Args:
		df: DataFrame. Dataframe from GetFitDf
	"""
	# Conversions
	m_to_miles = 0.000621371
	m_to_feet = 3.28084
	
	df2 = copy.deepcopy(df)
	
	for col in list(df):
		if '[m]' in col:
			new_col = col.replace('[m]', '[miles]')
			df2[new_col] = df[col] * m_to_miles
		if '[m]' in col:
			new_col = col.replace('[m]', '[ft]')
			df2[new_col] = df[col] * m_to_feet
		if '[m/s]' in col:
			new_col = col.replace('[m/s]', '[mph]')
			df2[new_col] = df[col] * m_to_miles * 60 * 60
		
	return df2
	
