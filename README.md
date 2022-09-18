# Hot
(Developer: Fergal Quinn)

![Mockup of Scubasport International](readme/mockup.jpg)

[View live site](https://ci-pp5-hot.herokuapp.com/)

** For testing payment with this site please use the following card details:**

A regular user has been setup with the username of customer and password of custpass

+ When making a payment as a regular user, a test credit card of 4242424242424242 has been set up for the card number
For the expiry date, cvc and postal code any series number(s) can be used(once they meet the mimimum values)

## Table of Content

1. [Strategy](#project-goals)
    1. [Site Owner Goals](#site-owner-goals)
    2. [User Goals](#user-goals)
    3. [Target Audience](#target-audience)
    3. [Business Model](#business-model)
    4. [SEO](#seo)
    5. [Marketing](#marketing)
2. [Structure](#structure)
    1. [Website pages](#website-pages)
    2. [Code Structure](#code-structure)
    3. [Database](#database)
    4. [Physical database model](#physical-database-model)
    5. [Models](#models)
        1. [User Model](#user-model)
        2. [UserProfile Model](#userprofile-model)
        3. [Product Model](#product-model)
        4. [Category Model](#category-model)
        5. [Brand Model](#brand-model)
        6. [Size Model](#size-model)
        7. [Color Model](#color-model)
        8. [Inventory Model](#inventory-model)
        10. [Course Model](#contact-model)
        11. [Contact Model](#reason-model)
        12. [Faq Model](#about-model)
    3. [Scope](#scope)
        1. [User Stories](#user-stories)
    4. [Skeleton](#skeleton)
        1. [Wireframes](#wireframes)
    5. [Surface](#surface)
        1. [Design Choices](#design-choices)
        2. [Colour](#colours)
        3. [Fonts](#fonts)
5. [Technologies Used](#technologies-used)
    1. [Languages](#languages)
    2. [Frameworks & Tools](#frameworks-&-tools)
6. [Features](#features)
7. [Testing](#validation)
    1. [HTML Validation](#HTML-validation)
    2. [CSS Validation](#CSS-validation)
    3. [JS Validation](#JS-validation)
    4. [Python Validation](#py-validation)
    5. [Accessibility](#accessibility)
    6. [Performance](#performance)
    7. [Device testing](#performing-tests-on-various-devices)
    8. [Browser compatibility](#browser-compatibility)
    9. [Testing user stories](#testing-user-stories)
8. [Bugs](#Bugs)
9. [Deployment](#deployment)
10. [Credits](#credits)
11. [Acknowledgements](#acknowledgements)

# User Experience
## Strategy

### Site Owner Goals


### User Goals

### Target Audience
## User Requirements and Expectations

## Business Model

## SEO


## Marketing

### Facebook Business Page


### Newsletter Signup

## Structure
### Code Structure
### Database
#### Physical database model


#### Models

##### User Model

##### UserProfile Model

##### Product Model

##### Category Model

##### Brand Model

##### Size Model

##### Color Model

##### Inventory Model

##### Course Model

##### Contact Model

##### Faq Model


## Scope
### User stories:


#### Error Flow

## Skeleton

### Wireframes


## Surface

### Design choices

### Colours

### Typography

## Features


### Page 1 – Home page


## Technologies Used

### Languages

#### Python Libraries


### Frameworks & Tools

## Validation

### HTML Validation


### CSS Validation
### JS Validation

### Py Validation

#### Admin py-validation


#### Forms py validation


#### Models py validation


#### Urls py validation


#### Context py validation


#### Views py validation


### Accessibility
### Performance 

## Testing

### Manual Testing
### Testing user stories

## Automated Testing

### Unit testing

As part of the project I have used a number of automated tests using the built in Django testing framework which is based on python unittest.

I have demonstrated some proficiency in using these tests however due to the tight time constraints on this project, the code does not have full coverage.  For future releases and project I could endeavor to increase the number of unit tests and coverage of the code.

#### About


#### Bag


#### Checkout


#### Contact



#### Home


#### Clothes

### Coverage


## Bugs

## Stripe

# Deployment
There are a number of applications that need to be configured to run this application locally or on a cloud based service, for example Heroku

## Amazon WebServices
1. Create an account at aws.amazon.com
2. Open the S3 application and create an S3 bucket named "hot"
3. Uncheck the "Block All Public access setting"
4. In the Properties section, navigate to the "Static Website Hosting" section and click edit
5. Enable the setting, and set the index.html and the error.html values
<br>![AWS Static](readme/misc/aws_static.png)
6. In the Permissions section, click edit on the CORS configuration and set the below configuration
<br>![AWS CORS](readme/misc/aws_cors.png)
7. In the permissions section, click edit on the bucket policy and generate and set the below configuration(or similar to your settings)
<br>![AWS Bucket Policy](readme/misc/aws_bucket_policy.png)
8. In the permissions section, click edit on the Access control list(ACL)
9. Set Read access for the Bucket ACL for Everyone(Public Access)
10. The bucket is created, the next step is to open the IAM application to set up access
11. Create a new user group named "manage-hot"
12. Add the "AmazonS3FullAccess" policy permission for the user group
<br>![AWS Bucket Policy](readme/misc/aws_user_group.png)
13. Go to "Policies" and click "Create New Policy"
14. Click "Import Managed Policy" and select "AmazonS3FullAccess" > Click 'Import'.
15. In the JSON editor, update the policy "Resource" to the following
<br><code>"Resource": [</code>
<br><code>"arn:aws:s3:::ci-pp5-hot",</code>
<br><code>"arn:aws:s3:::ci-pp5-hot/*"</code>
<br><code>]</code>
16. Give the policy a name and click "Create Policy"
17. Add the newly created policy to the user group
<br>![AWS Bucket Policy](readme/misc/aws_policy.png)
18. Go to Users and create a new user
19. Add the user to the user group manage-hot
20. Select "Programmatic access" for the access type
21. Note the AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID variables, they are used in other parts of this README for local deployment and Heroku setup
22. The user is now created with the correct user group and policy
<br>![AWS Bucket Policy](readme/misc/aws_user.png)
23. Note the AWS code in settings.py. Note an environment variable called USE_AWS must be set to use these settings, otherwise it will use local storage
<br>![AWS Settings](readme/misc/aws_settings.PNG)
24. These settings set up a cache policy, set the bucket name, and the environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY that you set in your aws account
25. The configuration also requires the media/static folders that must be setup in the AWS S3 bucket to store the media and static files 

## Local Deployment
To run this project locally, you will need to clone the repository
1. Login to GitHub (https://wwww.github.com)
2. Select the repository fergalquinn77/ci_pp5_summer_fashions.git
3. Click the Code button and copy the HTTPS url, for example: https://github.com/fergalquinn77/ci_pp5_summer_fashions.git
4. In your IDE, open a terminal and run the git clone command, for example 

    ```git clone https://github.com/fergalquinn77/ci_pp5_summer_fashions.git```

5. The repository will now be cloned in your workspace
6. Create an env.py file(do not commit this file to source control) in the root folder in your project, and add in the following code with the relevant key, value pairs, and ensure you enter the correct key values<br>
<br><code>import os</code>
<br><code>os.environ["SECRET_KEY"]= 'TO BE ADDED BY USER'</code>
<br><code>os.environ["STRIPE_PUBLIC_KEY"]= 'TO BE ADDED BY USER'</code>
<br><code>os.environ["STRIPE_SECRET_KEY"]= 'TO BE ADDED BY USER'</code>
<br><code>os.environ["STRIPE_WH_SECRET"]= 'TO BE ADDED BY USER'</code>
<br><code>os.environ["AWS_ACCESS_KEY_ID"]= 'TO BE ADDED BY USER'</code>
<br><code>os.environ["AWS_SECRET_ACCESS_KEY"]= 'TO BE ADDED BY USER'</code>
<br><code>os.environ["EMAIL_HOST_USER"]= 'TO BE ADDED BY USER'</code>
<br><code>os.environ["EMAIL_HOST_PASS"]= 'TO BE ADDED BY USER'</code>
<br><code>os.environ["USE_AWS"]= 'TO BE ADDED BY USER'</code>
<br><code>os.environ["DATABASE_URL"]= 'TO BE ADDED BY USER'</code>
<br><code>os.environ["DEVELOPMENT"] ='True'</code>
7. Some values for the environment variables above are described in different sections of this readme
8. Install the relevant packages as per the requirements.txt file
9. In the settings.py ensure the connection is set to either the Heroku postgres database or the local sqllite database
10. Ensure debug is set to true in the settings.py file for local development
11. Add localhost/127.0.0.1 to the ALLOWED_HOSTS variable in settings.py
12. Run "python3 manage.py showmigrations" to check the status of the migrations
13. Run "python3 manage.py migrate" to migrate the database
14. Run "python3 manage.py createsuperuser" to create a super/admin user
15. Run manage.py loaddata db.json to load the product data into the database
18. Start the application by running <code>python3 manage.py runserver</code>
19. Open the application in a web browser, for example: http://127.0.0.1:8000/

## Heroku and Postgres Database
To deploy this application to Heroku, run the following steps.
1. Create an account at heroku.com
2. Create an app, give it a name for example scuabasport, and select a region
3. Under resources search for postgres, and add a Postgres database to the app

![Heroku Postgres](readme/misc/heroku_postgres.png)
    
4. Note the DATABASE_URL, this can be set as an environment variable in Heroku and your local deployment(env.py)
5. Install the plugins dj-database-url and psycopg2-binary.
6. Run pip3 freeze > requirements.txt so both are added to the requirements.txt file
7. Create a Procfile with the text: web: gunicorn summerfashions.wsgi:application for example
8. In the settings.py ensure the connection is to the Heroku postgres database
9. Ensure debug is set to false in the settings.py file
10. Add localhost/127.0.0.1, and scuabasport.herokuapp.com to the ALLOWED_HOSTS variable in settings.py
11. Run "python3 manage.py showmigrations" to check the status of the migrations
12. Run "python3 manage.py migrate" to migrate the database
13. Run "python3 manage.py createsuperuser" to create a super/admin user
14. Run python3 manage.py loaddata db.json
16. Install gunicorn and add it to the requirements.tx file using the command pip3 freeze > requirements.txt
17. From the CLI login to Heroku using the command heroku git:remote -a hot
18. Disable collectstatic in Heroku before any code is pushed using the command heroku config:set DISABLE_COLLECTSTATIC=1 -a hot
19. Push the code to Heroku using the command git push heroku master
20. Ensure the following environment variables are set in Heroku
<br>![Heroku Env variables](readme/misc/heroku_env_variables.png)
21. Connect the app to GitHub, and enable automatic deploys from main
<br>![Heroku Postgres](readme/misc/heroku_deployment.png)
22. Click deploy to deploy your application to Heroku for the first time
23. Click on the link provided to access the application
24. If you encounter any issues accessing the build logs is a good way to troubleshoot the issue

## Credits


### Media

### Acknowledgements: 
