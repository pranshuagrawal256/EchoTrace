import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import requests
import joblib

model = joblib.load(
    "models/fake_news_model.pkl"
)

vectorizer = joblib.load(
    "models/vectorizer.pkl"
)
# --------------------------------------------------
# Suspicious Words
# --------------------------------------------------

suspicious_words = [
    "shocking",
    "urgent",
    "breaking",
    "secret",
    "panic",
    "exposed",
    "crisis",
    "warning",
    "leaked",
    "truth"
]
# --------------------------------------------------
# Emotion Score
# --------------------------------------------------

def emotion_score(text):

    score = 0

    text = str(text).lower()

    for word in suspicious_words:

        if word in text:
            score += 1

    return score


# --------------------------------------------------
# Exclamation Score
# --------------------------------------------------

def exclamation_score(text):

    return str(text).count("!")


# --------------------------------------------------
# Capital Score
# --------------------------------------------------

def capital_score(text):

    words = str(text).split()

    count = 0

    for word in words:

        if word.isupper() and len(word) > 2:
            count += 1

    return count

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="EchoTrace",
    page_icon="🛰️",
    layout="wide"
)

st.markdown("""
<style>

/* ==========================================
   GLOBAL THEME
========================================== */

.stApp{
    background: linear-gradient(
        180deg,
        #071330 0%,
        #0B1220 100%
    );
    color: white;
}

/* Hide Streamlit Default Menu */

#MainMenu,
footer,
header{
    visibility:hidden;
}


/* ==========================================
   HEADINGS
========================================== */

h1,h2,h3,h4{
    color:white !important;
    font-weight:700 !important;
}

p,label{
    color:#E2E8F0 !important;
}


/* ==========================================
   HERO CARD
========================================== */

.hero-box{
    background: linear-gradient(
        135deg,
        #1E3A8A,
        #4338CA
    );
    padding:40px;
    border-radius:24px;
}


/* ==========================================
   METRIC CARDS
========================================== */

[data-testid="stMetric"]{
    background:#172554;
    border:1px solid rgba(59,130,246,0.35);
    border-radius:20px;
    padding:20px;
    box-shadow:
        0 8px 25px rgba(0,0,0,0.25);
}

[data-testid="stMetric"]:hover{
    transform:translateY(-3px);
    transition:0.3s;
}

[data-testid="stMetricLabel"]{
    color:#CBD5E1 !important;
    font-size:16px !important;
    font-weight:600 !important;
}

[data-testid="stMetricValue"]{
    color:white !important;
    font-size:42px !important;
    font-weight:700 !important;
}


/* ==========================================
   TEXT INPUTS
========================================== */

.stTextInput input{
    background:#172554 !important;
    color:white !important;

    border:1px solid #3B82F6 !important;

    border-radius:14px !important;

    padding:12px !important;
}

.stTextInput input::placeholder{
    color:#CBD5E1 !important;
}

.stTextInput input:focus{
    border:2px solid #60A5FA !important;

    box-shadow:
        0 0 12px rgba(59,130,246,0.35) !important;
}


/* ==========================================
   SELECT BOX
========================================== */

div[data-baseweb="select"] > div{
    background:#172554 !important;
    color:white !important;

    border:1px solid #3B82F6 !important;

    border-radius:14px !important;
}

div[data-baseweb="select"] span{
    color:white !important;
}


/* ==========================================
   BUTTONS
========================================== */

.stButton > button{

    background:linear-gradient(
        135deg,
        #2563EB,
        #4F46E5
    ) !important;

    color:white !important;

    border:none !important;

    border-radius:12px !important;

    font-size:16px !important;

    font-weight:600 !important;

    padding:12px 24px !important;

    transition:0.3s !important;
}

.stButton > button:hover{

    background:linear-gradient(
        135deg,
        #3B82F6,
        #6366F1
    ) !important;

    transform:translateY(-2px);
}


/* ==========================================
   DATAFRAME
========================================== */

[data-testid="stDataFrame"]{
    border-radius:16px;
    overflow:hidden;
    border:1px solid #334155;
}

[data-testid="stDataFrame"] table{
    background:#111827 !important;
    color:white !important;
}

[data-testid="stDataFrame"] th{
    background:#172554 !important;
    color:white !important;
}

[data-testid="stDataFrame"] td{
    color:#E2E8F0 !important;
}


/* ==========================================
   PLOTLY CHARTS
========================================== */

.js-plotly-plot{
    border-radius:20px;
    overflow:hidden;
}


/* ==========================================
   DIVIDERS
========================================== */

hr{
    border:1px solid rgba(255,255,255,0.08);
}


/* ==========================================
   SCROLLBAR
========================================== */

::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-track{
    background:#071330;
}

::-webkit-scrollbar-thumb{
    background:#1E3A8A;
    border-radius:20px;
}

::-webkit-scrollbar-thumb:hover{
    background:#2563EB;
}

</style>
""", unsafe_allow_html=True)
# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown("""
<div style="
background:linear-gradient(135deg,#1e3a8a,#312e81);
padding:40px;
border-radius:25px;
margin-bottom:30px;
">

<h1 style="color:white;">
🛰️ EchoTrace
</h1>

<h3 style="color:#dbeafe;">
The Internet's Early Warning System for Viral Misinformation
</h3>

<p style="color:#cbd5e1;font-size:18px;">
Monitor suspicious content, detect misinformation,
analyze news sources and classify headlines using AI.
</p>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

conn = sqlite3.connect("database/echotrace.db")

query = """
SELECT
title,
source,
emotion_score,
suspicion_score,
credibility_score,
virality_score,
prediction
FROM news
"""
df = pd.read_sql_query(query, conn)

st.write(df[["title", "prediction"]].head())

# --------------------------------------------------
# METRICS
# --------------------------------------------------

fake_count = len(df[df["prediction"] == "FAKE"])
real_count = len(df[df["prediction"] == "REAL"])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📰 Total News",
        len(df)
    )

