import graphviz 
import matplotlib.pyplot as plt
import numpy as np
from src.Class_arbre import *
from src.Class_math import *
from src.Class_graph import *
    
class graph:
    def __init__(self,list_graph):
        self.list_graph = list_graph
        
    def plot_arbre(self):
        '''
        c'arbre à partir de la liste des arcs donnés.
        Cette méthode regroupe toutes les feuilles de l’arbre.

        Returns
        -------
        None.

        '''
        dot = graphviz.Digraph()    
        for arc in self.list_graph:
            dot.node(arc.getFather().getValue())
            dot.node(arc.getSon().getValue())
            dot.edge(arc.getFather().getValue(), arc.getSon().getValue(),arc.getWeight())
        
        dot.render('graph', view=True)
        
    def plot_matrice(self,matrix,data):
        '''
        Permet d’afficher la matrice de confusion.
        En prenant une matrice avec les données.
        
        Parameters
        ----------
        matrix : TYPE
            DESCRIPTION.
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        calc = Class_math(data) 
        labels = data[0]
        tick_labels = calc.getValeursPosibles(labels[len(labels)-1],data)
        
        confusion_matrix = matrix
        
        confusion_matrix = np.array(confusion_matrix)
        plt.figure(dpi=1200)
        plt.imshow(confusion_matrix, cmap='Blues')
        
        plt.colorbar()
        
        plt.xticks(range(len(tick_labels)), tick_labels, rotation=90)
        plt.yticks(range(len(tick_labels)), tick_labels)
        
        plt.xlabel('Predicted label')
        plt.ylabel('True label')
        plt.title('Confusion matrix')
        
        for i in range(len(confusion_matrix)):
            for j in range(len(confusion_matrix)):
                plt.text(j, i, str(confusion_matrix[i][j]), horizontalalignment='center', verticalalignment='center')
                
        plt.savefig('plot.png', bbox_inches='tight')
        plt.show()
            