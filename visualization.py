# ══════════════════════════════════════════════════════
# TASK 3 — STOCK MARKET VISUALIZATION PROJECT
# COMPLETE PROFESSIONAL VERSION
# ══════════════════════════════════════════════════════

# ──────────────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import textwrap

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ──────────────────────────────────────────────────────
# CREATE OUTPUT FOLDER
# ──────────────────────────────────────────────────────
os.makedirs("outputs", exist_ok=True)

# ──────────────────────────────────────────────────────
# STYLE
# ──────────────────────────────────────────────────────
sns.set_theme(
    style="whitegrid",
    font_scale=1
)

# ──────────────────────────────────────────────────────
# COLORS
# ──────────────────────────────────────────────────────
COLOR_LIGHT = "#FFC8DD"
COLOR_MID = "#FFAFCC"
COLOR_BRIGHT = "#FF4D6D"
COLOR_DARK = "#800F2F"
COLOR_DEEP = "#590D22"

# ══════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════
df = pd.read_excel(
    "most_active_stocks_dataset.xlsx"
)

# ══════════════════════════════════════════════════════
# DATA PREPARATION
# ══════════════════════════════════════════════════════
df["Status"] = np.where(
    df["Change"] > 0,
    "Gainer",
    "Loser"
)

mean_price = df["Price"].mean()

status_counts = df["Status"].value_counts()

top_stocks = df.nlargest(
    10,
    "% Change"
)

corr = df[
    ["Price", "Change", "% Change"]
].corr()

# ══════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════
def style_ax(ax, title):

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
        color=COLOR_DEEP,
        pad=15
    )

    ax.tick_params(
        colors=COLOR_DARK
    )

def save_chart(fig, filename):

    fig.savefig(
        f"outputs/{filename}",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    plt.close(fig)

# ══════════════════════════════════════════════════════
# CHART 1 — MARKET BREADTH
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 6))

ax.pie(
    status_counts.values,
    labels=status_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=[
        COLOR_BRIGHT,
        COLOR_LIGHT
    ],
    wedgeprops={
        "edgecolor": "white",
        "linewidth": 2
    }
)

style_ax(
    ax,
    "Market Breadth: Gainers vs Losers"
)

save_chart(
    fig,
    "01_market_breadth.png"
)

# ══════════════════════════════════════════════════════
# CHART 2 — PRICE DISTRIBUTION
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 5))

sns.histplot(
    df["Price"],
    bins=20,
    kde=True,
    color=COLOR_BRIGHT,
    edgecolor="white",
    linewidth=1,
    ax=ax
)

ax.axvline(
    mean_price,
    color=COLOR_DEEP,
    linestyle="--",
    linewidth=2,
    label=f"Mean = {mean_price:.2f}"
)

ax.legend()

style_ax(
    ax,
    "Stock Price Distribution"
)

save_chart(
    fig,
    "02_price_distribution.png"
)

# ══════════════════════════════════════════════════════
# CHART 3 — VIOLIN PLOT
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 5))

sns.violinplot(
    data=df,
    x="Status",
    y="Price",
    hue="Status",
    legend=False,
    palette=[
        COLOR_BRIGHT,
        COLOR_LIGHT
    ],
    linewidth=1.5,
    ax=ax
)

style_ax(
    ax,
    "Price Density by Market Direction"
)

save_chart(
    fig,
    "03_violin_plot.png"
)

# ══════════════════════════════════════════════════════
# CHART 4 — TOP PERFORMERS
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 6))

sns.barplot(
    data=top_stocks,
    y="Symbol",
    x="% Change",
    hue="Symbol",
    legend=False,
    palette="RdPu",
    ax=ax
)

style_ax(
    ax,
    "Top 10 Performing Stocks"
)

save_chart(
    fig,
    "04_top_performers.png"
)

# ══════════════════════════════════════════════════════
# CHART 5 — CORRELATION HEATMAP
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 6))

sns.heatmap(
    corr,
    annot=True,
    cmap="RdPu",
    linewidths=1,
    linecolor="white",
    square=True,
    annot_kws={
        "fontsize": 11,
        "fontweight": "bold"
    },
    ax=ax
)

style_ax(
    ax,
    "Correlation Heatmap"
)

save_chart(
    fig,
    "05_heatmap.png"
)

# ══════════════════════════════════════════════════════
# CHART 6 — SCATTERPLOT
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="Price",
    y="% Change",
    hue="Status",
    palette=[
        COLOR_BRIGHT,
        COLOR_LIGHT
    ],
    s=90,
    edgecolor="white",
    alpha=0.85,
    ax=ax
)

style_ax(
    ax,
    "Price vs Percentage Change"
)