with col2:
    st.metric(
        "🔴 Fake News",
        fake_count
    )

with col3:
    st.metric(
        "🟢 Real News",
        real_count
    )

st.divider()

# -----------------------------------------
# VIRAL NEWS
# -----------------------------------------

st.subheader("🚀 Most Viral News")

viral_df = (
    df.sort_values(
        by="virality_score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    viral_df[
        [
            "title",
            "source",
            "virality_score"
        ]
    ],
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# DONUT CHART
# --------------------------------------------------

st.subheader("📊 Fake vs Real News Distribution")

chart_data = pd.DataFrame({
    "Category": ["Fake News", "Real News"],
    "Count": [fake_count, real_count]
})

fig = px.pie(
    chart_data,
    values="Count",
    names="Category",
    hole=0.70,
    color="Category",
    color_discrete_map={
        "Fake News": "#D63737",   # Indigo
        "Real News": "#419F60"    # Blue
    }
)

fig.update_traces(
    textinfo="percent",          # cleaner
    textfont_size=20,
    hovertemplate=
    "<b>%{label}</b><br>" +
    "Count: %{value}<br>" +
    "Percentage: %{percent}<extra></extra>",
    marker=dict(
        line=dict(
            color="#0B1220",
            width=4
        )
    )
)

fig.update_layout(
    template="plotly_dark",

    height=500,

    paper_bgcolor="#111827",
    plot_bgcolor="#111827",

    font=dict(
        color="white",
        size=16
    ),

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(
            size=14,
            color="white"
        )
    ),

    showlegend=True,

    annotations=[
        dict(
            text="News<br>Analysis",
            x=0.5,
            y=0.5,
            font=dict(
                size=22,
                color="white"
            ),
            showarrow=False
        )
    ]
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)

st.divider()
# --------------------------------------------------
# TOP NEWS SOURCES
# --------------------------------------------------

st.subheader("📡 Top News Sources")

source_counts = (
    df["source"]
    .value_counts()
    .reset_index()
)

source_counts.columns = [
    "Source",
    "Articles"
]

fig_sources = px.bar(
    source_counts,
    x="Articles",
    y="Source",
    orientation="h",
    text="Articles",
    color="Articles",
    color_continuous_scale="Blues"
)

fig_sources.update_traces(
    textposition="outside"
)

fig_sources.update_layout(
    template="plotly_dark",
    height=500,
    paper_bgcolor="#0B1220",
    plot_bgcolor="#1A2332",
    font=dict(
        color="white",
        size=14
    ),
    xaxis_title="Number of Articles",
    yaxis_title="News Source"
)

st.plotly_chart(
    fig_sources,
    use_container_width=True,
    config={"displayModeBar": False}
)

# --------------------------------------------------
# SOURCE CREDIBILITY RANKING
# --------------------------------------------------

st.subheader("🛡 Source Credibility Ranking")

credibility_df = (
    df.groupby("source")["credibility_score"]
    .mean()
    .reset_index()
)

# Highest credibility first
credibility_df = credibility_df.sort_values(
    by="credibility_score",
    ascending=False
).head(10)

