import matplotlib.pyplot as plt

# Linecharts--------

def line_chart(x,y, **options):
    fig, ax = plt.subplots(1)

    ax.plot(x, y, linewidth = 4)

    ax.set(**options)

    fig.tight_layout()
    return fig

# Piecharts---------------------

def pie_chart(labels, sizes, **options):
    fig, ax = plt.subplots(1)
    
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=options.get("colors"))
    
    fig.tight_layout()
    return fig
