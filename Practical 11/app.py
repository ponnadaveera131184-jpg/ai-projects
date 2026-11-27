
from flask import Flask, render_template, request

app = Flask(__name__)

RULES = [
    (["rain"], "wet_ground", "If it rains, the ground becomes wet."),
    (["sprinkler_on"], "wet_ground", "If the sprinkler is on, the ground becomes wet."),
    (["rain"], "carry_umbrella", "If it rains, carry an umbrella."),
    (["cloudy", "rain"], "possible_rain", "Cloudy weather with rain confirms possible rain."),
    (["wet_ground", "traffic_busy"], "drive_slowly", "Wet roads and busy traffic mean drive slowly."),
    (["possible_rain"], "carry_umbrella", "If rain is expected, carry an umbrella.")
]

FACT_LABELS = {
    "rain": "Rain",
    "cloudy": "Cloudy weather",
    "sprinkler_on": "Sprinkler is ON",
    "traffic_busy": "Traffic is busy",
    "wet_ground": "Ground is wet",
    "carry_umbrella": "Carry an umbrella",
    "possible_rain": "Possible rain",
    "drive_slowly": "Drive slowly"
}


def forward_chaining(initial_facts):
    facts = set(initial_facts)
    steps = []
    changed = True

    while changed:
        changed = False

        for premises, conclusion, explanation in RULES:
            if all(fact in facts for fact in premises):
                if conclusion not in facts:
                    facts.add(conclusion)
                    steps.append(explanation)
                    changed = True

    return facts, steps


@app.route("/", methods=["GET", "POST"])
def index():
    selected_facts = []
    final_facts = []
    steps = []
    submitted = False

    if request.method == "POST":
        submitted = True
        selected_facts = request.form.getlist("facts")

        facts, steps = forward_chaining(selected_facts)

        final_facts = [
            FACT_LABELS.get(fact, fact)
            for fact in sorted(facts)
        ]

    return render_template(
        "index.html",
        selected_facts=selected_facts,
        final_facts=final_facts,
        steps=steps,
        submitted=submitted
    )


if __name__ == "__main__":
    app.run(debug=True)
