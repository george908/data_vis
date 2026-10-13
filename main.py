import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# get the data from the csv
data = pd.read_csv("farr.csv")

def draw_current_graph(year40, ax, name_of_graph):
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
    year40["deaths_without_?"] = pd.to_numeric(year40["deaths"], errors="coerce")
    
    # get the temperature reference
    temperature_reference = year40.iloc[0]["temperature_reference"]
    # get the mortality reference
    mortality_reference = year40.iloc[0]["mortality_reference"]
    
    # get the changes from the reference temperature and put them into an array
    temperature_change = []
    for index, row in year40.iterrows():
            temp = row["temperature_without_?"]
            if pd.notna(temp):
                change = temp - temperature_reference
            else:
                change = np.nan
            temperature_change.append(change)
    
    # get the changes from the reference mortality and put them into an array
    mortality_change = []
    for index, row in year40.iterrows():
            mortality = row["deaths_without_?"]
            if pd.notna(mortality):
                change = mortality - mortality_reference
            else:
                change = np.nan
            mortality_change.append(change)
    
    # put the temperatures into an array 
    temperature_array = year40["temperature_without_?"].tolist()
    # mortality into an array
    mortality_array = year40["deaths_without_?"].tolist()
    
    # store the angles where the temperature value is missing
    missing_temperature_angles = []
    
    # change the ? mark temperatures to the reference
    for week in range(number_of_weeks):
        if pd.isna(temperature_array[week]):
            temperature_array[week] = temperature_reference
            temperature_change[week] = 0
            missing_temperature_angles.append(angles_array[week])
    
    # store the angles where the mortality value is missing
    missing_mortality_angles = []
    
    # change the ? marks to the reference
    for week in range(number_of_weeks):
        if pd.isna(mortality_array[week]):
            mortality_array[week] = mortality_reference
            mortality_change[week] = 0
            missing_mortality_angles.append(angles_array[week])
    
    # add the temperature change 
    year40["temperature_change"] = temperature_change
    
    # add one to complete the circle
    temperature_array.append(temperature_array[0])
    
    # put the reference temperature into an array of the length of the year plus 1 to complete the circle
    temperature_reference_array = [temperature_reference] * (number_of_weeks + 1)
    
    # scale everything for the temperatures so that it looks better visually 
    temperature_scale = 10
    for week in range(len(temperature_array)):
        temperature_array[week] = temperature_array[week] * temperature_scale
        temperature_reference_array[week] = temperature_reference_array[week] * temperature_scale
    
    
    # add one to complete the circle
    mortality_array.append(mortality_array[0])
    
    # put the reference mortality into an array of the length of the year plus 1 to complete the circle
    mortality_reference_array = [mortality_reference] * (number_of_weeks + 1)
    
    # set the 0 degrees to the bottom of the chart 
    ax.set_theta_zero_location("S")
    # make it clockwise
    ax.set_theta_direction(-1)
    
    # make labels for only for every fourth week
    week_labels = []
    for week in range(1, number_of_weeks + 1):
        if week % 4 == 0:
            week_labels.append(str(week))
        else:
            week_labels.append("")
    
    # draw all of the radial lines 
    ax.set_xticks(angles_array[:-1])
    # only label every 4th radial line as it is too cluttered otherwise
    ax.set_xticklabels(week_labels, fontsize=8)
    # move the numbers closer so it looks better
    ax.tick_params(axis="x", pad=-5)
    
    # make the temperature changes the same length as the other arrays
    temperature_change_array = temperature_change.copy()
    temperature_change_array.append(temperature_change_array[0])
    
    # make the mortality changes the same length as the other arrays
    mortality_change_array = mortality_change.copy()
    mortality_change_array.append(mortality_change_array[0])
    
    # fill the space where the temperature is more than the reference 
    ax.fill_between(angles_array, temperature_reference_array, temperature_array, where=np.array(temperature_change_array) > 0, color="red",interpolate=True)
    # fill the space where the temperature is less than the reference 
    ax.fill_between(angles_array, temperature_reference_array, temperature_array, where=np.array(temperature_change_array) < 0, color="blue", interpolate=True)
    # fill the space where the mortality is more than the reference 
    ax.fill_between(angles_array, mortality_reference_array, mortality_array, where=np.array(mortality_change_array) > 0, color="red",interpolate=True)
    # fill the space where the mortality is less than the reference 
    ax.fill_between(angles_array, mortality_reference_array, mortality_array, where=np.array(mortality_change_array) < 0, color="blue", interpolate=True)
    
    # mark the weeks where the temperature data was missing
    for angle in missing_temperature_angles:
        # 10 points to make the lines smooth
        smooth_angles = []
        for num in range(10):
            smooth_angles.append(angle + (2*np.pi/number_of_weeks) * (num/9))
        ax.plot(smooth_angles, [temperature_reference * temperature_scale] * len(smooth_angles), color="purple")
    
    # mark the weeks where the mortality data was missing
    for angle in missing_mortality_angles:
        # 10 points to make the lines smooth
        smooth_angles = []
        for num in range(10):
            smooth_angles.append(angle + (2*np.pi/number_of_weeks) * (num/9))
        ax.plot(smooth_angles, [mortality_reference] * len(smooth_angles), color="purple")

    ax.set_title(name_of_graph)


# set the size of the page to the exact size of an A4 page and plot 12 graphs in rows of 4 and columns of 3
fig, axes = plt.subplots(4, 3, figsize=(8.27, 11.69), subplot_kw={"projection": "polar"})
# make it a 1D array so its easier 
axes = axes.flatten()

# loop through each year to pass it into the draw graph array 
for index, year in enumerate(range(1840, 1851)):
    year_info = data[data["year"] == year].copy()
    draw_current_graph(year_info, axes[index], str(year))


plt.tight_layout() 
plt.show()
