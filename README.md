## AI Chat System API

This is a Django-based API system that allows users to register, log in, chat with an AI chatbot, check their token balance, and top-up tokens. Each user starts with 4000 tokens, and each message sent to the AI deducts 100 tokens.

## Features

- **User Registration**: Register with a unique username and password.
- **User Login**: Authenticate via JWT token.
- **Chat with AI**: Send messages to an AI and receive responses, while tokens are deducted.
- **Token Management**: View remaining token balance and top-up tokens.

## Installation Instructions

### Prerequisites

- Python 3.x
- Django 3.x or higher
- Django REST Framework
- SimpleJWT for JWT Authentication
- drf-spectacular for API documentation

### Steps to Install

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/ai_chat_system.git
   cd ai_chat_system


2. **Create and activate a virtual environment:**

    ```bash
    python -m venv newenv
    source newenv/bin/activate  # On Windows use: newenv\Scripts\activate


3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt


4. **Run migrations to set up the database:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate


5. **Create a superuser (for accessing the Django admin panel):**

    ```bash
    python manage.py createsuperuser


6. **Start the development server:**

    ```bash
    python manage.py runserver


- The API will be available at `http://127.0.0.1:8000/`.


## Usage

1. Access the API documentation:

- Visit the Swagger UI documentation at `http://127.0.0.1:8000/api/docs/`.

### Running Tests
Unit tests are included for all endpoints. You can run them using:

```bash
python manage.py test
```

## Challenges Encountered
1. **JWT Authentication Setup:** Integrating JWT authentication using SimpleJWT required proper configuration to ensure that tokens were passed in headers correctly.

2. **drf-yasg Swagger Documentation Issues:** Initially, we used drf-yasg for API documentation, but it caused issues with handling JWT tokens in Swagger UI. This was resolved by switching to drf-spectacular, which provided better integration with Django and JWT tokens.


## Suggestions for Improvement
1. **AI Integration:** Currently, the AI response is a dummy response. Integrating a real AI service, such as OpenAI's GPT API, would make the chatbot more functional.

2. **Token Expiry:** Implementing token expiry and renewal functionality would enhance the system for real-world usage.

3. **Rate Limiting:** Adding rate limiting would help protect the system from abuse.