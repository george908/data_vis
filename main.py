import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

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
    
    # make labels for only for every four weeks
    week_labels = []
    for week in range(1, number_of_weeks + 1):
        if week == 1:
            week_labels.append("Week 1")
        elif (week - 1) % 4 == 0:
            week_labels.append(str(week))
        else:
            week_labels.append("")
    
    # draw all of the radial lines 
    ax.set_xticks(angles_array[:-1])
    # only label every 4th radial line as it is too cluttered otherwise
    ax.set_xticklabels(week_labels, fontsize=8)
    # move the numbers closer so it looks better
    ax.tick_params(axis="x", pad=-5)
    # take out the numbers between the inner circles
    ax.set_yticklabels([])
    
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
    ax.fill_between(angles_array, mortality_reference_array, mortality_array, where=np.array(mortality_change_array) > 0, color="grey",interpolate=True)
    # fill the space where the mortality is less than the reference 
    ax.fill_between(angles_array, mortality_reference_array, mortality_array, where=np.array(mortality_change_array) < 0, color="gold", interpolate=True)
    # put a black dashed line for the temperature reference value that year
    ax.plot(angles_array, temperature_reference_array, color="black", linestyle="dashed", linewidth=0.75)
    # put a black dashed line for the mortality reference value that year
    ax.plot(angles_array, mortality_reference_array, color="black", linestyle="dashed", linewidth=0.75)
    
    # mark the weeks where the temperature data was missing
    for angle in missing_temperature_angles:
        # 10 points to make the lines smooth
        smooth_angles = []
        for num in range(10):
            smooth_angles.append(angle + (2*np.pi/number_of_weeks) * (num/9))
        ax.plot(smooth_angles, [temperature_reference * temperature_scale] * len(smooth_angles), color="#BF40BF", linewidth=3)
    
    # mark the weeks where the mortality data was missing
    for angle in missing_mortality_angles:
        # 10 points to make the lines smooth
        smooth_angles = []
        for num in range(10):
            smooth_angles.append(angle + (2*np.pi/number_of_weeks) * (num/9))
        ax.plot(smooth_angles, [mortality_reference] * len(smooth_angles), color="#BF40BF", linewidth=3)

    ax.set_title(name_of_graph)


# set the size of the page to the exact size of an A4 page and plot 12 graphs in rows of 4 and columns of 3
fig, axes = plt.subplots(4, 3, figsize=(8.27, 11.69), subplot_kw={"projection": "polar"})
# make it a 1D array so its easier 
axes = axes.flatten()

# loop through each year to pass it into the draw graph array 
for index, year in enumerate(range(1840, 1851)):
    year_info = data[data["year"] == year].copy()
    draw_current_graph(year_info, axes[index], "Year " + str(year))

# columns to get the average of for the last graph 
columns_to_get_average = ["mean_temperature", "deaths", "temperature_reference", "mortality_reference"]

# get rid of the ? marks
for column in columns_to_get_average:
    data[column] = pd.to_numeric(data[column], errors="coerce")
# get the average for each week
average_rows = []
for week in range(1, 53):
    week_info = data[data["week"] == week]
    average_week = week_info[columns_to_get_average].mean()
    average_week["week"] = week
    average_rows.append(average_week)

# turn the averages into a dataframe so that it can be input the same way as the single years
average_data = pd.DataFrame(average_rows)
# call the function to draw the average graph
draw_current_graph(average_data, axes[11], "The average of Years 1840-1850")

# leave 10% of the page for the title and 10% of the page for the legend 
plt.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.16, hspace=0.35, wspace=0.20)
# give the page a title in bold that matches the original title 
fig.suptitle("Temperature and Mortality of London (1840–1850)", fontsize=17, fontweight="bold",y=0.97)

# make an array of colour labels for the legend to show what the different colours in the charts mean 
coloured_legend_labels = [
    Patch(color="red", label="Temperature above reference"),
    Patch(color="blue", label="Temperature below reference"),
    Patch(color="grey", label="Deaths above reference"),
    Patch(color="gold", label="Deaths below reference"),
    plt.Line2D([], [], color="black", linestyle="--", label="Reference values"),
    Patch(color="#BF40BF", label="Missing data")
]
# plot the colur labels of the legend on the right side of the legend 
fig.legend(handles=coloured_legend_labels, loc="center right", bbox_to_anchor=(0.98, 0.08), ncol=1, frameon=False, fontsize=9)

fig.text(0.06, 0.14,
    "Each circle represents the 52 weeks of the year starting from the bottom and moving\n" 
    "clockwise. The inner ring shows temperature and the outer ring shows deaths relative to\n"
    "their reference values with the temperature being measured in Fahrenheit and deaths\n"
    "measured in amount per week. The colours show if the values are above or below their\n"
    "reference values. Thicker coloured areas mean larger differences from the reference value.\n"
    "The temperature values and their reference values are multiplied by 10 to make the inner\n"
    "ring easier to see and analyse. Each year has its own scale to make the patterns visually\n"
    "easier to see, so comparisons should be made within each chart and not between different\n"
    "years. The last circle shows the weekly averages over the years 1840-1850 to compare the\n"
    "overall patterns. The reference levels for the temperature and deaths is marked with a\n"
    "dashed line and weeks with data missing are marked in purple at the reference level, but\n"
    "coloured areas may still appear above or below due to interpolation.",
    ha="left",
    va="top",
    fontsize=8
)

plt.savefig("final_image.pdf") # PDF to see how the final version of it would work 
plt.show()
