import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=[0], index_col='date')

# Clean data
df = df.loc[
    (df['value'] <= df['value'].quantile(0.975)) &
    (df['value'] >= df['value'].quantile(0.025))
    ]


def draw_line_plot():
    # Draw line plot
    fig, axes = plt.subplots(figsize=(15, 7))
    axes.plot(df.index, df['value'])
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    axes.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Years'] = df_bar.index.year
    df_bar['Months'] = df_bar.index.month
    df_bar = df_bar\
        .groupby(['Years', 'Months'])\
        .agg('mean')\
        .rename(columns={'value': 'Average Page Views'})\
        .reset_index()
    # Draw bar plot
    df_bar['Months'] = pd.to_datetime(df_bar['Months'], format='%m').dt.month_name()
    hue_order = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
    ]
    fig = sns.catplot(
        x='Years',
        y='Average Page Views',
        data=df_bar,
        kind='bar',
        hue='Months',
        hue_order=hue_order,
        legend_out=False
        # hue_order=hue_order
    ).figure
    # If you want to add the main title
    # fig.suptitle('Main Title')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(ncols=2, figsize=(18, 7))
    sns.boxplot(data=df_box, x='year', y='value', ax=ax[0], order=[2016, 2017, 2018, 2019])
    sns.boxplot(
        data=df_box,
        x='month',
        y='value',
        ax=ax[1],
        order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    )
    ax[0].set(xlabel='Year', ylabel='Page Views', title='Year-wise Box Plot (Trend)')
    ax[1].set(xlabel='Month', ylabel='Page Views', title='Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
