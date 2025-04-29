# app.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------
# Streamlit Page Setup
# ----------------------------------------------




# Must be the first Streamlit command
st.set_page_config(page_title="Happiness Data Visualization", layout="wide")

# Centered title using HTML
st.markdown("<h1 style='text-align: center;'>Happiness Data Visualization</h1>", unsafe_allow_html=True)






# Team members
st.markdown(
    """
    <h4 style='text-align: center; color: gray;'>Team Members: Jasmine, Princy, Divya</h4>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------
# Load Data
# ----------------------------------------------
@st.cache_data
def load_data():
    happiness_df = pd.read_csv('WHR2024.csv')
    health_df = pd.read_csv('MentalHealthDataset.csv')
    worklife_df = pd.read_csv('mental_health_datafinaldata.csv')
    return happiness_df, health_df, worklife_df

happiness_df, health_df, worklife_df = load_data()

# ----------------------------------------------
# 1. Bubble Chart: GDP vs Happiness
# ----------------------------------------------
st.header("GDP vs Happiness (Bubble Size = Social Support)")

cleaned_df = happiness_df.dropna(subset=['Explained by: Social support'])

fig1 = px.scatter(
    cleaned_df,
    x='Explained by: Log GDP per capita',
    y='Ladder score',
    size='Explained by: Social support',
    color='Country name',
    hover_name='Country name',
    size_max=10,
    opacity=0.7,
    template='plotly_dark',
    title="<b></b>"
)

fig1.update_traces(marker=dict(line=dict(width=0.5, color='white')))
fig1.update_layout(
    title=dict(x=0.5, font=dict(size=20, family='Arial', color='white')),
    yaxis=dict(dtick=0.5, title='<b>Ladder Score</b>', gridcolor='rgba(255,255,255,0.2)'),
    xaxis_title="<b>GDP per Capita (Log)</b>",
    legend_title_text='<b>Country</b>',
    margin=dict(t=80, l=40, r=40, b=40)
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown(
    """
    <h3 style='color: #2E86C1;'>➔ Countries with higher GDP per capita tend to have higher happiness scores, and those with stronger social support systems generally achieve the greatest levels of well-being.</h3>
    """,
    unsafe_allow_html=True
)

st.divider()

# ----------------------------------------------
# 2. Treemap: Top Countries by Happiness Factors
# ----------------------------------------------
st.header("Treemap: Top Countries by Happiness Factors")

top20 = happiness_df.nlargest(20, 'Ladder score')
tree_df = top20[['Country name', 'Explained by: Log GDP per capita', 'Explained by: Social support', 'Explained by: Healthy life expectancy']]
tree_long = tree_df.melt(id_vars='Country name', var_name='Factor', value_name='Value')
tree_long['Factor'] = pd.Categorical(tree_long['Factor'],
                                     categories=['Explained by: Log GDP per capita', 'Explained by: Social support', 'Explained by: Healthy life expectancy'],
                                     ordered=True)

fig2 = px.treemap(tree_long,
                  path=['Factor', 'Country name'],
                  values='Value',
                  color='Value',
                  color_continuous_scale='YlGnBu')

fig2.update_traces(hovertemplate='<b>Country:</b> %{label}<br><b>Factor:</b> %{parent}<br><b>Contribution:</b> %{value:.2f}<extra></extra>',
                   marker=dict(line=dict(width=1.5, color='white')))
fig2.update_layout(
    title=dict(x=0.5, font=dict(size=20, family='Arial', color='black')),
    margin=dict(t=70, l=20, r=20, b=20)
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
    <h3 style='color: #2E86C1;'>➔ Among the ten happiest countries, economic prosperity (GDP) and strong social support contribute the most to happiness, while healthy life expectancy plays a smaller but still important role.</h3>
    """,
    unsafe_allow_html=True
)

st.divider()

# ----------------------------------------------
# 3. Violin Plot: Stress Levels by Gender
# ----------------------------------------------
st.header("Stress Levels by Gender - Violin Plot")

sampled_health_df = health_df.sample(n=3500, random_state=42)

fig3 = px.violin(
    sampled_health_df,
    x='Gender',
    y='Growing_Stress',
    color='Gender',
    box=True,
    points='all',
    template='simple_white',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title=" "
)

fig3.update_traces(
    jitter=0.5,
    marker=dict(size=6, opacity=0.5, line=dict(width=0.5, color='gray')),
    meanline_visible=True
)

