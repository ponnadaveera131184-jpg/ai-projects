
from flask import Flask, render_template, request

app = Flask(__name__)


def diagnose(internet, wifi, other_device, router):
    if internet == "no":
        if other_device == "yes":
            return "The problem may be with your device's network settings."
        elif router == "no":
            return "The router may be switched off. Check its power connection."
        else:
            return "There may be an internet service outage. Contact your ISP."

    elif wifi == "no":
        return "Wi-Fi is disconnected. Turn on Wi-Fi and reconnect to your network."

    elif other_device == "no":
        return "The issue may be specific to your device. Restart its network connection."

    else:
        return "Your network appears to be working normally."


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        internet = request.form.get("internet")
        wifi = request.form.get("wifi")
        other_device = request.form.get("other_device")
        router = request.form.get("router")

        if all(value in ["yes", "no"] for value in
               [internet, wifi, other_device, router]):
            result = diagnose(internet, wifi, other_device, router)
        else:
            result = "Please select an answer for every question."

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
