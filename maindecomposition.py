'''
Authors: 
M Ely Piceno: almost all of this code taken from her file OutpDotFile.py

Jose Luis Balcazar, ORCID 0000-0003-4248-4528 (marked JLB):
- import-handling changes at the head of the file
- changed "%24" to "%23" midway through function Write
- renamed "main" to "decompose"
- extra argument "items" for TotalAttributesValues in ExtractLeaves
     and other places, taking '-' and '=' out of the names 
- tried to correct issue with "titanicproof" filename 
     but had to resort to a hack
- rest of changes near the end of the file
- transformation functions into matrix graph required by rest of s/w
    (including extra singleton list for each element)
- graph input before the main call 
- local TotalAttributesValues for other needs
'''

# JLB: hid these imports, recover CCT below
# ~ from FindUnionDecompositionV8 import *
# ~ #from FindUnionDecompositionV8 import ConstructColorTrees
# ~ from FromFileToGraph import *
# ~ from subprocess import check_call #fr1om .dot to .png

# JLB: trying to keep imports at the minimum
from FindUnionDecompositionV009 import ConstructColorTrees, MyClan, AddNode, ExtractLeaves, Find, EdgeOf

# JLB: Original Ely's code from here to the end, except as reported above

###################################################################

ClanList = []
SingletonNodes = []

DictColors=['white','black','blue','blueviolet','brown','burlywood','cadetblue','chartreuse','coral','crimson','cyan','darkorange','deeppink','deepskyblue','forestgreen','gold','greenyellow','hotpink','orangered','pink','red','seagreen','yellow']

#for i in MyGraph:
#	print (i)

#ActualClan = MyClan('complete')
#TotalAttributesValues =[]
'''
Descompose clan with it information, clans and singletons.
We may obtain the quantity of clans and the quantity of singletons nodes, also which they are.  
'''
def DecomposeClan(Clan):
	Clans =[]
	Singletons =[]
	for i in Clan.nodes:
		if '[' not in str(i):
			Singletons.append(i)
		else:
			Clans.append(Clan.getclanwithnodes(i))
	return Singletons,Clans

'''
Given a list, where there could be other lists or not, we obtain a string conformed by the elements involved.
JLB: remove '=' and '-' from cluster names previously on TotalAttributesValues
'''
def GiveName(SomeList):
	name=''
	# ~ print(SomeList, type(SomeList))
	if type(SomeList)== list:
		for i in SomeList:
			if type(i)==list:
				name = name + GiveName(i)
			else:
				name= name+TotalAttributesValues[int(i)]
	else:
		name= TotalAttributesValues[int(SomeList)]		
	# ~ name = name.replace(".","p")
	name = name.replace(".","_").replace("=","_").replace("-","_")	
	return name
	
