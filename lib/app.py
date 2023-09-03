from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define the Restaurant model
class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    reviews = relationship('Review', back_populates='restaurant')
    customers = relationship('Customer', secondary='reviews', back_populates='restaurants')

# Define the Customer model
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reviews = relationship('Review', back_populates='customer')
    restaurants = relationship('Restaurant', secondary='reviews', back_populates='customers')

# Define the Review model
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

# Create a database engine and session
engine = create_engine('sqlite:///restaurant_reviews.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Object Relationship Method

# Review methods
def review_customer(review):
    return review.customer

def review_restaurant(review):
    return review.restaurant

# Restaurant methods
def restaurant_reviews(restaurant):
    return restaurant.reviews

def restaurant_customers(restaurant):
    return restaurant.customers

# Customer methods
def customer_reviews(customer):
    return customer.reviews

def customer_restaurants(customer):
    return customer.restaurants

# Aggregate and Relationship Methods

# Customer methods
def full_name(customer):
    return f'{customer.first_name} {customer.last_name}'

def favorite_restaurant(customer):
    max_rating = 0
    favorite = None

    for review in customer.reviews:
        if review.star_rating > max_rating:
            max_rating = review.star_rating
            favorite = review.restaurant

    return favorite

def add_review(customer, restaurant, rating):
    new_review = Review(star_rating=rating, restaurant=restaurant, customer=customer)
    session.add(new_review)
    session.commit()

def delete_reviews(customer, restaurant):
    session.query(Review).filter_by(customer=customer, restaurant=restaurant).delete()
    session.commit()

# Review methods
def full_review(review):
    return f'Review for {review.restaurant.name} by {review.customer.first_name} {review.customer.last_name}: {review.star_rating} stars.'

# Restaurant methods
def fanciest(cls):
    fanciest = session.query(cls).order_by(cls.price.desc()).first()
    return fanciest

def all_reviews(restaurant):
    review_strings = []
    for review in restaurant.reviews:
        review_strings.append(full_review(review))
    return review_strings

if __name__ == "__main__":
    restaurant1 = Restaurant(name='Restaurant 1', price=3)
    customer1 = Customer(first_name='John', last_name='Doe')
    customer2 = Customer(first_name='Jane', last_name='Smith')

    session.add_all([restaurant1, customer1, customer2])
    session.commit()

    add_review(customer1, restaurant1, 5)
    add_review(customer2, restaurant1, 4)

    print(f'Full Name: {full_name(customer1)}')
    print(f'Favorite Restaurant: {favorite_restaurant(customer1).name}')

    print(f'Customer 1 Reviews: {customer_reviews(customer1)}')
    print(f'Restaurant 1 Customers: {restaurant_customers(restaurant1)}')

    print(f'Restaurant 1 Fanciest: {fanciest(Restaurant).name}')
    print(f'Restaurant 1 Reviews: {all_reviews(restaurant1)}')
