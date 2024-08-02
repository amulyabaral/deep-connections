from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
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

    # Creating DataFrame for each main category with subcategories
    neuroticism_df = pd.DataFrame({
        'Subcategory': ['Anxiety', 'Hostility', 'Depression', 'Self-consciousness', 'Impulsiveness', 'Vulnerability'],
        'Score': data['Neuroticism']
    }).set_index('Subcategory')
    
    extraversion_df = pd.DataFrame({
        'Subcategory': ['Warmth', 'Gregariousness', 'Assertiveness', 'Activity', 'Excitement Seeking', 'Positive Emotion'],
        'Score': data['Extraversion']
    }).set_index('Subcategory')
    
    openness_df = pd.DataFrame({
        'Subcategory': ['Fantasy', 'Aesthetics', 'Feelings', 'Actions', 'Ideas', 'Values'],
        'Score': data['Openness to Experience']
    }).set_index('Subcategory')
    
    agreeableness_df = pd.DataFrame({
        'Subcategory': ['Trust', 'Straightforwardness', 'Altruism', 'Compliance', 'Modesty', 'Tender-mindedness'],
        'Score': data['Agreeableness']
    }).set_index('Subcategory')
    
    conscientiousness_df = pd.DataFrame({
        'Subcategory': ['Competence', 'Orderliness', 'Dutifulness', 'Achievement Striving', 'Self-discipline', 'Deliberation'],
        'Score': data['Conscientiousness']
    }).set_index('Subcategory')

    # Concatenate all DataFrames into one
    combined_df = pd.concat([neuroticism_df, extraversion_df, openness_df, agreeableness_df, conscientiousness_df], axis=0, keys=['Neuroticism', 'Extraversion', 'Openness to Experience', 'Agreeableness', 'Conscientiousness'])
    combined_df = combined_df.reset_index().rename(columns={'level_0': 'Category'})

    # Pivot the DataFrame for plotting
    plot_df = combined_df.pivot(index='Category', columns='Subcategory', values='Score')

    # Plotting the stacked bar graph using seaborn for pastel colors
    fig, ax = plt.subplots(figsize=(10, 7))
    plot_df.plot(kind='bar', stacked=True, ax=ax, color=sns.color_palette("pastel", len(plot_df.columns)))

    ax.set_title('Personality Traits Stacked Bar Graph')
    ax.set_ylabel('Scores')
    ax.set_xlabel('Personality Categories')
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1), title='Subcategories')

    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('result.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)