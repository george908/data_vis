import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# get the data from the csv
data = pd.read_csv("farr.csv")

# get the data per year 
year40 = data[data["year"] == 1840].copy()
# get the amount of weeks 
number_of_weeks = len(year40)
# make the array of angles between the weeks
angles_array = []
for week in range(number_of_weeks):
    angle = 2 * np.pi * (week / number_of_weeks) 
    angles_array.append(angle)
# add one to complete the circle
angles_array.append(angles_array[0] + 2 * np.pi)

# take out all of the ? marks
year40["temperature_without_?"] = pd.to_numeric(year40["mean_temperature"], errors="coerce")

# get the temperature reference
temperature_reference = year40.iloc[0]["temperature_reference"]

# get the changes from the reference temperature and put them into an array
temperature_change = []
for index, row in year40.iterrows():
        temp = row["temperature_without_?"]
        if pd.notna(temp):
            change = temp - temperature_reference
        else:
            change = np.nan
        temperature_change.append(change)

# put the temperatures into an array 
temperature_array = year40["temperature_without_?"].tolist()

# store the angles where the temperature value is missing
missing_temperature_angles = []

# change the ? mark temperatures to the reference
for week in range(number_of_weeks):
    if pd.isna(temperature_array[week]):
        temperature_array[week] = temperature_reference
        temperature_change[week] = 0
        missing_temperature_angles.append(angles_array[week])

# add the temperature change 
year40["temperature_change"] = temperature_change

# add one to complete the circle
temperature_array.append(temperature_array[0])

# put the reference temperature into an array of the length of the year plus 1 to complete the circle
temperature_reference_array = [temperature_reference] * (number_of_weeks + 1)

# make a circlular graph
fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
# set the 0 degrees to the bottom of the chart 
ax.set_theta_zero_location("S")
# make it clockwise
ax.set_theta_direction(-1)
# plot it out 
ax.plot(angles_array, temperature_reference_array)

# plot the temperature using the angles 
ax.plot(angles_array, temperature_array)

# make the temperature changes the same length as the other arrays
temperature_change_array = temperature_change.copy()
temperature_change_array.append(temperature_change_array[0])

# fill the space where the temperature is more than the reference 
ax.fill_between(angles_array, temperature_reference_array, temperature_array, where=np.array(temperature_change_array) > 0, color="red",interpolate=True)
# fill the space where the temperature is less than the reference 
ax.fill_between(angles_array, temperature_reference_array, temperature_array, where=np.array(temperature_change_array) < 0, color="blue", interpolate=True)

# mark the weeks where the temperature data was missing
for angle in missing_temperature_angles:
    ax.scatter(angle, temperature_reference, color="purple")

plt.show()
