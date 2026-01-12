import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="New Year's Resolution Dashboard", layout="wide")

# Title
st.title("New Year's Resolution Challenge 2026")


# Load data
@st.cache_data
def load_data():
    """Load all three CSV files"""
    pullups = pd.read_csv('pullups_data.csv')
    jokes = pd.read_csv('dadjokes_data.csv')
    vocab = pd.read_csv('vocabulary_data.csv')
    return pullups, jokes, vocab


# Load the data
pullups_df, jokes_df, vocab_df = load_data()

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["Overall Comparison", "Individual Insight", "Animated Progress Race"])

# -----------------------------
# TAB 1: OVERALL COMPARISON
# -----------------------------
with tab1:
    st.markdown("Compare all five friends across all categories")

    # Calculate totals/averages for all categories
    # Pull-ups: Average per day
    avg_pullups = pullups_df.groupby('student_name')['pullups'].mean()

    # Dad jokes: Weighted laughter score (LMAO=2, LOL=1)
    jokes_with_score: pd.DataFrame = jokes_df.copy()
    jokes_with_score['score'] = jokes_with_score['reaction'].map({
        '😂 LMAO': 2,
        '😆 LOL': 1,
        '😐 STRAIGHT FACE': 0,
        '😠 ANGRY': 0,
        '😞 DISAPPOINTED': 0
    })
    laughter_scores = jokes_with_score.groupby('student_name')['score'].sum()

    # Vocabulary: Cumulative total
    total_vocab = vocab_df.groupby('student_name')['flashcards_solved'].sum()

    # Create three separate bar charts
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Pull-ups")
        fig_pullups = px.bar(
            avg_pullups,
            x=avg_pullups.index,
            y=avg_pullups.values,
            color=avg_pullups.index,
            title='Average Pull-ups per Day',
            labels={'x': 'Student', 'y': 'Avg Pull-ups', 'index': 'Student'},
            template='plotly_white'
        )
        fig_pullups.update_layout(showlegend=False, height=400)
        fig_pullups.update_xaxes(title_text='Student')
        st.plotly_chart(fig_pullups, width="stretch")

    with col2:
        st.subheader("Dad Jokes")
        fig_jokes = px.bar(
            laughter_scores,
            x=laughter_scores.index,
            y=laughter_scores.values,
            color=laughter_scores.index,
            title='Laughter Score (LMAO=2, LOL=1)',
            labels={'x': 'Student', 'y': 'Score', 'index': 'Student'},
            template='plotly_white'
        )
        fig_jokes.update_layout(showlegend=False, height=400)
        fig_jokes.update_xaxes(title_text='Student')
        st.plotly_chart(fig_jokes, width="stretch")

    with col3:
        st.subheader("Vocabulary")
        fig_vocab = px.bar(
            total_vocab,
            x=total_vocab.index,
            y=total_vocab.values,
            color=total_vocab.index,
            title='Total Flashcards',
            labels={'x': 'Student', 'y': 'Flashcards', 'index': 'Student'},
            template='plotly_white'
        )
        fig_vocab.update_layout(showlegend=False, height=400)
        fig_vocab.update_xaxes(title_text='Student')
        st.plotly_chart(fig_vocab, width="stretch")

    # Summary insights
    st.markdown("---")
    st.subheader("Key Insights")
    st.markdown(f"""
    - **They protec:** Koriand'r (11.5 avg per day)
    - **They make you laugh:** Harmoney (14 laughter points - 6 LMAO + 2 LOL!)
    - **They will write poetry about you:** X Æ A-Xii (300+ cumulative flashcards)

    **Metrics Explained:**
    - Pull-ups: Average per day 
    - Dad Jokes: Weighted laughter score (LMAO=2 points, LOL=1 point)
    - Vocabulary: Cumulative total 
    """)

