# Bookmarker API

The **Bookmarker API** is a simple RESTful API designed to manage bookmarks. The API allows users to create, read, update, and delete bookmarks, making it a useful tool for personal bookmark management or integration into larger projects that require bookmark functionality.

## Features

- **Create**: Add new bookmarks with a title, URL, and optional description.
- **Read**: Retrieve all bookmarks or a specific bookmark by ID.
- **Update**: Modify existing bookmarks.
- **Delete**: Remove bookmarks that are no longer needed.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- [Python 3.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/swewalka-tgm/bookmarker-api.git
   cd bookmarker-api
   ```
2. **Install the required dependencies:**
```bash
pip install -r requirements.txt
```
3. **Set up environment variables:**
Create a .flaskenv file in the root directory (if not already present) and add the following configuration:
```bash
FLASK_APP=src
FLASK_ENV=development
```

4. **Run the application:**
```bash
flask run
```
**Deployment**

To deploy this API on a platform like Heroku, you can use the provided Procfile. Make sure to configure any necessary environment variables on your deployment platform.
