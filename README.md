# DjangoGramm

DjangoGramm is a social media platform With the power of Django, users can seamlessly express themselves through captivating posts, rich content, and engaging interactions.


## Getting Started


### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Maks-Siglov/DjangoGramm.git
    cd DjangoGramm/
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements/prod.txt -r requirements/dev.txt

    ```

3. Apply migrations:

    ```bash
    cd djangogramm/
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

   - **Or Login as the already created Admin:**
     - **Username:** admin
     - **Password:** 223344qq

    
6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Visit `http://127.0.0.1:8000/admin/` to log in with your superuser account and start using DjangoGramm.


### Enable extended functionality

1. Project use two-step registration with email verification. For using this feature add your email data in .env file
    - **Replace data in .env file**
     ```bash
    EMAIL_HOST='smtp.gmail.com'
    EMAIL_PORT=587
    EMAIL_HOST_USER='Replace with your email'
    EMAIL_HOST_PASSWORD='Replace with your app password'    
    ```

2. Project by default stores images in media directory. But you can change it to your own AWS S3 bucket

    - **Replace data in .env file**
     ```bash
    AWS_ACCESS_KEY_ID='Your account access key'
    AWS_SECRET_ACCESS_KEY='Your account secret key'
    AWS_STORAGE_BUCKET_NAME='Name of your S3 bucket'
    AWS_S3_REGION_NAME='Your region, like eu-central-1'
    AWS_DEFAULT_ACL='Your default access control, you can choose private/public-read ...'  
    ```
   
   - **In core/settings/base uncomment DEFAULT_FILE_STORAGE and remove MEDIA_URL and MEDIA_ROOT**
    ```bash
    # DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    MEDIA_URL = "media/"
    MEDIA_ROOT = BASE_DIR / "media"
    ```
   
   - **In core/settings/urls remove this pattern:**
    ```bash
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    ```

3. Project provide login though GitHub
       - **For enable it provide your OAuth secret and Client ID in .env files**
    ```bash
    GITHUB_AUTH_CLIENT_ID='Your Client ID'
    GITHUB_AUTH_SECRET='Your OAuth app secret'
    ```
       
    - **In GitHub OAuth app settings**
     ```bash
    Homepage URL='http://127.0.0.1:8000'
    Authorization callback URL='http://localhost:8000/accounts/github/login/'
    ```

## Features

- **User Authentication**: Users can sign up with email verification, log in, and log out securely.
- **Password Functionality**: Users can reset the password if they forgot hem.
- **Post Creation**: Users can create posts with content and images.
- **Tagging**: Users can add tag to posts.
- **Following**: Users can follow and unfollow other users to see their posts in their feed.
- **Likes/Dislikes**: Users can like or dislike comments and posts.
- **Responsive Design**: The platform is designed to be accessible and user-friendly.

## Usage

- Navigate to `http://127.0.0.1:8000/` to access the main application.
- Explore the features, create posts, follow other users, and engage with the community.
