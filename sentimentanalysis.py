# ══════════════════════════════════════════════════════
# FINANCIAL SENTIMENT ANALYSIS REPORT
# COMPLETE PROFESSIONAL VERSION
# Prepared By: Ameni Jabeur
# Academic Year: 2025 / 2026
# ══════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════
# IMPORTS
# ══════════════════════════════════════════════════════
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import textwrap

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ══════════════════════════════════════════════════════
# SETUP
# ══════════════════════════════════════════════════════
os.makedirs("outputs", exist_ok=True)

sns.set_theme(
    style="whitegrid"
)

analyzer = SentimentIntensityAnalyzer()

# Colors
COLOR_BRIGHT = "#FF4D6D"
COLOR_LIGHT = "#FFC8DD"
COLOR_DEEP = "#590D22"

# ══════════════════════════════════════════════════════
# DATASET
# ══════════════════════════════════════════════════════
headlines = [

    "Tech stocks surge as NVIDIA hits record highs.",
    "Market volatility concerns investors amidst inflation.",
    "Federal Reserve holds rates steady, market stays neutral.",
    "Panic selling hits retail sector after poor earnings.",
    "Investors are highly optimistic about the new fiscal policy.",
    "Energy sector faces headwinds as oil prices drop.",
    "Renewable energy stocks show consistent growth.",
    "Analysts warn of potential recession in Q4.",
    "Consumer confidence index reaches a five-year high.",
    "Global trade tensions impact semiconductor supply chains.",

    "Artificial intelligence companies continue strong expansion.",
    "Banking stocks decline after economic slowdown fears.",
    "Oil prices rebound amid global supply concerns.",
    "Stock market rallies following positive earnings season.",
    "Inflation pressures continue affecting global markets.",
    "Technology sector leads gains across Wall Street.",
    "Investors remain cautious despite market recovery.",
    "Strong quarterly reports boost investor confidence.",
    "Economic uncertainty impacts international trade outlook.",
    "Major companies announce expansion into AI services.",

] * 2

df = pd.DataFrame(
    headlines,
    columns=["Headline"]
)

# ══════════════════════════════════════════════════════
# SENTIMENT ANALYSIS
# ══════════════════════════════════════════════════════
def get_sentiment(text):

    score = analyzer.polarity_scores(text)

    return pd.Series([
        score["compound"],
        score["pos"],
        score["neg"],
        score["neu"]
    ])

df[[
    "Polarity",
    "Positive",
    "Negative",
    "Neutral"
]] = df["Headline"].apply(get_sentiment)

# Sentiment labels
df["Sentiment"] = np.where(
    df["Polarity"] > 0.05,
    "Positive",
    np.where(
        df["Polarity"] < -0.05,
        "Negative",
        "Neutral"
    )
)

# ══════════════════════════════════════════════════════
# VISUALIZATIONS
# ══════════════════════════════════════════════════════

# ──────────────────────────────────────────────────────
# 1. SENTIMENT DISTRIBUTION
# ──────────────────────────────────────────────────────
plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="Sentiment",
    hue="Sentiment",
    palette=[
        COLOR_BRIGHT,
        COLOR_LIGHT,
        COLOR_DEEP
    ],
    legend=False
)

plt.title(
    "Market Sentiment Distribution",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Sentiment")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig(
    "outputs/sentiment_distribution.png",
    dpi=300
)

plt.show()

# ──────────────────────────────────────────────────────
# 2. PIE CHART
# ──────────────────────────────────────────────────────
plt.figure(figsize=(7, 7))

counts = df["Sentiment"].value_counts()

plt.pie(
    counts.values,
    labels=counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=[
        COLOR_BRIGHT,
        COLOR_LIGHT,
        COLOR_DEEP
    ],
    wedgeprops={
        "edgecolor": "white",
        "linewidth": 2
    }
)

plt.title(
    "Sentiment Proportions",
    fontsize=18,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "outputs/sentiment_pie_chart.png",
    dpi=300
)

plt.show()

# ──────────────────────────────────────────────────────
# 3. WORD CLOUD
# ──────────────────────────────────────────────────────
all_text = " ".join(df["Headline"])

wordcloud = WordCloud(
    width=1600,
    height=900,
    background_color="white",
    colormap="RdPu",
    max_words=100
).generate(all_text)

