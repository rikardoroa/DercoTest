#script by rikardoroa, just python it!
#library to generate various plots


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import logging

def explore_duplicates(x):
    data = x
    #vemos las ocurrencia de todas las filas que se repitan
    if  data[data.duplicated(keep=False)].shape[0]>0:
        cols = []
        for col in data.columns:
            cols.append(col)
        data = data[~data.duplicated(subset=cols,keep=False)].drop_duplicates()#verificamos todas las ocurrencias de las filas
        return data
    else:
        return data
    
    
def exploring_nulls_inf(x):
    data = x
    #verificamos si hay valores nulos y infinitos en el df
    Inf_values = {col : data[data[col].isin([np.inf, -np.inf])].shape[0] for col in data.columns}
    Null_values = {col : data[data[col].isna()].shape[0] for col in data.columns}
    #declaramos variables
    cols =['Inf Values','Null Values','Col Names']
    Null=[]
    #formamos los valores de cada uno de los diccionarios y formamos tuplas
    t = ([*Inf_values.values()],[*Null_values.values()],data.columns)
    #creamos la lista con los valores de las tuplas
    for index, item in enumerate(zip(t)):
        Null.append(t[index])
    #generamos el nuevo json
    dc = {cols[index]:Null[index] for index, item in enumerate(zip(cols,Null))}
    df = pd.DataFrame(data=dc)

    return df
   

        
def plot_decorator(function):
    
    def plotting(*args,**kwargs):
    #generamos el grafico
        x,y = function(*args,**kwargs)
        fig, ax = plt.subplots(figsize=kwargs['tam'])
        plot = ax.bar(x, y,color=kwargs['colors'])
        ax.set_xlabel(kwargs['xlabel'])
        ax.set_ylabel(kwargs['ylabel'])
        ax.set_title(kwargs['title'],fontweight='bold')
        ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y,  p: format(int(y), ',')))
        for container in ax.containers:
            ax.bar_label(container,labels=[f'{p.get_height():,}' for p in container])
        return plt.show()
    return plotting

  
@plot_decorator   
#def generating_barplot(title,xlabel,ylabel,cola,colb,data,tam,colors,*args,**kwargs):
def generating_barplot(data,cola,colb,**kwargs):
    #declaramos las listas que tendran los valores de x,y
    y =[]
    x =[]
    #definimos valores del eje y
    for item in data[cola]:
        y.append(item)
    #definimos los valores del eje x
    for item in  data[colb]:
        x.append(item)
        x = list(dict.fromkeys(x))
        x.sort()
    return x,y
    
def generating_stakedbarplot(title,xlabel,ylabel,df1,colx,df2,coly,labels,tam,legendx,legendy):
    
    #transformando los datos iniciales para los ejes x, y
        x_=[]
        y=[]
        label=[]
        
        #capturamos los datos de las barras y labels en las listas definidas
        for item in df1[colx]:
            x_.append(item)
            
        for item in df2[coly]:
            y.append(item)
            
        for item in df2[labels]:
            label.append(item)
            
        
        #generando el grafico
        x = np.arange(len(label))  
        width = 0.35  
        fig, ax = plt.subplots(figsize=(tam))
        bar1 = ax.bar(x - width/2, x_, width, label=legendx)
        bar2 = ax.bar(x + width/2, y, width, label=legendy)
        
        
        #agregando label a los ejes x,y
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        ax.set_title(title,fontweight='bold')
        ax.set_xticks(x, label)
        ax.legend()
        ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y,  p: format(int(y), ',')))
        for container in ax.containers:
            ax.bar_label(container,labels=[f'{p.get_height():,}' for p in container])
        
        return plt.show()
    
    
def generating_lineplot(df1=None,col1=None,col2=None,title=None,tam=None,xlabel=None,ylabel=None, hue=None,option=None):
    try:
       
        option_ = [1,2]
        for item in option_:
            if item == option and item == 1:

                #calculamos el promedio por año
                x=[]
                y=[]

                #generando los valores para los ejes x,y

                for item in df1[col1]:
                    x.append(item)

                for item in df1[col2]:
                    y.append(item)

                #generando el grafico
                fig, ax = plt.subplots(figsize=(tam))
                ax.plot(x, y,  '-gD')
                titulo = plt.suptitle(title, fontname='arial', fontsize=12,fontweight='bold')
                plt.setp(titulo,color='black')
                plt.xlabel(xlabel,fontsize=12)
                plt.ylabel(ylabel,fontsize=12)

                #formateamos con el separador de miles
                ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y,  p: format(int(y), ',')))
                #visualizamos los valores en las barras del plot
                for x,y in zip(x,y):
                    etiqueta = "{:,}".format(y)
                    ax.annotate(etiqueta, (x,y), textcoords="offset points",xytext=(0,10),ha="center")

                ax.grid(True)
                return plt.show()

            if item == option and item == 2:

                fig, ax = plt.subplots(figsize=(tam))
                ax = sns.lineplot(x=col1, y=col2, hue=hue, data=df1,  marker='o',)
                ax.set_xlabel(xlabel,fontsize='15')
                ax.set_ylabel(ylabel,fontsize='15')
                ax.set_title(title,fontweight='bold')
                ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y,  p: format(int(y), ',')))
                ax = plt.gca()

                #formateamos los label del plot con el separador de miles
                for x, y in zip(df1[col1], df1[col2]):
                    plt.text(x , y, s = '{:,}'.format(y),color = 'red')
                return plt.show()
    except TypeError:
            print('Escriba el parametro correcto')

        
