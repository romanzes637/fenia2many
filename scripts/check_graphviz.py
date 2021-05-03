from graphviz import Digraph

if __name__ == '__main__':
    dot = Digraph(comment='The Round Table')

    dot.node('A', 'King Arthur')
    dot.node('B', 'Sir Bedevere the Wise')
    dot.node('L', 'Sir Lancelot the Brave')

    dot.edges(['AB', 'AL'])
    dot.edge('B', 'L', constraint='false')

    dot.render('round-table.gv', format='png', view=True)

