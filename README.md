# DjangoGramm

DjangoGramm is a social media platform With the power of Django, users can seamlessly express themselves through captivating posts, rich content, and engaging interactions.


## Getting Started


### Installation

1. Clone the repository:

    ```bash
    git clone https://git.foxminded.ua/foxstudent105590/task_11-djangogramm.git
    cd DjangoGramm
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements/prod.txt
    ```

3. Apply migrations:

    ```bash
    python manage.py migrate
    ```
   
4. Load Dumpdata:

    ```bash
    python manage.py loaddata fixtures/dumpdata.json
    ```

5. Superuser:

   - **Create a Superuser:**
     ```bash
     python manage.py createsuperuser
     ```

   - **Or Login as the Admin:**
     - **Username:** admin
     - **Password:** 223344qq

    
6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Visit `http://127.0.0.1:8000/admin/` to log in with your superuser account and start using DjangoGramm.

## Features

- **User Authentication**: Users can sign up with email verification, log in, and log out securely.
- - **Password Functionality**: Users can reset the password if they forgot hem.
- **Post Creation**: Users can create posts with content and images.
- **Tagging**: Users can add tag to posts.
- **Following**: Users can follow and unfollow other users to see their posts in their feed.
- **Likes/Dislikes**: Users can like or dislike comments and posts.
- **Responsive Design**: The platform is designed to be accessible and user-friendly.

## Usage

- Navigate to `http://127.0.0.1:8000/` to access the main application.
- Explore the features, create posts, follow other users, and engage with the community.


## Acknowledgements

- [Django Documentation](https://docs.djangoproject.com/)
