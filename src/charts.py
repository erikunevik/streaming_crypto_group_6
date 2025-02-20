import matplotlib.pyplot as plt

# Linecharts--------

def line_chart(x,y, **options):
    fig, ax = plt.subplots(1)
    
    ax.plot(x, y, linewidth = 1)

    ax.set(**options)
    plt.xticks(rotation=45)
    fig.tight_layout()
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))
    #ax.legend()
    return fig

# Piecharts---------------------



def pie_chart(labels, sizes, **options):
    fig, ax = plt.subplots(1)
    
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=options.get("colors"))
    
    fig.tight_layout()
    return fig