'''
Generate the cluster of the clan Clan
'''
def MakeCluster(Clan,OutputFile):
	name = GiveName(Clan.nodes)
	OutputFile.write('subgraph cluster_'+name+'{\n node [shape = point ];\n')
	DCC = DecomposeClan(Clan)
		
	if len(Clan.nodes) == 2:
		OutputFile.write('rank= same;\n')
		
	actnode = 0
	
	if len(Clan.nodes)< 12:
		SingletonNodes.extend(DCC[0])
		while actnode < len(Clan.nodes)-1:
			restnode = actnode + 1
			flist = Clan.nodes[actnode]				
			while restnode < len(Clan.nodes):
				tlist = Clan.nodes[restnode]
				f = GiveName(flist)
				t = GiveName(tlist)
				
				if type(flist)==list:
					flist1 = flist[0]
				else:
					flist1 = flist
				if type(tlist)==list:
					tlist1 = tlist[0]
				else:
					tlist1 = tlist	
				ColorEdge = str(Find(EdgeOf(str(flist1)+','+str(tlist1))))
				Indx= ColorEdge.split(',')
				if int(MyGraph[int(Indx[0])][int(Indx[1])][0])== 0:
					OutputFile.write('n_'+f+' -> n_'+t+' [color=black, style=dashed, arrowhead = none];\n')
				elif Indx[0]!= Indx[1]:
					#colr = 1  # int(MyGraph[int(Indx[0])][int(Indx[1])])%23
					if type(MyGraph[int(Indx[0])][int(Indx[1])])==list:
						colr= int(MyGraph[int(Indx[0])][int(Indx[1])][0])%24
					else:
						colr = int(MyGraph[int(Indx[0])][int(Indx[1])])%24
					# ~ print('*from to: ', int(Indx[0]), int(Indx[1]),MyGraph[int(Indx[0])][int(Indx[1])])	
				
					# ~ print('clase: ', MyGraph[int(Indx[0])][int(Indx[1])])
					# ~ print('color: '+ DictColors[colr])
					OutputFile.write('n_'+f+' -> n_'+t+' [color= '+DictColors[colr]+', arrowhead = none];\n')
				else:
					OutputFile.write('n_'+f+' -> n_'+t+' [color=black, arrowhead = none];\n')
				restnode += 1
			actnode += 1
	
	elif len(DCC[0])>5 and len(DCC[1])<5:
		#if len(DCC[1])==1:
		OutputFile.write('rank=same;')
		if Clan.clantype== 'complete':
			ColorEdge = str(Find(EdgeOf(DCC[0][0]+','+DCC[1][0])))
			Indx= ColorEdge.split(',')
			if MyGraph[int(Indx[0])][int(Indx[1])][0] == '0':
				OutputFile.write('label = '+Clan.clantype+' "----";\n')
			else:
				OutputFile.write('label = '+Clan.clantype+' "____";\n')
		else:
			OutputFile.write('label = '+Clan.clantype+';\n')
		while actnode < len(Clan.nodes)-1:
			restnode = actnode + 1
			flist = Clan.nodes[actnode]				
			while restnode < len(Clan.nodes) and '[' in str(flist):
				tlist = Clan.nodes[restnode]
				if '[' in str(tlist):
					f = GiveName(flist)
					t = GiveName(tlist)
					OutputFile.write('n_'+f+' -> n_'+t+' [color=white,arrowhead = none];\n')
				restnode += 1
			actnode += 1
		f= GiveName(DCC[0])	
		InternalOthers.append(f)
		for i in Clan.nodes:				
			if '[' in str(i):
				t = GiveName(i)				
				OutputFile.write('n_'+f+' -> n_'+t+' [color=white,arrowhead = none];\n')
				
	else:# 
		if Clan.clantype== 'complete':
			ColorEdge = str(Find(EdgeOf(DCC[0][0]+','+DCC[1][0])))
			Indx= ColorEdge.split(',')
			if MyGraph[int(Indx[0])][int(Indx[1])][0] != '0':
				OutputFile.write('label = '+Clan.clantype+' "____";\n')
			else:
				OutputFile.write('label = '+Clan.clantype+' "----";\n')
		else:
			OutputFile.write('label = '+Clan.clantype+';\n')
	OutputFile.write('}\n')	
	
			
def FindClans(Clan):
	clans = DecomposeClan(Clan)[1]
	ClanList.extend(clans)
	for clan in clans:
		FindClans(clan)