def sns_barplot(x=None,y=None,hue=None,df=None,tam=None,xlabel=None,ylabel=None,title=None, option=None):
    
    option_ = [1,2]
    
    for item in option_:
        if item == option and item == 1:
    
            #generamos el grafico
            fig, ax = plt.subplots(figsize=(tam))
            ax = sns.barplot (x=x, y=y, hue=hue, data=df)
            ax.set_xlabel(xlabel,fontsize='15')
            ax.set_ylabel(ylabel,fontsize='15')
            ax.set_title(title,fontweight='bold')
            ax.set_xticklabels(ax.get_xmajorticklabels())
            ax.set_yticklabels(ax.get_yticks(), fontsize = '12')
            ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y,  p: format(int(y), ',')))
           

            #formateamos los label del plot con el separador de miles
            for container in ax.containers:
                ax.bar_label(container,labels=[f'{p.get_height():,}' for p in container])

            return  plt.show()
        
        if item == option and item == 2:
            
            years=[]
            for year in df[x]:
                years.append(year)
            years = list(dict.fromkeys(years))    

            #Generando el Grafico

            for i in range(len(years)):

                fig, ax = plt.subplots(figsize=(tam))
                ax = sns.barplot(x=x, y=y, hue=hue, data=df[df[x]==years[i]])
                ax.set_xlabel(xlabel,fontsize='15')
                ax.set_ylabel(ylabel,fontsize='15')
                ax.set_title(title,fontweight='bold')
                ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y,  p: format(int(y), ',')))
                ax.xaxis.label.set_size(20)
                ax.legend(fontsize = 8.5)
                for container in ax.containers:
                    ax.bar_label(container,labels=[f'{p.get_height():,}' for p in container], fontsize = 9)

            return plt.show()

    
    
def generating_stakedplot(df = None ,label_col=None,col_a=None ,col_b=None,
                                                  filteredcol=None,filteredvalue_a=None,filteredvalue_b=None,ylabel=None,xlabel=None,
                                                   title = None,tam = None, colors = None,option = None,tick_b=None,tick_a=None,hue=None):
        
        #genero las listas para guardar los datos de los ejes x,y y la opcion del grafico
        label_a=[]
        label_b= []
        x=[]
        y=[]
        option_=[1,2]
        
        
        #genero los dataframes con las columnas filtradas
        df1 = df.loc[df[filteredcol]==filteredvalue_a]
        df2 = df.loc[df[filteredcol]==filteredvalue_b]
        
            
        #Generando los valores para los graficos
        width = 0.35 
        axes_labels=[]
        
        
        #generando los graficos
        for item in option_:
            if item == option and item == 1:
                
                #definimos datos de las labels y los ejex x,y
                for item in df[label_col]:
                    label_a.append(item)
                    
                label = list(dict.fromkeys(label_a))
                
                for item in df1[col_a]:
                    x.append(item)

                for i, j in zip (df2[col_a],df2[col_b]):
                    y.append(i)
                    label_b.append(j)

                axes_labels.append(label)
                axes_labels.append(label_b)

                for i in range(len(axes_labels)):
                    fig, ax = plt.subplots(figsize=(tam))
                    colors = colors
                    ax.bar(axes_labels[i], x, width, label=tick_a, color=colors[0])
                    ax.bar(axes_labels[i], y, width, bottom=x, label=tick_b, color=colors[1])
                    ax.set_ylabel(ylabel)
                    ax.set_title(title,fontweight='bold')
                    ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y,  p: format(int(y), ',')))
                    for container in ax.containers:
                        ax.bar_label(container,labels=[f'{p.get_height():,}' for p in container])
                    fig.tight_layout()
                    ax.legend()
                return plt.show()

            if item == option and item == 2:
                
                for item in df1[col_a]:
                    x.append(item)

                for item in df1[col_a]:
                    y.append(item)

                axes_labels.append(df1)
                axes_labels.append(df2)
                #generamos los graficos
                for i in range(len(axes_labels)):
                    fig, ax = plt.subplots(figsize=(tam))
                    ax = sns.barplot(x = col_a, y = col_b ,hue=hue, data = axes_labels[i])
                    ax.set_xlabel(xlabel,fontsize='15')
                    ax.set_ylabel(ylabel,fontsize='15')
                    ax.set_title(title,fontweight='bold')
                    ax.set_xticklabels(ax.get_xmajorticklabels())
                    ax.set_yticklabels(ax.get_yticks(), fontsize = '12')
                    ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y,  p: format(int(y), ',')))
                    ax.tick_params(length=1, axis='x')
                    plt.setp(ax.get_legend().get_texts(), fontsize='12') 
                    plt.setp(ax.get_legend().get_title(), fontsize='12')

                    #formateamos los label del plot con el separador de miles
                    for container in ax.containers:
                        ax.bar_label(container)

                return plt.show()


        
        
    