# -----------------------------
# TAB 2: INDIVIDUAL INSIGHT
# -----------------------------
with tab2:
    # Sidebar filters for this tab
    with st.sidebar:
        st.header("Individual Insight Filters")

        students = pullups_df['student_name'].unique()
        selected_student = st.selectbox(
            "Choose a student:",
            options=students
        )

        category = st.radio(
            "Choose a category:",
            options=["Pull-ups", "Dad Jokes", "Vocabulary Flashcards"]
        )

    # Filter data based on selected student and category
    if category == "Pull-ups":
        filtered_data = pullups_df[pullups_df['student_name'] == selected_student].copy()
        y_column = 'pullups'
        y_label = 'Pull-ups Completed'

        # Create line chart
        fig_progress = px.line(
            filtered_data,
            x='date',
            y=y_column,
            markers=True,
            title=f"{selected_student}'s {category} Progress Over Time",
            labels={'date': 'Date', y_column: y_label},
            template='plotly_white'
        )

        # Customize appearance
        fig_progress.update_traces(
            line_color='#4ECDC4',
            marker=dict(size=10, color='#FF6B6B')
        )
        fig_progress.update_layout(font=dict(size=12))

        st.plotly_chart(fig_progress, width="stretch")

        # Show statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", filtered_data[y_column].sum())
        with col2:
            st.metric("Average per Day", f"{filtered_data[y_column].mean():.1f}")
        with col3:
            st.metric("Best Day", filtered_data[y_column].max())

    elif category == "Dad Jokes":
        filtered_data = jokes_df[jokes_df['student_name'] == selected_student].copy()

        if len(filtered_data) == 0:
            st.warning(f"{selected_student} hasn't told any jokes yet!")
        else:
            # Calculate laughter score
            filtered_data['score'] = filtered_data['reaction'].map({
                '😂 LMAO': 2,
                '😆 LOL': 1,
                '😐 STRAIGHT FACE': 0,
                '😠 ANGRY': 0,
                '😞 DISAPPOINTED': 0
            })

            total_score = filtered_data['score'].sum()

            col1, col2 = st.columns([1, 1])

            with col1:
                # Pie chart of reactions
                reaction_counts = filtered_data['reaction'].value_counts()
                fig_pie = px.pie(
                    values=reaction_counts.values,
                    names=reaction_counts.index,
                    title=f"{selected_student}'s Joke Reactions",
                    template='plotly_white'
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, width="stretch")

            with col2:
                st.metric("Total Jokes Told", len(filtered_data))
                st.metric("Laughter Score", f"{total_score} points")
                st.metric("Success Rate", f"{(filtered_data['score'] > 0).sum() / len(filtered_data) * 100:.0f}%")

            # List funniest jokes (LMAO reactions)
            st.subheader("Funniest Jokes (LMAO Reactions)")
            lmao_jokes = filtered_data[filtered_data['reaction'] == '😂 LMAO']

            if len(lmao_jokes) > 0:
                for idx, row in lmao_jokes.iterrows():
                    st.markdown(f"**{row['date']}** - {row['dad_joke']} 😂")
            else:
                st.info("No LMAO reactions yet. Keep trying!")

            # List all jokes
            st.subheader("All Jokes")
            for idx, row in filtered_data.iterrows():
                st.markdown(f"**{row['date']}** ({row['reaction']}) - {row['dad_joke']}")

    elif category == "Vocabulary Flashcards":
        filtered_data = vocab_df[vocab_df['student_name'] == selected_student].copy()
        y_column = 'flashcards_solved'
        y_label = 'Flashcards Solved'

        # Create line chart
        fig_progress = px.line(
            filtered_data,
            x='date',
            y=y_column,
            markers=True,
            title=f"{selected_student}'s {category} Progress Over Time",
            labels={'date': 'Date', y_column: y_label},
            template='plotly_white'
        )

        # Customize appearance
        fig_progress.update_traces(
            line_color='#4ECDC4',
            marker=dict(size=10, color='#FF6B6B')
        )
        fig_progress.update_layout(font=dict(size=12))

        st.plotly_chart(fig_progress, width="stretch")

        # Show statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", filtered_data[y_column].sum())
        with col2:
            st.metric("Average per Day", f"{filtered_data[y_column].mean():.1f}")
        with col3:
            st.metric("Best Day", filtered_data[y_column].max())

