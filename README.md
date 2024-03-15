# Blog-App

## Description
This is a blog web application. The primary focus was on practicing all backend skills i have picked up so far.

### Features
- User Authentication
    - Ability to register an admin and a regular user
    - Email verification on signup
    - Ability to login and log out 
    - Forgot password implementation
    - Change password implementation
- User Profile Creation
    - Automatic creation of user profiles upon user regustration, providing personalized experience for each user.
    - Allow users to update their profile information, including profile picture and bio.
- Create and Edit Posts
    - Intuitive interface for creating, editing and deleting blog posts.
- Rich text Editing
    - Built-in rich text editor to format posts with ease.
- Comments
    - Ability to comment on posts.
- Search functionality
    - Good search functionality to find posts based on categories or keywords in the article.
- Blog article management
    - Enable users to manage their blog articles directly from their user-specific page.    

## Installation
### To use this repository locally:
- Clone this repository to a specified directory in your local machine.
- Make sure python is installed in your local machine.
- Create a python envirionment with; 
    `python -m venv .venv` and activate with `.venv\Scripts\activate`
- Install the dependencies;
    `pip install -r requirements.txt`
- Set up the database with;
     `python manage.py migrate`
- Start the development server;
    `python manage.py runserver`
- Open your web browser and navigate to `http://localhost:8000` to access the Blog App.    

## Usage
- Register for a new account or log in if you already have one.
- Create new blog posts by clicking on the "New Article" button.
- Edit or delete existing posts you created.
- Explore and discover posts by browsing categoriesor using the search feature.
- Engage with other users by leaving comments on their posts.