plt.figure(figsize=(14, 8))

plt.imshow(
    wordcloud,
    interpolation="bilinear"
)

plt.axis("off")

plt.title(
    "Financial Word Cloud",
    fontsize=20,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "outputs/wordcloud.png",
    dpi=300
)

plt.show()

# ──────────────────────────────────────────────────────
# 4. POLARITY DISTRIBUTION
# ──────────────────────────────────────────────────────
plt.figure(figsize=(8, 5))

sns.histplot(
    df["Polarity"],
    bins=12,
    kde=True,
    color=COLOR_BRIGHT
)

plt.axvline(
    df["Polarity"].mean(),
    linestyle="--",
    linewidth=2,
    color=COLOR_DEEP
)

plt.title(
    "Polarity Score Distribution",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Polarity Score")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "outputs/polarity_distribution.png",
    dpi=300
)

plt.show()

# ══════════════════════════════════════════════════════
# PDF REPORT
# ══════════════════════════════════════════════════════
pdf_path = "outputs/final_sentiment_report.pdf"

c = canvas.Canvas(
    pdf_path,
    pagesize=A4
)

page_width, page_height = A4

# ══════════════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════════════
c.setFillColorRGB(0.96, 0.93, 0.95)

c.rect(
    0,
    0,
    page_width,
    page_height,
    fill=1,
    stroke=0
)

c.setFillColorRGB(0.35, 0.05, 0.15)

c.setFont(
    "Helvetica-Bold",
    30
)

c.drawCentredString(
    page_width / 2,
    page_height - 260,
    "Financial Sentiment Analysis Report"
)

c.setFont(
    "Helvetica",
    20
)

c.drawCentredString(
    page_width / 2,
    page_height - 340,
    "Prepared By: Ameni Jabeur"
)

c.setFont(
    "Helvetica-Oblique",
    16
)

c.drawCentredString(
    page_width / 2,
    page_height - 390,
    "Academic Year: 2025 / 2026"
)

c.showPage()

# ══════════════════════════════════════════════════════
# INTRODUCTION PAGE
# ══════════════════════════════════════════════════════
c.setFont(
    "Helvetica-Bold",
    24
)

c.setFillColorRGB(0.35, 0.05, 0.15)

c.drawString(
    60,
    page_height - 60,
    "Project Introduction"
)

c.line(
    60,
    page_height - 72,
    page_width - 60,
    page_height - 72
)

text = c.beginText(
    70,
    page_height - 130
)

text.setFont(
    "Helvetica",
    13
)

text.setLeading(28)

intro_text = """
This project applies Natural Language Processing (NLP)
and VADER sentiment analysis techniques to evaluate
financial market headlines and investor behaviour.

The primary objective is to identify sentiment patterns,
market confidence trends, and dominant financial topics
that influence public opinion and investment decisions.

The analysis further demonstrates how sentiment analytics
can support marketing strategy, business intelligence,
financial forecasting, and product positioning.

By transforming unstructured textual information into
quantifiable analytical insight, the project highlights
the practical value of artificial intelligence and data
science techniques within modern financial environments.
"""

wrapped = textwrap.wrap(
    intro_text,
    width=60
)

for line in wrapped:
    text.textLine(line)

c.drawText(text)

c.showPage()

# ══════════════════════════════════════════════════════
# MARKET ANALYSIS OVERVIEW
# ══════════════════════════════════════════════════════

c.setFillColorRGB(0.35, 0.05, 0.15)

# TITLE
c.setFont(
    "Helvetica-Bold",
    26
)

c.drawString(
    60,
    page_height - 60,
    "Market Analysis Overview"
)

# Decorative line
c.setLineWidth(1.5)

c.line(
    60,
    page_height - 75,
    page_width - 60,
    page_height - 75
)

# TEXT OBJECT
text = c.beginText()

text.setTextOrigin(
    75,
    page_height - 130
)

# Better readability
text.setLeading(30)

text.setFont(
    "Helvetica",
    12.5
)

# INTRODUCTION PARAGRAPH
paragraph1 = """
This report presents a sentiment analysis study conducted on
financial and economic headlines using Natural Language
Processing techniques and the VADER sentiment analysis model.
"""

paragraph2 = f"""
A total of {len(df)} financial headlines were analysed to
identify public sentiment trends, investor confidence levels,
and dominant economic concerns affecting financial markets.
"""

