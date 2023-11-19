import openai
from openai.error import AuthenticationError
from flask import Flask, render_template, redirect, request, flash, session, url_for
from sqlalchemy.sql.expression import desc

from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datablog.sqlite3"
app.config['SECRET_KEY'] = 'my_secret_key'
app.app_context().push()
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if "api_key" in session:
      print(session['api_key'])
    if request.method == "POST":
        if "api_key" not in session:
            # If API key doesn't exist in the session, redirect to the API key form.
            return redirect(url_for('api_key_form'))
        else:
            response = request.form
            if response['prompt']:
                prompt = response['prompt']
                openai.api_key = session['api_key']
                gpt_prompt = f"""Turn the following into an article in the style of The Hindu: {prompt}

                  Your response should be structured exactly like this:
                  Headline:
                  Subheading:
                  Summary:
                  Article:
                  Prompt for thumbnail image:
                  """
                try:
                    response = openai.Completion.create(model="text-davinci-003",
                                                            prompt=gpt_prompt,
                                                            temperature=0.7,
                                                            max_tokens=500,
                                                            top_p=1,
                                                            frequency_penalty=0,
                                                            presence_penalty=0)

                    response = response["choices"][0]["text"]

                    start_headline = response.index("Headline:") + len("Headline:")
                    end_headline = response.index("Subheading:")
                    start_subheading = response.index("Subheading:") + len("Subheading:")
                    end_subheading = response.index("Summary:")
                    start_summary = response.index("Summary:") + len("Summary:")
                    end_summary = response.index("Article:")
                    start_article = response.index("Article:") + len("Article:")
                    end_article = response.lower().index("prompt for thumbnail image:")

                    headline = response[start_headline:end_headline].strip()
                    subheading = response[start_subheading:end_subheading].strip()
                    summary = response[start_summary:end_summary].strip()
                    article = response[start_article:end_article].strip()

                    headline = str(headline)
                    subheading = str(subheading)
                    summary = str(summary)
                    article = str(article)

                    new_article = Article(prompt=prompt, headline=headline, subheading=subheading, summary=summary, article=article)
                    try:
                        db.session.add(new_article)
                        db.session.commit()
                        return redirect("/")
                    except:
                        return "There was a problem processing. Please go Back!"
                except AuthenticationError:
                    flash('Incorrect API key provided. Please provide a valid API key.')
                    session.pop('api_key', None)  # Remove incorrect key from the session
                    return redirect(url_for('api_key_form'))
                    
              

    else:
        return render_template('all.html', articles=Article.query.order_by(desc('id')).all())

@app.route('/article/<int:id>', methods=['GET', 'POST'])
def article(id):
    article = Article.query.get(id)
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template('article.html', article=article)

@app.route('/api_key_form', methods=['GET', 'POST'])
def api_key_form():
    if request.method == "POST":
        api_key = request.form.get('api_key')
        if api_key:
            # Store the API key in the session.
            session['api_key'] = api_key
            return redirect('/')
        else:
            flash('Please provide an API key.')
    return render_template('api_key_form.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
