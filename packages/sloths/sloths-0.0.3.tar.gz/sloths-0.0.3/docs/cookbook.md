# Cookbook

## Reading a file line by line

```{literalinclude} ./examples/read_file.py
:pyobject: compute_sequential
```

If the file is very large we can also do this using a process pool:

```{literalinclude} ./examples/read_file.py
:pyobject: compute_processpool
```

```{literalinclude} ./examples/read_file.py
:pyobject: part_sum
```

## Rate limiting

```{literalinclude} ./examples/rate_limit.py
```

## Adding progress bars

The {meth}`~sloths.Stream.inspect` function is useful to add progress monitoring
hooks within the pipeline, for example using `tqdm` and working off the file
reading example above:

```{literalinclude} ./examples/progress_bar.py
:pyobject: compute
```

Will result in an output like so:

```
Lines read: 79100904it [00:25, 2868235.68it/s]
Batches ready: 4943it [00:25, 179.08it/s]
Batches summed: 4939it [00:25, 176.77it/s]
```