save_chart(
    fig,
    "06_scatter_plot.png"
)

# ══════════════════════════════════════════════════════
# CHART 7 — BOXPLOT
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="Status",
    y="% Change",
    hue="Status",
    legend=False,
    palette=[
        COLOR_BRIGHT,
        COLOR_LIGHT
    ],
    ax=ax
)

style_ax(
    ax,
    "Percentage Change Spread"
)

save_chart(
    fig,
    "07_boxplot.png"
)

# ══════════════════════════════════════════════════════
# OPTIONAL CLEAN DASHBOARD
# ══════════════════════════════════════════════════════
fig = plt.figure(
    figsize=(16, 10),
    facecolor="white"
)

gs = fig.add_gridspec(
    2,
    2,
    hspace=0.35,
    wspace=0.25
)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

# Pie
ax1.pie(
    status_counts.values,
    labels=status_counts.index,
    autopct="%1.1f%%",
    colors=[
        COLOR_BRIGHT,
        COLOR_LIGHT
    ],
    startangle=90,
    wedgeprops={
        "edgecolor": "white"
    }
)

ax1.set_title(
    "Market Breadth",
    fontsize=13,
    fontweight="bold"
)

# Histogram
sns.histplot(
    df["Price"],
    bins=20,
    kde=True,
    color=COLOR_BRIGHT,
    edgecolor="white",
    ax=ax2
)

ax2.axvline(
    mean_price,
    color=COLOR_DEEP,
    linestyle="--",
    linewidth=2
)

ax2.set_title(
    "Price Distribution",
    fontsize=13,
    fontweight="bold"
)

# Heatmap
sns.heatmap(
    corr,
    annot=True,
    cmap="RdPu",
    linewidths=1,
    linecolor="white",
    square=True,
    cbar=False,
    ax=ax3
)

ax3.set_title(
    "Correlation Heatmap",
    fontsize=13,
    fontweight="bold"
)

# Scatter
sns.scatterplot(
    data=df,
    x="Price",
    y="% Change",
    hue="Status",
    palette=[
        COLOR_BRIGHT,
        COLOR_LIGHT
    ],
    s=80,
    edgecolor="white",
    ax=ax4
)

ax4.set_title(
    "Price vs Percentage Change",
    fontsize=13,
    fontweight="bold"
)

fig.suptitle(
    "Stock Market Dashboard",
    fontsize=22,
    fontweight="bold",
    color=COLOR_DEEP,
    y=0.97
)

fig.subplots_adjust(
    top=0.88,
    left=0.06,
    right=0.96,
    bottom=0.08
)

save_chart(
    fig,
    "08_dashboard.png"
)

# ══════════════════════════════════════════════════════
# PDF REPORT
# ══════════════════════════════════════════════════════
pdf_path = "outputs/market_analysis_report.pdf"

c = canvas.Canvas(
    pdf_path,
    pagesize=A4
)

page_width, page_height = A4

## ══════════════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════════════
c.setFillColorRGB(0.35, 0.05, 0.15)

# Main Title
c.setFont(
    "Helvetica-Bold",
    30
)

c.drawCentredString(
    page_width / 2,
    page_height - 110,
    "Stock Market Analysis Report"
)

# Subtitle
c.setFont(
    "Helvetica",
    16
)

c.drawCentredString(
    page_width / 2,
    page_height - 145,
    "Exploratory Data Analysis & Visualization"
)

# Decorative line
c.setLineWidth(1.5)

c.line(
    90,
    page_height - 165,
    page_width - 90,
    page_height - 165
)

# Prepared By
c.setFillColorRGB(0, 0, 0)

c.setFont(
    "Helvetica-Bold",
    18
)

c.drawCentredString(
    page_width / 2,
    page_height - 250,
    "Prepared By"
)

c.setFont(
    "Helvetica",
    16
)

c.drawCentredString(
    page_width / 2,
    page_height - 285,
    "Ameni Jabeur"
)

# Project Description
description = [
    "This report analyzes the 100 most active stocks",
    "using statistical visualization and exploratory analysis.",
    "",
    "The objective is to identify market behavior,",
    "price distribution trends, volatility patterns,",
    "and relationships between stock variables."
]

y = page_height - 390

c.setFont(
    "Helvetica",
    13
)

for line in description:

    c.drawCentredString(
        page_width / 2,
        y,
        line
    )

    y -= 28

# Footer
c.setFont(
    "Helvetica-Oblique",
    10
)

c.drawCentredString(
    page_width / 2,
    60,
    "Generated using Python, Pandas, Matplotlib, Seaborn, and ReportLab"
)

c.showPage()