def Write(ActualClan, inputfilename, MyGraphA):
	#print('TOTAL ATRIBUTE VALUES', TotalAttributesValues)
	#inputfilename = input('Name of the dot file: ')
	#inputfilename = gfilename
	OutputFile = open(inputfilename+'.dot', 'w')
	OutputFile.write('strict digraph '+inputfilename+'_dot {\n compound=true;\n fontname=Verdana;\n fontsize=12;\n newrank=true;\n node [shape=ellipse]; \n')



	#MakeCluster(ActualClan)::::ojo hacer una lista de InternalOthers

	name =GiveName(ActualClan.nodes)
	OutputFile.write('subgraph cluster_'+name+'{\n node [shape = point ];\n')
	if len(ActualClan.nodes) == 2:
		OutputFile.write('rank= same;\n')

	DCC =DecomposeClan(ActualClan)
	OthersMax=''
	InternalOthers=[]
	
	actnode = 0
	if len(ActualClan.nodes)< 13:
		SingletonNodes.extend(DCC[0])
		while actnode < len(ActualClan.nodes)-1:
			restnode = actnode + 1
			flist = ActualClan.nodes[actnode]				
			while restnode < len(ActualClan.nodes):
				tlist = ActualClan.nodes[restnode]
				f = GiveName(flist)
				t = GiveName(tlist)			
				if type(flist)==list:
					flist1 = flist[0]
				else:
					flist1 = flist
				if type(tlist)==list:
					tlist1 = tlist[0]
				else:
					tlist1 = tlist	
				ColorEdge = str(Find(EdgeOf(str(flist1)+','+str(tlist1))))
				Indx= ColorEdge.split(',')
				if int(MyGraphA[int(Indx[0])][int(Indx[1])][0]) == 0:
					OutputFile.write('n_'+f+' -> n_'+t+' [color=black, style=dashed, arrowhead = none];\n')
				elif Indx[0]!= Indx[1]:
					"JLB: modulus was 24, I think it is incorrect, changed to 23"
					if type(MyGraphA[int(Indx[0])][int(Indx[1])])==list:
						colr= int(MyGraphA[int(Indx[0])][int(Indx[1])][0])%23
					else:	
						colr = int(MyGraphA[int(Indx[0])][int(Indx[1])])%23
							
					#OutputFile.write('******from to: ', int(Indx[0]),int(Indx[1]))	
					#OutputFile.write('*******clase: ', MyGraph[int(Indx[0])][int(Indx[1])])
					#OutputFile.write('*******color '+DictColors[colr])
					OutputFile.write('n_'+f+' -> n_'+t+' [color= '+DictColors[colr]+' arrowhead = none];\n')
				else:
					OutputFile.write('n_'+f+' -> n_'+t+' [color=black, arrowhead = none];\n')
				restnode += 1
			actnode += 1

	elif len(DCC[0])>5 and len(DCC[1])==1:
		OutputFile.write('rank = same; \n')
		OutputFile.write('label = '+ActualClan.clantype+';\n')
		if ActualClan.clantype== 'complete':
			uniqueclannodes =DCC[1][0].nodes
			ColorEdge = str(Find(EdgeOf(DCC[0][0]+','+uniqueclannodes[0])))
			Indx= ColorEdge.split(',')
			f = GiveName(DCC[0])
			t = GiveName(uniqueclannodes)
			if MyGraphA[int(Indx[0])][int(Indx[1])][0] == '0':
				OutputFile.write('n_'+f+' -> n_'+t+' [color=black, style=dashed, arrowhead = none];\n')
				OthersMax = f
			else:				
				OutputFile.write('n_'+f+' -> n_'+t+' [color=white, arrowhead = none];\n')
				OthersMax = f
		else:
			uniqueclannodes =DCC[1][0].nodes
			f = GiveName(DCC[0])
			t = GiveName(uniqueclannodes)
			OutputFile.write('n_'+f+' -> n_'+t+' [color=white, arrowhead = none];\n')
			OthersMax = f
		
	elif len(DCC[0])>5 and len(DCC[1])<5:
		if ActualClan.clantype== 'complete':
			ColorEdge = str(Find(EdgeOf(DCC[0][0]+','+DCC[1][0].nodes[0])))
			Indx= ColorEdge.split(',')
			if MyGraphA[int(Indx[0])][int(Indx[1])][0] == '0':
				OutputFile.write('label = '+ActualClan.clantype+' "----";\n')
			else:
				OutputFile.write('label = '+ActualClan.clantype+' "____";\n')
		else:
			OutputFile.write('label = '+ActualClan.clantype+';\n')
		while actnode < len(ActualClan.nodes)-1:
			restnode = actnode + 1
			flist = ActualClan.nodes[actnode]				
			while restnode < len(ActualClan.nodes) and '[' in str(flist):
				tlist = ActualClan.nodes[restnode]
				if '[' in str(tlist):
					f = GiveName(flist)
					t = GiveName(tlist)
					OutputFile.write('n_'+f+' -> n_'+t+' [color=white,arrowhead = none];\n')
				restnode += 1
			actnode += 1
		f= GiveName(DCC[0])			
		for i in ActualClan.nodes:				
			if '[' in str(i):
				t = GiveName(i)				
				OutputFile.write('n_'+f+' -> n_'+t+' [color=white,arrowhead = none];\n')
		OthersMax = f
			
	else:# len(DCC[1])<5:
		if ActualClan.clantype== 'complete':
			if type(DCC[0][0])== MyClan:
				i = str(DCC[0][0].nodes[0])
			else:
				i = DCC[0][0]			 
			if type(DCC[1][0])== MyClan:
				j = str(DCC[1][0].nodes[0])
			else:
				j =	DCC[1][0]
			ColorEdge = str(Find(EdgeOf(i+','+j)))
			#ColorEdge = str(Find(EdgeOf(DCC[0][0]+','+DCC[1][0])))
			Indx= ColorEdge.split(',')
			if MyGraphA[int(Indx[0])][int(Indx[1])][0] != '0':
				OutputFile.write('label = '+ ActualClan.clantype+' "____";\n')
			else:
				OutputFile.write('label = '+ ActualClan.clantype+' "----";\n')
		else:
			OutputFile.write('label = '+ ActualClan.clantype+';\n')
	OutputFile.write('}\n')	
	#end make cluster ActualClan	



	FindClans(ActualClan)

	for c in ClanList:
		# ~ print('clanes: ',str(c))
		MakeCluster(c,OutputFile)
	
	for i in SingletonNodes:
		if TotalAttributesValues[int(i)][0].isdigit():
			OutputFile.write('"'+TotalAttributesValues[int(i)]+'";\n')
		else:
			OutputFile.write(TotalAttributesValues[int(i)]+';\n')
	if len(ClanList)>=1:
		#if len(ClanList)==2:
		#	OutputFile.write('rank=same;\n')
		for i in ClanList:
			DC1=DecomposeClan(i)
			f = GiveName(i.nodes)
			if f != name:
				if len(DC1[0])<7:
					tlist = i.nodes[0]
					t = GiveName(tlist)
					OutputFile.write('n_'+f+' -> n_'+t+' [lhead = cluster_'+f+', color=black, arrowhead = none];\n')
				elif DC1[1]!=[]:
					tlist = DC1[1][0].nodes
					t = GiveName(tlist)
					OutputFile.write('n_'+f+' -> n_'+t+' [lhead = cluster_'+f+', color=black, arrowhead = none];\n')



	for i in SingletonNodes:
		fromAttributeValue = TotalAttributesValues[int(i)].replace('.','p')
		if TotalAttributesValues[int(i)][0].isdigit() or '.' in TotalAttributesValues[int(i)][0]:
			OutputFile.write('n_'+fromAttributeValue +' -> "'+TotalAttributesValues[int(i)]+'" [arrowhead = none];\n')
		else:
			OutputFile.write('n_'+fromAttributeValue +' -> '+TotalAttributesValues[int(i)]+' [arrowhead = none];\n') 
			#OutputFile.write('n_'+TotalAttributesValues[int(i)] +' -> '+TotalAttributesValues[int(i)]+' [arrowhead = none];\n') 

	if OthersMax!='':
		OutputFile.write('n_'+OthersMax+' -> Others [arrowhead = none];\n') 
	# ~ print('Internal others: ', InternalOthers,'*************************************************************') 	
	for i in InternalOthers:	
		OutputFile.write('n_'+i+' -> others [arrowhead = none];\n')	
		OutputFile.write('others [label = Others];\n')				
	OutputFile.write('}\n')

	OutputFile.close()
	#check_call(['dot','-Tpng',inputfilename+'.dot','-o',inputfilename+'.png'])#from .dot to .png

