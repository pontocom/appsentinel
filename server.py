from flask import (
    Flask,
    render_template,
    Blueprint
)
import scanner_api as scanner_api
import recommendation_api as recommendation_api

# Create the application instance
app = Flask(__name__, template_folder="templates")


def find_blueprint(api):
    for obj in vars(api).values():
        if isinstance(obj, Blueprint):
            return obj
    return None


app.register_blueprint(find_blueprint(scanner_api))
app.register_blueprint(find_blueprint(recommendation_api))


# Create a URL route in our application for "/"
# This is purely to see if the server is running, there is currently no website planned
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
