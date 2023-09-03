from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, Customer, Review

# Create a database engine and session
engine = create_engine('sqlite:///restaurant_reviews.db')
Session = sessionmaker(bind=engine)
session = Session()

# Insert sample data for restaurants
restaurant1 = Restaurant(name='Restaurant 1', price=3)
restaurant2 = Restaurant(name='Restaurant 2', price=2)
session.add_all([restaurant1, restaurant2])

# Insert sample data for customers
customer1 = Customer(first_name='John', last_name='Doe')
customer2 = Customer(first_name='Jane', last_name='Smith')
session.add_all([customer1, customer2])

# Insert sample data for reviews
review1 = Review(star_rating=4, restaurant=restaurant1, customer=customer1)
review2 = Review(star_rating=5, restaurant=restaurant1, customer=customer2)
review3 = Review(star_rating=3, restaurant=restaurant2, customer=customer1)
session.add_all([review1, review2, review3])

# Commit the changes to the database
session.commit()

# Close the session
session.close()