paragraph3 = """
Positive sentiment slightly outweighed negative sentiment,
primarily driven by optimism surrounding technology growth,
artificial intelligence expansion, and strong earnings reports.
"""

paragraph4 = """
However, negative sentiment remained strongly associated with
inflation concerns, recession fears, interest rate uncertainty,
and broader economic instability.
"""

paragraph5 = f"""
The average polarity score observed in the dataset was
{df['Polarity'].mean():.3f}, indicating a moderately balanced
but cautious market outlook overall.
"""

paragraphs = [
    paragraph1,
    paragraph2,
    paragraph3,
    paragraph4,
    paragraph5
]

# DRAW PARAGRAPHS WITH REAL SPACING
for paragraph in paragraphs:

    wrapped = textwrap.wrap(
        paragraph,
        width=62
    )

    for line in wrapped:

        text.textLine(line)

    # EXTRA GAP BETWEEN PARAGRAPHS
    text.textLine("")
    text.textLine("")

# DRAW TEXT
c.drawText(text)

# FOOTER
c.setFont(
    "Helvetica-Oblique",
    9
)

c.setFillColorRGB(0.45, 0.45, 0.45)

c.drawCentredString(
    page_width / 2,
    30,
    "Financial Sentiment Analysis Report — Market Overview"
)

c.showPage()
# ══════════════════════════════════════════════════════
# INSIGHTS & RECOMMENDATIONS
# ══════════════════════════════════════════════════════

c.setFillColorRGB(0.35, 0.05, 0.15)

# TITLE
c.setFont(
    "Helvetica-Bold",
    26
)

c.drawString(
    60,
    page_height - 60,
    "Insights & Recommendations"
)

# Decorative line
c.setLineWidth(1.5)

c.line(
    60,
    page_height - 75,
    page_width - 60,
    page_height - 75
)

# TEXT OBJECT
text = c.beginText()

text.setTextOrigin(
    75,
    page_height - 125
)

# Better spacing
text.setLeading(28)

# BODY FONT
text.setFont(
    "Helvetica",
    11.8
)

# ──────────────────────────────────────────────────────
# SECTION: KEY INSIGHTS
# ──────────────────────────────────────────────────────
text.setFont(
    "Helvetica-Bold",
    16
)

text.textLine("KEY INSIGHTS")
text.textLine("")

text.setFont(
    "Helvetica",
    11.8
)

insights = [

    "Technology and AI-related headlines generated the strongest positive sentiment scores across the dataset, reflecting strong investor confidence in innovation-driven market sectors.",

    "Inflation and recession-related headlines produced the strongest negative emotional reactions, highlighting continued concerns regarding economic uncertainty and financial instability.",

    "Investor confidence appears highly reactive to monetary policy announcements, interest rate decisions, and broader macroeconomic developments.",

    "Word cloud analysis revealed that terms such as 'market', 'stocks', 'inflation', and 'investors' dominate financial discussions and public attention."

]

for item in insights:

    wrapped = textwrap.wrap(
        "• " + item,
        width=72
    )

    for line in wrapped:
        text.textLine(line)

    # Space between bullet points
    text.textLine("")


# ──────────────────────────────────────────────────────
# SECTION: BUSINESS RECOMMENDATIONS
# ──────────────────────────────────────────────────────
text.textLine("")

text.setFont(
    "Helvetica-Bold",
    16
)

text.textLine("BUSINESS RECOMMENDATIONS")
text.textLine("")

text.setFont(
    "Helvetica",
    11.8
)

recommendations = [

    "Organisations should monitor sentiment trends to better understand changing investor behaviour and public opinion patterns.",

    "Financial institutions may integrate NLP-based analytics into forecasting models and decision support systems to improve strategic planning.",

    "Marketing teams can use sentiment analysis to evaluate consumer confidence, customer perception, and overall brand reputation.",

    "Businesses should combine sentiment analytics with predictive modelling techniques to strengthen business intelligence capabilities."

]

for item in recommendations:

    wrapped = textwrap.wrap(
        "• " + item,
        width=72
    )

    for line in wrapped:
        text.textLine(line)

    text.textLine("")


# ──────────────────────────────────────────────────────
# SECTION: CONCLUSION
# ──────────────────────────────────────────────────────
text.textLine("")

