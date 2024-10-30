# Manifest Kenya Registration Platform

[![Python Version](https://img.shields.io/badge/python-3.11-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-5.1-brightgreen.svg)](https://www.djangoproject.com/download/)
[![Bootstrap Version](https://img.shields.io/badge/bootstrap-5.3-purple.svg)](https://getbootstrap.com/docs/5.3/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Manifest Kenya](https://github.com/am-derrick/church_reg/blob/prod/static/images/logo-01.png)

A robust church registration platform built with Django, featuring member management and a custom admin dashboard with analytics.

## 🚀 Features

- Member registration and management system
- Custom admin dashboard with role-based access control
- Analytics and audit logging
- Responsive Bootstrap 5.3 UI
- Secure authentication system

## 🏗️ Project Structure

The project consists of two main applications:

1. `members`
   - Handles member registration
   - Manages member data and logic
   - Custom views and forms

2. `custom_admin`
   - Custom user model with role-based access
   - Admin dashboard with analytics
   - Audit logging system
   - Authentication views (signup, login)

## 🌐 Live Demo

- [Registration Portal](http://www.manifestke.com/members/register)
- [Admin Dashboard](http://www.manifestke.com/custom_admin)

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- pip
- virtualenv (recommended)

### Local Development Setup

1. Clone the repository
```bash
git clone git@github.com:am-derrick/church_reg.git
cd church_registration
```

2. Create and activate virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
```

Required environment variables:
- `DJANGO_SECRET_KEY`: Random secret key for Django
- `DEBUG`: Set to `True` for development
- `DEVELOPMENT_MODE`: Set to `True` for development
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string (optional)

5. Setup database
```bash
python manage.py migrate
python manage.py makemigrations
```

6. Run development server
```bash
python manage.py runserver
```

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🧪 Running Tests

```bash
python manage.py test
```

## 📝 Code Style

This project follows the [Black](https://github.com/psf/black) code style. To format your code:

```bash
black .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Useful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/)
- [Python Documentation](https://docs.python.org/3/)

## 📧 Support

For support, email ampire90@gmail.com or open an issue in the repository.