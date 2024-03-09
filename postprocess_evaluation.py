import pandas as pd
import re
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


def per_evaluator_stats(df,score):

    # Mode: The most frequently occurring value in the score_accuracy.
    # Quantiles: Percentiles such as the 25th, 75th, and possibly other percentiles to understand the distribution of scores.
    # Range: The difference between the maximum and minimum values.
    # Interquartile Range (IQR): The range between the 25th and 75th percentiles, which can provide information about the spread of the middle 50% of the data.
    # Coefficient of Variation (CV): Ratio of the standard deviation to the mean, expressed as a percentage. It provides a measure of relative variability.
    # Count: Total number of rows (entries)
    df = df.groupby(['evaluator','model','prompting'])[score].agg([
    'mean', 'median', 'std', 'min', 'max',
    lambda x: x.mode().iloc[0], # Mode
    lambda x: x.quantile(0.25),  # 25th percentile
    lambda x: x.quantile(0.75),  # 75th percentile
    lambda x: x.max() - x.min(), # Range
    lambda x: x.quantile(0.75) - x.quantile(0.25), # IQR
    lambda x: x.std() / x.mean() * 100 if x.mean() != 0 else 0, # Coefficient of Variation
     'count'
    ])
    # Rename the lambda functions for better understanding
    df = df.rename(columns={
        '<lambda_0>': 'mode',
        '<lambda_1>': '25th_percentile',
        '<lambda_2>': '75th_percentile',
        '<lambda_3>': 'range',
        '<lambda_4>': 'IQR',
        '<lambda_5>': 'CV'
    })
    
    df = df.reset_index()
    df['score'] = score
    
    return df
    


def per_evaluator_plots(df,score):
    
    prompting_type = df['prompting'].unique()[0]
    
    df = df.sort_values(by='model', ascending=True)

    fig = px.box(df, x="model", y=score, color="evaluator")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default

    fig.update_layout(title=score + ': ' + prompting_type + " Prompting",
                      legend_title_text='LLM Evaluator', width=1000, height=600)

    fig.show()
    
    df = df.groupby(['model','evaluator'])[score].value_counts().reset_index()
    fig = px.scatter(df, x="model", y=score, color=score,
                     size='count', hover_data=['evaluator'], width=1000, height=600)
    fig.show()


    
    
def per_context_plots(df,evaluator,score):
    
    df = df[df.evaluator == evaluator]
    
    df = df.sort_values(by='model', ascending=True)

    fig = px.box(df, x="model", y=score, color="prompting")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default

    fig.update_layout(title=score + ': ' + evaluator + " evaluator", width=1000, height=600)
    fig.show()   

    df = df.groupby(['model','prompting'])[score].value_counts().reset_index()
    fig = px.scatter(df, x="model", y=score, color=score,
                     size='count', hover_data=['prompting'], width=1000, height=600)
    fig.show()

def per_user_plots(df,score):
    df = df.sort_values(by='user', ascending=True)

    fig = px.box(df, y=score, color="user")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig.update_layout(title=score + ': summarized',legend_title_text='User', width=1000, height=600)
    fig.show()

    fig = px.box(df, x='model', y=score, color="user")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig.update_layout(title=score + ': per model',legend_title_text='User', width=1000, height=600)
    fig.show()

    fig = px.box(df, x='prompting', y=score, color="user")
    fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig.update_layout(title=score + ': per context',legend_title_text='User', width=1000, height=600)
    fig.show()