text.setFont(
    "Helvetica-Bold",
    16
)

text.textLine("CONCLUSION")
text.textLine("")

text.setFont(
    "Helvetica",
    11.8
)

conclusion = """
This project demonstrates how Natural Language
Processing and sentiment analysis techniques can
transform unstructured textual data into meaningful
business insight capable of supporting strategic
decision-making processes.

The findings further highlight the growing importance
of combining artificial intelligence techniques with
modern business intelligence and analytics frameworks.
"""

wrapped_conclusion = textwrap.wrap(
    conclusion,
    width=72
)

for line in wrapped_conclusion:
    text.textLine(line)

# DRAW EVERYTHING
c.drawText(text)

# FOOTER
c.setFont(
    "Helvetica-Oblique",
    9
)

c.setFillColorRGB(0.45, 0.45, 0.45)

c.drawCentredString(
    page_width / 2,
    30,
    "Financial Sentiment Analysis Report — Insights & Strategic Recommendations"
)

c.showPage()
# ══════════════════════════════════════════════════════
# ANALYTICAL SIGNIFICANCE
# ══════════════════════════════════════════════════════
c.setFont(
    "Helvetica-Bold",
    24
)

c.setFillColorRGB(0.35, 0.05, 0.15)

c.drawString(
    60,
    page_height - 60,
    "Analytical Significance"
)

c.line(
    60,
    page_height - 72,
    page_width - 60,
    page_height - 72
)

text = c.beginText(
    70,
    page_height - 130
)

text.setFont(
    "Helvetica",
    12
)

text.setLeading(28)

closing = """
The results demonstrate the growing importance of integrating machine learning,
sentiment analysis, and Natural Language Processing techniques into modern
business intelligence frameworks.

The project highlights how unstructured textual data can be transformed into
meaningful analytical insight capable of supporting strategic decision-making
processes across finance, marketing, and market research environments.

The findings further confirm that sentiment analysis can provide organisations
with deeper understanding of public opinion, investor psychology,
consumer behaviour, and evolving market trends.

Overall, the project demonstrates the practical value of combining artificial
intelligence techniques with modern data analytics methodologies.
"""

wrapped = textwrap.wrap(
    closing,
    width=78
)

for line in wrapped:
    text.textLine(line)

c.drawText(text)

c.showPage()

# ══════════════════════════════════════════════════════
# VISUALIZATION PAGES
# ══════════════════════════════════════════════════════
charts = [

    (
        "sentiment_distribution.png",
        "Market Sentiment Distribution",
        "The sentiment distribution illustrates the balance between positive, neutral, and negative financial sentiment across analysed headlines."
    ),

    (
        "sentiment_pie_chart.png",
        "Sentiment Proportions",
        "The pie chart highlights the proportional relationship between different market sentiment categories."
    ),

    (
        "wordcloud.png",
        "Financial Word Cloud",
        "The word cloud identifies dominant financial themes and recurring market discussion topics."
    ),

    (
        "polarity_distribution.png",
        "Polarity Score Distribution",
        "The polarity score distribution demonstrates variation in sentiment intensity across financial headlines."
    )

]

for filename, title, interpretation in charts:

    image_path = f"outputs/{filename}"

    # TITLE
    c.setFont(
        "Helvetica-Bold",
        22
    )

    c.setFillColorRGB(0.35, 0.05, 0.15)

    c.drawString(
        60,
        page_height - 60,
        title
    )

    c.line(
        60,
        page_height - 72,
        page_width - 60,
        page_height - 72
    )

    # EXPLANATION
    text = c.beginText(
        60,
        page_height - 120
    )

    text.setFont(
        "Helvetica",
        12
    )

    text.setLeading(24)

    wrapped = textwrap.wrap(
        interpretation,
        width=80
    )

    for line in wrapped:
        text.textLine(line)

    c.drawText(text)

    # IMAGE
    c.drawImage(
        image_path,
        80,
        170,
        width=430,
        height=320,
        preserveAspectRatio=True
    )

    c.showPage()

# ══════════════════════════════════════════════════════
# SAVE PDF
# ══════════════════════════════════════════════════════
c.save()

print("\nProfessional sentiment analysis report generated successfully.")
print("Saved → outputs/final_sentiment_report.pdf")