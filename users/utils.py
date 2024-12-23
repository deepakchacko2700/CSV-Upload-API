import csv
from faker import Faker

# Initialize the Faker object
fake = Faker()

file_name = 'user_data.csv'

# Create and open the CSV file in write mode
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['name', 'email', 'age'])
    
  
    for _ in range(1000):
        # Generate fake data
        name = fake.name()
        age = fake.random_int(min=0, max=120)
        email = fake.email()
        
        # Write the record to the CSV file
        writer.writerow([name, email, age])

print(f'{file_name} has been created with 1000 records.')