fig3.update_layout(
    title=dict(x=0.5, font=dict(size=24, family='Verdana', color='#000000')),  
    xaxis_title="<b>Gender</b>",
    yaxis_title="<b>Growing Stress Level</b>",
    legend_title=dict(text="<b>Gender</b>", font=dict(color='#000000')),
    legend=dict(font=dict(color='#000000')),
    xaxis=dict(
        title_font=dict(size=18, family='Verdana', color='#000000'), 
        tickfont=dict(size=14, color='#000000')
    ),
    yaxis=dict(
        title_font=dict(size=18, family='Verdana', color='#000000'), 
        tickfont=dict(size=14, color='#000000')
    ),
    margin=dict(t=80, l=50, r=50, b=50),
    height=600,
    width=1000,
    font=dict(family="Verdana", size=15, color='#000000'),
    plot_bgcolor='rgba(240, 248, 255, 1)',
    paper_bgcolor='rgba(245, 245, 250, 1)'
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown(
    """
    <h3 style='color: #2E86C1;'>➔ Self-reported stress levels are very similar for males and females, with only a slight lean toward higher average stress among females, suggesting minimal gender differences in stress experiences.</h3>
    """,
    unsafe_allow_html=True
)

st.divider()

# ----------------------------------------------
# 4. Sankey Diagram: Work Hours vs Stress
# ----------------------------------------------
st.header("Interactive Sankey Diagram: Work Hours vs Stress Level")

stress_level_order = ['Low', 'Medium', 'High']
stress_level_labels = [f"{level} Stress" for level in stress_level_order]

stress_color_mapping = {
    'Low Stress': '#7ED957',
    'Medium Stress': '#FFC107',
    'High Stress': '#FF4C4C'
}

def prepare_sankey_data(grouped=True):
    if grouped:
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        bin_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
        worklife_df['Work_Hours_Grouped'] = pd.cut(worklife_df['Work_Hours'], bins=bins, labels=bin_labels, right=True)
        source_col = 'Work_Hours_Grouped'
        sorted_hours = bin_labels
        work_hours_labels = [f"{label} Hours" for label in sorted_hours]
    else:
        sorted_hours = sorted(worklife_df['Work_Hours'].unique())
        work_hours_labels = [f"{int(hour)} Hours" for hour in sorted_hours]
        source_col = 'Work_Hours'

    labels = work_hours_labels + stress_level_labels

    worklife_df[source_col] = pd.Categorical(worklife_df[source_col], categories=sorted_hours, ordered=True)
    worklife_df['Stress_Level_Sorted'] = pd.Categorical(worklife_df['Stress_Level'], categories=stress_level_order, ordered=True)

    value_counts = worklife_df.groupby([source_col, 'Stress_Level_Sorted']).size().reset_index(name='count')
    source_codes = value_counts[source_col].astype('category').cat.codes
    target_codes = value_counts['Stress_Level_Sorted'].astype('category').cat.codes + len(sorted_hours)

    link_colors = []
    for stress in value_counts['Stress_Level_Sorted']:
        if stress == 'Low':
            link_colors.append('rgba(126,217,87,0.5)')
        elif stress == 'Medium':
            link_colors.append('rgba(255,193,7,0.5)')
        else:
            link_colors.append('rgba(255,76,76,0.5)')

    work_hours_colors = ['#4A90E2'] * len(work_hours_labels)
    stress_colors = [stress_color_mapping[label] for label in stress_level_labels]
    node_colors = work_hours_colors + stress_colors

    return {
        'labels': labels,
        'node_colors': node_colors,
        'source': source_codes,
        'target': target_codes,
        'value': value_counts['count'],
        'link_colors': link_colors
    }

data_grouped = prepare_sankey_data(grouped=True)

fig4 = go.Figure(data=[go.Sankey(
    node=dict(pad=20, thickness=30, line=dict(color="black", width=1),
              label=data_grouped['labels'], color=data_grouped['node_colors']),
    link=dict(source=data_grouped['source'], target=data_grouped['target'],
              value=data_grouped['value'], color=data_grouped['link_colors'])
)])

fig4.update_layout(
    title_text="<b>Weekly Work Hours vs Stress Level Distribution</b>",
    font=dict(size=12, family='Arial'),
    height=700,
    margin=dict(l=20, r=20, t=80, b=20)
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown(
    """
    <h3 style='color: #2E86C1;'>➔ Regardless of how many hours people work, stress levels remain fairly mixed across low, medium, and high categories, with medium stress being the most common outcome across all work-hour ranges.</h3>
    """,
    unsafe_allow_html=True
)

st.divider()

# ----------------------------------------------
# 5. 3D Choropleth Globe: World Happiness Levels
# ----------------------------------------------
st.header("World Happiness Levels - 3D Globe View")

fig5 = go.Figure()

fig5.add_trace(go.Choropleth(
    locations=happiness_df['Country name'],
    locationmode='country names',
    z=happiness_df['Ladder score'],
    colorscale='Plasma',
    colorbar_title='<b>Happiness Index</b>',
    marker_line_color='black',
    marker_line_width=0.6,
    zmin=happiness_df['Ladder score'].min(),
    zmax=happiness_df['Ladder score'].max(),
    hovertemplate='<b>%{location}</b><br><b>Happiness Score:</b> %{z:.2f}<extra></extra>'
))

fig5.update_layout(
    geo=dict(
        showland=True,
        landcolor='rgb(250,250,250)',
        oceancolor='rgb(150,200,255)',
        showocean=True,
        showcountries=True,
        projection_type='orthographic',
        bgcolor='white',
        showframe=False
    ),
    coloraxis_colorbar=dict(
        title=dict(
            text='<b>Happiness Index</b>',
            font=dict(size=18, family='Arial', color='#000000')
        ),
        tickfont=dict(color='#000000')
    ),
    paper_bgcolor='white',
    margin=dict(l=0, r=0, t=50, b=0),
    font=dict(family="Arial", size=14, color='#000000')
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown(
    """
    <h3 style='color: #2E86C1;'>➔ Happiness levels vary widely across the world, with Northern European countries ranking the happiest and parts of South Asia and Africa showing much lower well-being, highlighting global inequality in happiness.</h3>
    """,
    unsafe_allow_html=True
)

