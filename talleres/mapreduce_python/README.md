# MapReduce in Python
Simple MapReduce example in Python, taken from this [tutorial](https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/)

## Execute

Small sample text
```shell script
echo "foo foo quux labs foo bar quux" | python mapper.py | sort -k 1 | python reducer.py | sort -k 2nr
```

Top 10 words in Ulysses by James Joyce
```shell script
cat /path/to/book.txt | python mapper.py | sort -k 1 | python reducer.py | sort -k 2nr | head -n 10
```