# -----------------------------
# TAB 3: ANIMATED PROGRESS RACE
# -----------------------------
with tab3:
    # Sidebar filter for this tab
    with st.sidebar:

        st.markdown("---")
        st.header("Animation Race Filter")

        race_category = st.radio(
            "Choose a category to race:",
            options=["Pull-ups", "Dad Jokes", "Vocabulary Flashcards"],
            key="race_category"
        )

    st.markdown(f"Watch all five friends compete in: **{race_category}**")

    # Prepare animation data based on category
    if race_category == "Pull-ups":
        # For pull-ups, calculate daily average (cumulative sum / number of days)
        animation_data = pullups_df.copy()
        animation_data = animation_data.sort_values('date')
        animation_data['cumulative_sum'] = animation_data.groupby('student_name')['pullups'].cumsum()
        animation_data['day_count'] = animation_data.groupby('student_name').cumcount() + 1
        animation_data['cumulative'] = animation_data['cumulative_sum'] / animation_data['day_count']
        y_label = 'Average Pull-ups per Day'
        max_value = 12
    elif race_category == "Dad Jokes":
        # For jokes, count weighted laughter score: LMAO = 2 points, LOL = 1 point
        # Create score column
        jokes_with_score = jokes_df.copy()
        jokes_with_score['score'] = jokes_with_score['reaction'].map({
            '😂 LMAO': 2,
            '😆 LOL': 1,
            '😐 STRAIGHT FACE': 0,
            '😠 ANGRY': 0,
            '😞 DISAPPOINTED': 0
        })

        # Create a complete timeline for all students
        all_dates = jokes_df['date'].unique()
        all_students = jokes_df['student_name'].unique()

        # Create a frame for each date showing cumulative laughter score
        animation_frames = []
        for date in sorted(all_dates):
            for student in all_students:
                jokes_up_to_date = jokes_with_score[
                    (jokes_with_score['student_name'] == student) &
                    (jokes_with_score['date'] <= date)
                    ]
                animation_frames.append({
                    'date': date,
                    'student_name': student,
                    'cumulative': jokes_up_to_date['score'].sum()
                })

        animation_data = pd.DataFrame(animation_frames)
        y_label = 'Laughter Score (LMAO=2, LOL=1)'
        max_value = 16
    elif race_category == "Vocabulary Flashcards":
        animation_data = vocab_df.copy()
        animation_data['cumulative'] = animation_data.groupby('student_name')['flashcards_solved'].cumsum()
        y_label = 'Cumulative Flashcards'
        max_value = 300

    # Create animated bar chart
    fig_animated = px.bar(
        animation_data,
        x='student_name',
        y='cumulative',
        color='student_name',
        animation_frame='date',
        animation_group='student_name',
        range_y=[0, max_value],
        title=f'{race_category} Race: Cumulative Progress Over 12 Days',
        labels={'student_name': 'Student', 'cumulative': y_label},
        template='plotly_white'
    )

    # Update x-axis label
    fig_animated.update_xaxes(title_text='Student')

    # Customize animation speed
    fig_animated.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 800
    fig_animated.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 500

    # Update layout
    fig_animated.update_layout(font=dict(size=12), height=600)

    st.plotly_chart(fig_animated, width="stretch")

    # Instructions
    st.info("**Instructions:** Click the play button on the chart to watch the race unfold day by day!")

    # Winner announcement
    winner = animation_data.groupby('student_name')['cumulative'].max().idxmax()
    winner_score = animation_data.groupby('student_name')['cumulative'].max().max()

    if race_category == "Pull-ups":
        st.success(f"**The one with muscles:** {winner} with {winner_score:.1f} average pull-ups per day!")
    elif race_category == "Dad Jokes":
        st.success(f"**The one with jokes:** {winner} with {winner_score:.0f} laughter points (LMAO=2, LOL=1)!")
    else:
        st.success(f"**The one with brain cells:** {winner} with {winner_score:.0f} total!")

# -----------------------------
# BONUS: EXPLORE THE DATA
# -----------------------------
with st.expander("Explore the Raw Data"):
    st.subheader("Pull-ups Data")
    st.dataframe(pullups_df)

    st.subheader("Dad Jokes Data")
    st.dataframe(jokes_df)

    st.subheader("Vocabulary Data")
    st.dataframe(vocab_df)

# Footer
st.markdown("---")
st.markdown("**New Year's Resolution Challenge 2026** | Programming for EduTech Week 12")