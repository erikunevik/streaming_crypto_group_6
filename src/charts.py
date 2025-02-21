import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Linecharts--------
def line_chart(x, y, hour_format=False, **options):
    fig, ax = plt.subplots(1)
    
    ax.plot(x, y, linewidth=2)
    ax.set(**options)
    plt.xticks(rotation=45)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_title(label= options["title"], fontsize=12, fontweight="bold")
    my_xfmt = mdates.DateFormatter('%y-%m-%d %H:%M')
    ax.xaxis.set_major_formatter(my_xfmt)
    ax.yaxis.set_major_formatter('{x:,.0f}')

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
        ax.set_title(options['title'], fontsize=12, fontweight="bold")
 
    
    fig.tight_layout()
    return fig
