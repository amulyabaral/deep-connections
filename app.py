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

    cumulative_scores = {category: sum(scores) for category, scores in data.items()}

    labels = list(cumulative_scores.keys())
    values = list(cumulative_scores.values())
    values += values[:1]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    colors = ['#ADD8E6' for _ in range(len(labels))]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    ax.fill(angles, values, color='lightblue', alpha=0.25)
    ax.plot(angles, values, color='lightblue', linewidth=2)

    # Adding dots for each category
    ax.scatter(angles[:-1], values[:-1], color='blue', s=50, zorder=10)

    # Adding category labels at the data points
    for angle, value, label in zip(angles, values, labels):
        ax.text(angle, value, label, horizontalalignment='center', size=12, color='blue', weight='semibold')

    ax.set_yticklabels([])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('result.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)