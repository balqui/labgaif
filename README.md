labgaif: Labeled Gaifman graphs
===============================

Transactional Datasets
----------------------

A transactional dataset on a set of items is formed by a 
set of labeled transactions, each transaction being a set
of items. The labels allow for the presence of several
copies of the same transactions if labels are different.
Most often, the dataset is a sequence of transactions and
the transaction label is given by the ordering. A simple
example appears in file e13.td in this repository.

Labeled Gaifman Graphs
----------------------

Given a transactional dataset, its classical Gaifman graph
has items as vertices, and an edge joins two vertices if and
only if the corresponding items appear together in some
transaction.

In the labeled Gaifman graph, each edge is labeled by its
multiplicity, that is, the number of transactions in which
the corresponding items appear together. Nonedges can be
seen as well as edges with multiplicity zero. Many variants
of Gaifman graphs can be defined on the basis of the labeled
variant.

This piece of software reads a transactional dataset in 
the ".td" format, described in file td.md in this repository,
and writes down the labeled Gaifman graph in DOT format,
so that Graphviz-related utilities can be applied on it
or on its variants.

Relational Data
---------------

The original concept of Gaifman graph was actually applied 
to relational datasets (finite relational structures as
models of first-order logic). A relational dataset is given 
by a set of relations over a relational scheme. The scheme 
indicates, for each relation name, a list of attribute names. 
Each relation proper consists of tuples: each tuple provides 
a value for each of the attributes given in the scheme for the
corresponding relation.

Handling several relations raises a number of issues;
here we consider only the case of a single relation.
The classical Gaifman graph (which was originally, 
in fact, this relational version) has a vertex for
each attribute value and an edge whenever two values
appear together in the same tuple. In the labeled 
variant, each edge is labeled again by its 
multiplicity: the number of tuples having both
values as indicated by the edge endpoints.

In practice, a simple question that is to be asked
is whether the same names for attribute values are
actually the same values or a different value is to
be considered for each attribute; for instance, 
number 8 does not have the same meaning for attribute
"age" than for attribute "number-of-children". 
If necessary, the attribute name is prepended often
to the attribute value in order to keep these
distinctions.

Then, each tuple is a set of pairs, attribute and
value; taking these pairs as items, tuples may be
seen as transactions and the relation may be recoded
as a transactional dataset. A simple example appears 
in file lenses.td in this repository.

Usage
-----

It is Python 3 code. Try 

$ ./td2dot dataset.td 

and, if this does not work, then 

$ python td2dot.py dataset.td 

(or python3) should work. If no dataset is supplied, 
a filename is asked. Flags -V and -h are honored in 
the standard way.

Coming
------

Options for:
* redefining the separator: #s',' for a comma, and likewise anything else (but it must be printable 7bit-ascii)
* plain comments, probably with double hash '##'
* specification of existence of header line and what to do with it:
** #hv: the first line is a header line: please prepend all attribute **v**alues with the attribute name
** #hr: the first line is a header line but attribute names are **r**edundant, they are already prepended to attribute values
** #hi: the first line is a header line but simply please **i**gnore it, whatever the reasons
** #hm: **m**issing: there is no header line, all lines are data transactions
