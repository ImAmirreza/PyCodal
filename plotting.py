import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
import jalali_pandas
def load_and_convert_data(symbol):
    try:
        with open(f"Data/{symbol}/Total.json", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {symbol}/Total.json does not exist.")
    
    df = pd.DataFrame(list(data.items()), columns=['Date', 'Income'])
    try:
        df['Date'] = df['Date'].jalali.parse_jalali("%Y/%m/%d")
    except Exception as e:
        raise ValueError(f"Error parsing Jalali dates: {e}")
    
    df['Year'] = df['Date'].jalali.year
    df['Month'] = df['Date'].jalali.month
    df['Income'] = pd.to_numeric(df['Income'], errors='coerce') / 10000

    output_csv = f"Data/{symbol}/Total.csv"
    # os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    return df

def filter_and_pivot_data(df, year):
    df = df[df['Year'] != year]
    df_pivot = df.pivot(index='Month', columns='Year', values='Income')
    return df_pivot

def plot_monthly_data(df_pivot, symbol, show=False):
    # Set Seaborn theme
    sns.set_theme(style="whitegrid")
    print(df_pivot)
    # Reset index to use for plotting
    df_melted = df_pivot.reset_index().melt(id_vars='Month', var_name='Year', value_name='Income')
    df_melted.rename(columns={'index': 'Month'}, inplace=True)

    # Create a color palette for years
    palette = sns.color_palette("husl", len(df_pivot.columns))

    # Plot the bar chart
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(data=df_melted, x='Month', y='Income', hue='Year', palette=palette, edgecolor='black')

    # Enhance aesthetics
    plt.title(f"Monthly Income Over Years for {symbol}", fontsize=16, weight='bold', pad=15)
    plt.xlabel("Month", fontsize=14, labelpad=10)
    plt.ylabel("Income", fontsize=14, labelpad=10)
    plt.xticks(fontsize=12, rotation=45, ha='right')
    plt.yticks(fontsize=12)
    plt.legend(title="Year", fontsize=12, title_fontsize=14, loc='upper left', bbox_to_anchor=(1, 1))

    # Add percentage changes between years as annotations
    months = df_pivot.index.tolist()
    years = df_pivot.columns.tolist()
    years.sort()

    for month_index, month in enumerate(months):
        previous_year_income = df_pivot.loc[month, years[0]]
        current_year_income = df_pivot.loc[month, years[-1]]
        if not pd.isnull(previous_year_income) and not pd.isnull(current_year_income):
            percentage_change = ((current_year_income - previous_year_income) / previous_year_income) * 100
            if percentage_change > 0:
                plt.text(
                    x=month_index,
                    y=current_year_income + current_year_income / 50,
                    s=f'+{percentage_change:.2f}%',
                    color='green',
                    fontsize=10,
                    weight='bold',
                    ha='center'
                )
            else:
                plt.text(
                    x=month_index,
                    y=previous_year_income + previous_year_income / 50,
                    s=f'{percentage_change:.2f}%',
                    color='red',
                    fontsize=10,
                    weight='bold',
                    ha='center'
                )
    plt.tight_layout()
    if show:
        plt.show()
    else:
        plt.savefig(f'Data/{symbol}/Monthly.png')


def calculate_and_plot_quarterly_data(df, symbol,show=False):
    # Filter data to exclude a specific year
    df = df[df['Year'] != 1401]

    # Calculate Quarter based on Month
    df['Quarter'] = df['Month'].apply(lambda x: (x - 1) // 3 + 1)

    # Group data by Quarter and Year, then calculate the sum of Income
    df_quarterly = df.groupby(['Quarter', 'Year'])['Income'].sum().unstack()

    # Display the quarterly data
    print(df_quarterly)

    # Set Seaborn theme for aesthetics
    sns.set_theme(style="whitegrid")

    # Create a color palette for years
    palette = sns.color_palette("husl", len(df_quarterly.columns))

    # Plot the bar chart
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(
        data=df_quarterly.reset_index().melt(id_vars='Quarter', var_name='Year', value_name='Income'),
        x='Quarter', y='Income', hue='Year', palette=palette, edgecolor='black'
    )

    # Enhance plot aesthetics
    plt.title(f"Quarterly Income Over Years for {symbol}", fontsize=16, weight='bold', pad=15)
    plt.xlabel("Quarter", fontsize=14, labelpad=10)
    plt.ylabel("Income", fontsize=14, labelpad=10)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title="Year", fontsize=12, title_fontsize=14, loc='upper left', bbox_to_anchor=(1, 1))

    # Add percentage change annotations
    quarters = df_quarterly.index.tolist()
    years = df_quarterly.columns.tolist()
    years.sort()

    for quarter_index, quarter in enumerate(quarters):
        previous_year_income = df_quarterly.loc[quarter, years[0]] if len(years) > 0 else None
        current_year_income = df_quarterly.loc[quarter, years[-1]] if len(years) > 1 else None

        if previous_year_income and current_year_income and not pd.isnull(previous_year_income) and not pd.isnull(current_year_income):
            percentage_change = ((current_year_income - previous_year_income) / previous_year_income) * 100
            if percentage_change > 0:
                plt.text(
                    x=quarter_index,
                    y=current_year_income + current_year_income / 50,
                    s=f'+{percentage_change:.2f}%',
                    color='green',
                    fontsize=10,
                    weight='bold',
                    ha='center'
                )
            else:
                plt.text(
                    x=quarter_index,
                    y=previous_year_income + previous_year_income / 50,
                    s=f'{percentage_change:.2f}%',
                    color='red',
                    fontsize=10,
                    weight='bold',
                    ha='center'
                )

    # Tight layout for better spacing
    plt.tight_layout()
    if show:
        plt.show()
    else:
        plt.savefig(f'Data/{symbol}/Quarterly.png')
def main(symbol):
    df = load_and_convert_data(symbol)
    try:
        df_pivot = filter_and_pivot_data(df, 1401)
    except ValueError as e:
        print(f"Error in pivoting data: {e}")
        return

    print("Monthly data pivoted successfully.")

    # Plot monthly data (placeholder for integration)
    plot_monthly_data(df_pivot, symbol)  # If required

    calculate_and_plot_quarterly_data(df, symbol)

if __name__ == "__main__":
    main("شکلر")
