from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arizapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
    db = SQLAlchemy(app)
    
    class Ariza(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)
        content = db.Column(db.Text, nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.utcnow)

        def __repr__(self):
            return f"Ariza('{self.title}', '{self.date_created}')"

    # Ensure tables exist
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            ariza = Ariza(title=title, content=content)
            db.session.add(ariza)
            db.session.commit()
            # Post/Redirect/Get to avoid duplicate submissions on refresh
            return redirect(url_for('hello_world'))
    allpeople = Ariza.query.all()
    print(allpeople)

    return render_template('index.html', allpeople=allpeople)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id: int):
    """Delete an entry by id and redirect to home."""
    person = db.session.get(Ariza, id)
    if not person:
        # If not found, redirect back (alternatively, abort(404))
        return redirect(url_for('hello_world'))
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('hello_world'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id: int):
    """Render update form on GET; apply changes on POST then redirect."""
    person = db.session.get(Ariza, id)
    if not person:
        abort(404)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            person.title = title
            person.content = content
            db.session.commit()
            return redirect(url_for('hello_world'))
    return render_template('update.html', person=person)

if __name__ == "__main__": 
    app.run(debug=True)  