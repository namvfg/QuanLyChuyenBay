from app import app, controller
from app import admin, dao

#load trang chu
app.add_url_rule("/", "index", controller.index)


if __name__ == "__main__":
    app.run(debug=True)