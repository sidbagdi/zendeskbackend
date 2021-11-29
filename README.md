# zendeskbackend
Features -
1. Landing Page
![image](https://user-images.githubusercontent.com/91580288/143808834-c47d05a8-8e89-4e1e-bf18-59b1e4a23691.png)
2. Search by ID
![image](https://user-images.githubusercontent.com/91580288/143808880-7c04d362-e6f0-455e-b34b-055809cf1828.png)

3. View all tickets

![image](https://user-images.githubusercontent.com/91580288/143808750-04ee0a7d-f35f-43c1-85c4-7b5131c6dac8.png)

Setup Instructions:

1. Clone repository
2. Install Python 3.8 & pip(if not installed already)
3. pip install -r requirements.txt
4. Run command - python manage.py makemigrations
5. Run command - python manage.py migrate

Update app.ini file to enter your credentials = 
1. api_url=https://{subdomain}.zendesk.com
2. api_token={your_api_token}
3. email_id={your_email_id}

To start server - python manage.py runserver

Open browser at localhost:8000/ticket/