# ══════════════════════════════════════════════════════
# SUMMARY PAGE
# ══════════════════════════════════════════════════════
c.setFillColorRGB(0.35, 0.05, 0.15)

c.setFont(
    "Helvetica-Bold",
    22
)

c.drawString(
    70,
    page_height - 70,
    "Executive Summary"
)

c.line(
    70,
    page_height - 82,
    page_width - 70,
    page_height - 82
)

summary_text = """
The dataset reveals a market dominated by lower-priced securities,
while a small number of expensive stocks significantly influence
the overall average stock price.

Correlation analysis shows weak relationships between stock price
and percentage movement, suggesting that both low-priced and
high-priced securities experience volatility independently.

The visualizations also demonstrate an active market session
containing both gainers and losers with moderate dispersion
across percentage changes.
"""

wrapped_summary = textwrap.wrap(
    summary_text,
    width=70
)

text = c.beginText(
    70,
    page_height - 130
)

text.setFont(
    "Helvetica",
    12
)

text.setLeading(24)

for line in wrapped_summary:
    text.textLine(line)

c.drawText(text)

# Metrics
c.setFont(
    "Helvetica-Bold",
    18
)

c.drawString(
    70,
    page_height - 370,
    "Key Metrics"
)

metrics = [
    f"Total Stocks Analysed: {len(df)}",
    f"Average Stock Price: ${df['Price'].mean():.2f}",
    f"Median Stock Price: ${df['Price'].median():.2f}",
    f"Highest Stock Price: ${df['Price'].max():.2f}",
    f"Average Percentage Change: {df['% Change'].mean():.2f}%",
    f"Number of Gainers: {len(df[df['Change'] > 0])}",
    f"Number of Losers: {len(df[df['Change'] < 0])}",
]

y = page_height - 410

c.setFont(
    "Helvetica",
    12
)

for metric in metrics:

    c.drawString(
        90,
        y,
        f"• {metric}"
    )

    y -= 28

c.showPage()

# ══════════════════════════════════════════════════════
# VISUALIZATION PAGES
# ══════════════════════════════════════════════════════
charts = [

    (
        "01_market_breadth.png",
        "Market Breadth Analysis",
        "The market session contained both gainers and losers, with gainers slightly dominating total activity."
    ),

    (
        "02_price_distribution.png",
        "Stock Price Distribution",
        "The distribution is highly right-skewed, meaning a small number of expensive stocks strongly influence the market average."
    ),

    (
        "03_violin_plot.png",
        "Price Density Comparison",
        "Price distributions overlap significantly between gainers and losers, indicating volatility across all price levels."
    ),

    (
        "04_top_performers.png",
        "Top Performing Stocks",
        "Several stocks achieved exceptional percentage gains relative to the broader market."
    ),

    (
        "05_heatmap.png",
        "Correlation Heatmap",
        "Correlation analysis reveals weak relationships between stock price and market movement."
    ),

    (
        "06_scatter_plot.png",
        "Price vs Percentage Change",
        "The scatterplot demonstrates no strong linear relationship between stock price and percentage movement."
    ),

    (
        "07_boxplot.png",
        "Percentage Change Spread",
        "The boxplot highlights market variability and the presence of several statistical outliers."
    )
]

for filename, title, interpretation in charts:

    image_path = f"outputs/{filename}"

    # Title
    c.setFillColorRGB(0.35, 0.05, 0.15)

    c.setFont(
        "Helvetica-Bold",
        22
    )

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

    # Interpretation
    wrapped = textwrap.wrap(
        interpretation,
        width=80
    )

    text = c.beginText(
        60,
        page_height - 110
    )

    text.setFont(
        "Helvetica",
        12
    )

    text.setLeading(22)

    for line in wrapped:
        text.textLine(line)

    c.drawText(text)

    # Image
    img = ImageReader(
        image_path
    )

    img_width, img_height = img.getSize()

    max_width = page_width - 120
    max_height = 420

    scale = min(
        max_width / img_width,
        max_height / img_height
    )

    draw_width = img_width * scale
    draw_height = img_height * scale

    x = (page_width - draw_width) / 2
    y = 120

    c.drawImage(
        image_path,
        x,
        y,
        width=draw_width,
        height=draw_height
    )

    # Footer
    c.setFont(
        "Helvetica-Oblique",
        9
    )

    c.drawCentredString(
        page_width / 2,
        40,
        "Generated using Python, Pandas, Matplotlib, Seaborn, and ReportLab"
    )

    c.showPage()

# ══════════════════════════════════════════════════════
# SAVE PDF
# ══════════════════════════════════════════════════════
c.save()

print("\nProfessional PDF report exported successfully.")
print("Saved → outputs/market_analysis_report.pdf")