from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Collect data from the form and convert to numeric values
    data = {
        'Neuroticism': [
            int(request.form['anxiety']),
            int(request.form['hostility']),
            int(request.form['depression']),
            int(request.form['self-consciousness']),
            int(request.form['impulsiveness']),
            int(request.form['vulnerability'])
        ],
        'Extraversion': [
            int(request.form['warmth']),
            int(request.form['gregariousness']),
            int(request.form['assertiveness']),
            int(request.form['activity']),
            int(request.form['excitement_seeking']),
            int(request.form['positive_emotion'])
        ],
        'Openness to Experience': [
            int(request.form['fantasy']),
            int(request.form['aesthetics']),
            int(request.form['feelings']),
            int(request.form['actions']),
            int(request.form['ideas']),
            int(request.form['values'])
        ],
        'Agreeableness': [
            int(request.form['trust']),
            int(request.form['straightforwardness']),
            int(request.form['altruism']),
            int(request.form['compliance']),
            int(request.form['modesty']),
            int(request.form['tender_mindedness'])
        ],
        'Conscientiousness': [
            int(request.form['competence']),
            int(request.form['orderliness']),
            int(request.form['dutifulness']),
            int(request.form['achievement_striving']),
            int(request.form['self_discipline']),
            int(request.form['deliberation'])
        ]
    }

    # Calculate cumulative scores for each main category
    cumulative_scores = {category: sum(scores) for category, scores in data.items()}

    # Prepare data for radar chart
    labels = list(cumulative_scores.keys())
    values = list(cumulative_scores.values())
    values += values[:1]  # Repeat the first value to close the radar chart

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop

    # Colors for each main category
    colors = ['red', 'green', 'blue', 'purple', 'orange']

    # Create radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='grey', alpha=0.1)  # Background fill for visibility

    for i in range(len(labels)):
        values_single = [values[i], values[i+1]]
        angles_single = [angles[i], angles[i+1]]
        ax.fill(angles_single, values_single, color=colors[i], alpha=0.25)
        ax.plot(angles_single, values_single, color=colors[i], linewidth=2)

    ax.set_yticklabels([])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('result.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