# JLB: function "main" renamed to "decompose"

def decompose(Graph, opt, file_name):
	EdgesNodes =[]
	CCT =[]
	if '9' not in opt:
		CCT=ConstructColorTrees(Graph,EdgesNodes)
		# ~ print('Edge nodes size: ', len(EdgesNodes))
		ActualClan = MyClan('complete')
		ActualClan.add_node(str(0))	
		for i in range(1,len(Graph)):
			AddNode(ActualClan,str(i),CCT,EdgesNodes)
		ExtractLeaves(ActualClan, TotalAttributesValues) # JLB: TotalAttributesValues was common to several files
		# ~ print ("compara")
		# ~ print (ActualClan.nodes)
		# ~ Write(ActualClan,'titanicproof',Graph) # JLB: trying to get a sensible name
		Write(ActualClan, file_name, Graph)
	else: #Construir los grafos paso a paso
		# ~ for i in Graph:
			# ~ print(i)
		OpF = open('Increasing1.txt', 'w')	
		for i in range(len(CoOccurrenceValues)):
			if CoOccurrenceValues[i] != 319  and CoOccurrenceValues[i] != 261 and CoOccurrenceValues[i] != 212: #and CoOccurrenceValues[i] != 425 and CoOccurrenceValues[i] != 367 and CoOccurrenceValues[i] != 344 and CoOccurrenceValues[i] != 203 and CoOccurrenceValues[i] != 196 and CoOccurrenceValues[i] != 180:
				AuxGraph =[]
				EdgesNodes =[]
				#print('threshold: ',CoOccurrenceValues[i])
				MatrixToMATPD(Graph, AuxGraph, CoOccurrenceValues[i],0)
				OpF.write('threshold: '+str(CoOccurrenceValues[i])+'\n') 
				namefile= file_name + '_' + str(CoOccurrenceValues[i])				
				for i in AuxGraph:
					print(i)	
				CCT=ConstructColorTrees(AuxGraph,EdgesNodes)
				# ~ print('Edge nodes size: ', len(EdgesNodes))
				ActualClan = MyClan('complete')
				ActualClan.add_node(str(0))	
				for i in range(1,len(AuxGraph)):
					AddNode(ActualClan,str(i),CCT,EdgesNodes)
				ExtractLeaves(ActualClan) 
				# ~ print ("compara")
				# ~ print (ActualClan.nodes)				
				OpF.write(str(ActualClan.nodes)+'\n')	
				Write(ActualClan,namefile,AuxGraph)
		OpF.close()

