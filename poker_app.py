
import streamlit as st
## import matplotlib.pyplot as plt
import pandas as pd

# Function to calculate employee cost
def calculate_employee_cost(hours, employee_pay_per_hour, table_close_time, initial_employees):
    employee_cost = []
    current_employees = initial_employees
    for hour in hours:
        employee_cost.append(current_employees * employee_pay_per_hour)
        if hour == table_close_time[0] or hour == table_close_time[1]:
            current_employees -= 1
    return [sum(employee_cost[:hour]) for hour in hours]

# Function to calculate rake
def calculate_rake(player_count, buyin_rake, reentry_rake, entrance_fee, entrance_fee_percent, min_reentries, max_reentries):
    total_rake_min = player_count * buyin_rake + min_reentries * reentry_rake
    total_rake_max = player_count * buyin_rake + max_reentries * reentry_rake
    total_entrance_fee = player_count * entrance_fee_percent * entrance_fee
    return (total_rake_min + total_entrance_fee, total_rake_max + total_entrance_fee)

# Function to plot financials
#def plot_financials(hours, rake_min, rake_max, employee_cost):
#    fig, ax = plt.subplots(figsize=(12, 6))
#    ax.plot(hours, rake_min, label='Total Rake (Min reentries + Entrance Fee)', linestyle='--')
#    ax.plot(hours, rake_max, label='Total Rake (Max reentries + Entrance Fee)', linestyle='--')
#    ax.plot(hours, employee_cost, label='Total Employee Cost (Adjusted)', color='red')
#    ax.fill_between(hours, rake_min, rake_max, color='lightgrey', alpha=0.5)
#    ax.set_xlabel('Hours')
#    ax.set_ylabel('Kr')
#    ax.set_title('Poker Tournament Financials (Adjusted for Table Closures, Reentry Fee, and Entrance Fee)')
#    ax.legend()
#    ax.grid(True)
#    st.pyplot(fig)

# Streamlit web app
st.title('Poker Tournament Financials')

# Acknowledgment
st.write("### Created by Frederik-Emil Jensen... Casino Marienlyst")

# Sliders for user input
employee_pay_per_hour = st.slider('Employee Pay per Hour (Kr)', 200, 300, 200)
initial_employees = st.slider('Initial Number of Employees', 1, 10, 5)
table_close_time = st.slider('Table Close Time (Hours)', 1, 8, (3, 6))
player_count = st.slider('Number of Players', 10, 50, 30)
buyin_rake = st.slider('Rake for Buy-in (Kr)', 0, 250, 200)
reentry_rake = st.slider('Rake for Reentry (Kr)', 0, 200, 100)
entrance_fee_percent = st.slider('Percentage of Players Paying Entrance Fee', 0.0, 1.0, 0.8)
min_reentries = st.slider('Minimum Reentries', 0, 100, 10)
max_reentries = st.slider('Maximum Reentries', 0, 100, 20)
entrance_fee = 70  # Fixed entrance fee

# Parameters
hours = list(range(1, 9))

# Calculations
employee_cost = calculate_employee_cost(hours, employee_pay_per_hour, table_close_time, initial_employees)
total_rake_min, total_rake_max = calculate_rake(player_count, buyin_rake, reentry_rake, entrance_fee, entrance_fee_percent, min_reentries, max_reentries)
total_rake_min_list = [total_rake_min] * len(hours)
total_rake_max_list = [total_rake_max] * len(hours)

# Plotting
plot_financials(hours, total_rake_min_list, total_rake_max_list, employee_cost)

# Profit calculations
total_profit_min = [rake - cost for rake, cost in zip(total_rake_min_list, employee_cost)] 
total_profit_max = [rake - cost for rake, cost in zip(total_rake_max_list, employee_cost)]

# Create DataFrame for display
data = {
    "Hour": hours,
    "Total Profit (Min reentries + Entrance Fee)": total_profit_min,
    "Total Profit (Max reentries + Entrance Fee)": total_profit_max
}
profit_df = pd.DataFrame(data)

# Display DataFrame
st.subheader('Profit Data')
st.dataframe(profit_df)
