from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Main route

    Returns:
        HTML: index template
    """
    return render_template('index.html')
