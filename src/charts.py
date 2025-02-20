import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Linecharts--------
def line_chart(x, y, hour_format=False, **options):
    fig, ax = plt.subplots(1)
    
    ax.plot(x, y, linewidth=1)
    ax.set(**options)
    plt.xticks(rotation=45)
    fig.tight_layout()
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))

# -------- To be able to give minutes to 24 hour graph
    if hour_format:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        
    return fig

# Piecharts---------------------

def pie_chart(labels, sizes, **options):
    fig, ax = plt.subplots(1)
    colors = ['#155263', '#ff6f3c', '#ff9a3c', '#ffc93c']
    
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    
    if 'title' in options:
        ax.set_title(options['title'])
    
    fig.tight_layout()
    return fig
