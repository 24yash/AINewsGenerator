# News Article Generation with OpenAI API

This project allows users to generate news articles based on provided prompts using the OpenAI API and showcases the generated articles in a feed format.

## Overview

The code in this repository is a Flask-based web application that integrates with the OpenAI API to generate news articles. It involves taking user prompts, processing them through the OpenAI text-generating model (specifically, the `text-davinci-003` model), and storing the generated articles in a SQLite database. The generated articles are then displayed in a feed format on the web application.

## How it works

The core functionalities of the code include:

- Retrieving user prompts through a web form.
- Authenticating with the OpenAI API using the provided API key.
- Generating news articles based on user prompts using the OpenAI API's text generation capabilities.
- Storing the generated articles in a SQLite database.
- Displaying the stored articles in a feed-like interface on the web application.

## Getting Started

### Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- OpenAI Python package

### Setup Instructions

1. Clone this repository.
2. Install the necessary Python dependencies using `pip install -r requirements.txt`.
3. Run the Flask application using `python app.py`.

## Usage

1. Access the web application by navigating to `http://localhost:5000/` in your browser.
2. Submit a prompt in the provided form to generate a news article.
3. View the generated articles in the feed.

## File Structure

- `app.py`: Contains the Flask application code for handling user requests and interacting with the OpenAI API.
- `models.py`: Defines the SQLAlchemy model for the SQLite database.
- HTML templates for rendering web pages:
  - `base.html`: Base HTML layout.
  - `all.html`: Template for displaying all articles in the feed.
  - `article.html`: Template for displaying a single article.
  - `api_key_form.html`: Template for providing the OpenAI API key.
