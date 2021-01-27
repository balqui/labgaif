Transactional Datasets Format
=============================

File format appropriate for transactional datasets with proviso for comments and headers.

The format
----------

Very simple. Each transaction comes in one line and consists of items, 
separated by spaces. Items are strings of nonblank printable characters
and are taken at face value (no numeric translation). No empty transaction
is allowed. Items can be repeated in the transaction (but usually aren't).

Plan is to add options for headers (with some nonstandard options too) and
comments.

Context
-------

(To describe: why CSV is not employed.)