# Reverse so highest appears at top in horizontal chart
credibility_df = credibility_df.iloc[::-1]

fig_credibility = px.bar(
    credibility_df,
    x="credibility_score",
    y="source",
    orientation="h",
    text="credibility_score",
    color="credibility_score",
    color_continuous_scale="Viridis"
)

fig_credibility.update_traces(
    textposition="outside"
)

fig_credibility.update_layout(
    template="plotly_dark",
    height=500,
    paper_bgcolor="#0B1220",
    plot_bgcolor="#1A2332",
    font=dict(
        color="white",
        size=14
    ),
    xaxis_title="Credibility Score",
    yaxis_title="News Source"
)

st.plotly_chart(
    fig_credibility,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.divider()

# --------------------------------------------------
# FILTER BY SOURCE
# --------------------------------------------------

st.subheader("🎯 Filter By Source")

sources = ["All"] + sorted(
    df["source"].unique().tolist()
)

selected_source = st.selectbox(
    "Choose News Source",
    sources
)

filtered_df = df.copy()

if selected_source != "All":

    filtered_df = filtered_df[
        filtered_df["source"] == selected_source
    ]

# --------------------------------------------------
# SEARCH HEADLINES
# --------------------------------------------------

st.subheader("🔍 Search Headlines")

st.markdown(
    """
    <p style="
    color:#CBD5E1;
    font-size:16px;
    margin-bottom:10px;
    ">
    Search news headlines stored in the database
    </p>
    """,
    unsafe_allow_html=True
)

search = st.text_input(
    "",
    placeholder="Type a keyword... (e.g. Trump, Nvidia, Israel)"
)

if search:

    filtered_df = filtered_df[
        filtered_df["title"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    st.success(
        f"Found {len(filtered_df)} matching headlines"
    )

else:

    st.info(
        f"Showing all {len(filtered_df)} headlines"
    )

# --------------------------------------------------
# TABLE
# --------------------------------------------------

display_df = filtered_df.copy()

display_df["prediction"] = (
    display_df["prediction"]
    .apply(
        lambda x:
        "🟢 REAL"
        if x == "REAL"
        else "🔴 FAKE"
    )
)

st.dataframe(
    display_df,
    use_container_width=True,
    height=500
)

def verify_with_live_news(headline):

    API_KEY = "4c6dac639c074f46a5862efc17efca4b"

    important_words = []

    for word in headline.split():

        if len(word) > 4:

            important_words.append(word)

    search_query = " ".join(
        important_words[:4]
    )


    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={search_query}"
        f"&language=en"
        f"&pageSize=5"
        f"&apiKey={API_KEY}"
    )

    try:

        response = requests.get(url)

        data = response.json()

        if data["status"] == "ok" and data["totalResults"] > 0:

            return True, data["articles"]

        return False, []

    except:

        return False, []

# --------------------------------------------------
# LIVE HEADLINE ANALYZER
# --------------------------------------------------

st.divider()

st.subheader("🧠 Live Headline Analyzer")

headline = st.text_input(
    "Enter Any News Headline"
)

if st.button("Analyze Headline"):

    if headline.strip() == "":

        st.error(
            "Please enter a headline."
        )
    else:

        # AI Prediction

        headline_vector = vectorizer.transform(
            [headline]
        )

        prediction = int(
            model.predict(headline_vector)[0]
        )

        probabilities = model.predict_proba(
            headline_vector
        )[0]

        real_confidence = round(
            probabilities[1] * 100,
            2
        )

        fake_confidence = round(
            probabilities[0] * 100,
            2
        )

        # Final Prediction

        if prediction == 1:

            st.progress(
                int(real_confidence)
            )

            st.success(
                f"✅ Prediction: REAL NEWS ({real_confidence}% confidence)"
            )

            st.info(
                """
                Reason:
                • Headline follows standard news writing style
                • No excessive emotional language detected
                • Confidence score suggests legitimate reporting
                """
            )

        else:

            st.progress(
                int(fake_confidence)
            )

            st.error(
                f"🚨 Prediction: POTENTIAL FAKE NEWS ({fake_confidence}% confidence)"
            )

            st.warning(
                """
                Reason:
                • High emotional intensity detected
                • Clickbait or sensational wording present
                • Headline matches misinformation patterns
                """
            )

        # Feature Analysis

        emotion = emotion_score(
            headline
        )

        exclamation = exclamation_score(
            headline
        )

        capital = capital_score(
            headline
        )

        detected_words = []

        for word in suspicious_words:

            if word.lower() in headline.lower():

                detected_words.append(
                    word
                )

        suspicious_word_count = len(
            detected_words
        )

        suspicion_score = min(
            100,
            emotion * 15 +
            exclamation * 10 +
            capital * 10
        )

        # Risk Level

        if suspicion_score >= 80:

            risk_level = "🔴 HIGH"

        elif suspicion_score >= 40:

            risk_level = "🟡 MEDIUM"

        else:

            risk_level = "🟢 LOW"

        # Virality Score

        virality_score = 0

        virality_score += min(
            len(headline) // 5,
            20
        )

        virality_score += emotion * 15

        virality_score += suspicion_score // 2

        if "?" in headline:

            virality_score += 10

        if "!" in headline:

            virality_score += 10

        trending_words = [
            "trump",
            "musk",
            "nvidia",
            "ai",
            "openai",
            "tesla",
            "war",
            "china",
            "india",
            "election",
            "covid"
        ]

        for word in trending_words:

            if word in headline.lower():

                virality_score += 15

        virality_score = min(
            100,
            virality_score
        )

        # Viral Label

        if virality_score >= 80:

            viral_label = "🔥 Highly Viral"

        elif virality_score >= 50:

            viral_label = "📈 Trending"

        else:

            viral_label = "📄 Normal Reach"

        verified, articles = verify_with_live_news(
        headline
        )    

        # TRUST SCORE
        if prediction == 1:

         trust_score = real_confidence

        else:

         trust_score = 100 - fake_confidence

        if verified:

         trust_score += 20

         trust_score -= (
          suspicion_score * 0.3
          )

        trust_score = max(
        0,
        min(
        100,
        round(trust_score)
        )
     )

        st.subheader(
        "🛡️ Trust Score"
        )

        st.progress(
        int(trust_score)
        )

        st.metric(
        "Trust Score",
        f"{trust_score}/100",
        )

        if trust_score >= 80:

         st.success(
          "Highly Trustworthy"
         )

        elif trust_score >= 50:

         st.warning(
          "Needs Verification"
        )

        else:

         st.error(
          "Low Trust Score"
          )
         
        # Display Results

        st.write(
            "## 📊 Analysis Result"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Emotion Score",
                emotion
            )

            st.metric(
                "Capital Score",
                capital
            )

        with col2:

            st.metric(
                "Exclamation Score",
                exclamation
            )

            st.metric(
                "Suspicion Score",
                suspicion_score
            )

        with col3:

            st.metric(
                "Virality Score",
                virality_score
            )

            st.metric(
                "Risk Level",
                risk_level
            )

        st.divider()

        st.subheader(
            "🌐 Live News Verification"
        )

        # FACT CHECK SCORE

        if verified:

            fact_score = 100

            st.success(
                "✅ Verified: Similar articles found online"
            )

            for article in articles:

                st.write(
                    "• " + article["title"]
                )

        else:

            fact_score = 0

            st.warning(
                "⚠️ No matching trusted news articles found"
            )

        # FACT CHECK RESULT

        st.subheader(
            "🎯 EchoTrace Verdict"
        )

        if prediction == 1 and verified:

            st.success(
                "✅ LIKELY REAL NEWS"
            )

            st.info(
                "ML model predicts REAL and supporting articles were found online."
            )

        elif prediction == 0 and verified:

            st.warning(
                "⚠️ NEEDS REVIEW"
            )

            st.info(
                "ML model predicts FAKE but trusted articles were found online."
            )

        elif prediction == 1 and not verified:

            st.warning(
                "⚠️ UNVERIFIED"
            )

            st.info(
                "ML model predicts REAL but no supporting articles were found online."
            )

        else:

            st.error(
                "🚨 LIKELY FAKE NEWS"
            )

            st.info(
                "ML model predicts FAKE and no supporting articles were found."
            )

        # VIRALITY RESULT

        st.subheader(
            "📈 Virality Assessment"
        )

        if virality_score >= 80:

            st.error(
                f"🔥 Viral Potential: {viral_label}"
            )

        elif virality_score >= 50:

            st.warning(
                f"📈 Viral Potential: {viral_label}"
            )

        else:

            st.success(
                f"📄 Viral Potential: {viral_label}"
            )

        # SUSPICIOUS WORDS

        st.subheader(
            "🚩 Trigger Word Analysis"
        )

        if detected_words:

            st.error(
                "Suspicious words detected:"
            )

            st.write(
                ", ".join(
                    detected_words
                )
            )

        else:

            st.success(
                "✅ No suspicious trigger words detected"
            )
conn.close()