This is the submission for the second assignment of CS315A at IIT Kanpur in 2014-15/II semester by Dhruv Singal (12243).

The program essentially generates a B+ tree storing data obtained from the assgn2_bplus_data.txt file, which consists of 10^6 data points. Multiple instances of same key are allowed. 

This implementation is novel in the manner that it stores all the nodes in form of file, with each node having maximum number of children specified in the bplustree.config file.

This program supports 3 query operations:
-insert
-point query
-range query

To run, simply call `make all`. To clean the data files generated, call `make clean`.