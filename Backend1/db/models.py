"""
This module defines the SQLAlchemy ORM models for the Mentormate project.
It sets up the database schema by defining the structure of tables and their relationships.
The module uses SQLAlchemy's ORM features to map Python classes to database tables,
establish relationships between them, and handle data interactions.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# Create a base class for declarative class definitions.
# All models will inherit from this Base class to use SQLAlchemy's ORM features.
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    # Define the columns for the 'users' table.
    id = Column(Integer, primary_key=True)  # Primary key for the user record
    email = Column(String(255), unique=True, nullable=False)  # Unique email address, cannot be null
    user_name = Column(String(50), nullable=False)  # User's name, not required to be unique
    password_hash = Column(String(255), nullable=False)  # Hashed password for security
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of user creation

    # Define a one-to-many relationship with ChatThread.
    # A user can have multiple chat threads.
    threads = relationship("ChatThread", back_populates="user", cascade="all, delete-orphan")

class ChatThread(Base):
    __tablename__ = 'chat_threads'

    # Define the columns for the 'chat_threads' table.
    id = Column(Integer, primary_key=True)  # Primary key for the chat thread record
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key linking to the 'users' table
    thread_title = Column(String(255), nullable=True)  # Optional title for the chat thread
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of thread creation

    # Define a many-to-one relationship with User.
    # Each chat thread is created by one user.
    user = relationship("User", back_populates="threads")

    # Define a one-to-many relationship with Message.
    # A chat thread can contain multiple messages.
    messages = relationship("Message", back_populates="thread", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = 'messages'

    # Define the columns for the 'messages' table.
    id = Column(Integer, primary_key=True)  # Primary key for the message record
    thread_id = Column(Integer, ForeignKey('chat_threads.id'), nullable=False)  # Foreign key linking to the 'chat_threads' table
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key linking to the 'users' table
    message_content = Column(Text, nullable=False)  # Content of the message, cannot be null
    message_type = Column(String(10), nullable=False)  # Type of message: 'human' or 'ai'
    timestamp = Column(DateTime, default=datetime.utcnow)  # Timestamp of when the message was sent

    # Define a many-to-one relationship with ChatThread.
    # Each message belongs to one chat thread.
    thread = relationship("ChatThread", back_populates="messages")

    # Define a many-to-one relationship with User.
    # Each message is sent by one user.
    user = relationship("User")

# Unit model
class Unit(Base):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)  # Unique ID for each unit
    unit_name = Column(String(255), nullable=False)  # Name of the unit (e.g., "Cell Biology")
    unit_description = Column(Text, nullable=True)  # Optional description of the unit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # One-to-many relationship with questions
    questions = relationship("Question", back_populates="unit", cascade="all, delete-orphan")

# Question model
class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)  # Unique ID for each question
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)  # Foreign key to Unit
    question_text = Column(Text, nullable=False)  # The text of the question
    difficulty_level = Column(String(50), nullable=True)  # Difficulty of the question (easy, medium, hard)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    unit = relationship("Unit", back_populates="questions")
    sample_answer = relationship("SampleAnswer", back_populates="question", uselist=False, cascade="all, delete-orphan")

# SampleAnswer model
class SampleAnswer(Base):
    __tablename__ = 'sample_answers'

    id = Column(Integer, primary_key=True)  # Unique ID for each sample answer
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)  # Foreign key to Question
    answer_text = Column(Text, nullable=False)  # Reference/sample answer for the question
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    question = relationship("Question", back_populates="sample_answer")