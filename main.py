import os
import requests
from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.header import Header

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
BLOG_EMAIL = os.environ.get("BLOG_EMAIL")
# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        with smtplib.SMTP("smtp.gmail.com") as connection:
            subject = "New message from your blog"
            content = f"Name:{name}\nEmail:{email}\nPhone:{phone}\nMessage:{message}"
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['subject'] = Header(subject, 'utf-8')
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,to_addrs=BLOG_EMAIL,
                                msg=msg.as_string())
        return render_template("contact.html",method=request.method)
    else:
        return render_template("contact.html",method=request.method)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