####################################################

# JLB: remainder of file is my hacks to make the algorithm 
#      useable from outside via function calls

# JLB: make available global variable TotalAttributesValues, 
#      necessary for Ely's code to work 
TotalAttributesValues = [ ]

# JLB: make items available as global variable TotalAttributesValues, 
#      necessary for Ely's code to work - also, there, 
#      replace '-' and '=' in names as disallowed by dot
def hack_items_in(items):
	global TotalAttributesValues
	TotalAttributesValues = [ item.replace('-', '_').replace('=', '_').replace(':','_') for item in items ] 

# JLB: make available global variable MyGraph, 
#      necessary for Ely's code to work 
MyGraph = [ ]

# JLB: set global variable MyGraph to actual graph 
def hack_graph_in(my_graph):
	global MyGraph
	MyGraph = my_graph

# JLB: several functions follow that receive a labeled
#      graph read in via github's labgaif/td2dot.py
#      which is to be reformatted as required by Ely's code

# JLB: from labeled graph to thresholded Gaifman graph 
def stdGgraph(graph, items, thr = 0):
	"list of lists of adjacency 0/1 booleans, optional lower threshold"
	MyGraph = []
	for r in items:
		"create each graph-matrix row"
		row = []
		for c in items:
			if graph[r][c] > thr:
				row.append([1]) # yes, a list of length 1, who knows why
			else:
				row.append([0])
		MyGraph.append(row)
	return MyGraph

# JLB: just recode the labeled graph as required by Ely's code
def labGgraph(graph, items):
	"list of lists of adjacency counts"
	MyGraph = []
	for r in items:
		"create each graph-matrix row"
		row = []
		for c in items:
			row.append([graph[r][c]]) # yes, a list of length 1, who knows why
		MyGraph.append(row)
	return MyGraph

if __name__ == "__main__":
	"JLB: integration tests, not all of them work well yet"

	# JLB: import from github's labgaif/td2dot.py to create a
	#      labeled Gaifman graph from a transactional data file 
	from td2dot import read_graph_in

	# choose an available .td file
	datasetfile = 'titanic_'
	
	# JLB: read labeled Gaifman graph
	graph, items = read_graph_in(datasetfile + '.td')
	
	# JLB: make items available as global variable TotalAttributesValues, 
	#      necessary for Ely's code to work - also, there, 
	#      replace '-' and '=' in names as disallowed by dot
	hack_items_in(items)
	
	# JLB: option 1 for original graph
	#      Recoded graph MUST be named MyGraph due to how Ely's code works
	# ~ MyGraph = labGgraph(graph, items)
	# ~ decompose(MyGraph, '1', datasetfile + '_orig_decomp')
	
	# JLB: option 2 for standard Gaifman graph: thresholded graph with default 0 threshold
	#      Recoded graph MUST be named MyGraph due to how Ely's code works
	MyGraph = stdGgraph(graph, items)
	decompose(MyGraph, '2', datasetfile + '_std_decomp')
	
	# JLB: option 3 for thresholded graph with explicit threshold
	#      Recoded graph MUST be named MyGraph due to how Ely's code works
	#      OK IF THRESHOLD IS 344 OR MORE, BUT WITH 343 OR LESS IT FAILS!	
	# ~ MyGraph = stdGgraph(graph, items, 344) 
	# ~ decompose(MyGraph, '3', datasetfile + '_decomp')
	
	
	
