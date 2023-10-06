import csv

# Sample data
data = [
    ['E.ID', 'Employee Name'] + [f'Day {day}' for day in range(1, 32)],
    [''] + [''] + ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] * 6 + ['Monday'],  # This spreads out the days to fit under Day 1 to Day 31
    [0, 'John Smith'] + ['Morning', 'Evening', 'Night'] * 10 + ['Morning'],
    [1, 'Jane Doe'] + ['Night', 'Morning', 'Evening'] * 10 + ['Night'],
    [2, 'Alice Johnson'] + ['Evening', 'Night', 'Morning'] * 10 + ['Evening']
]

# Create and write to the CSV file
with open('sample.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("Sample CSV file 'sample.csv' created successfully.")
