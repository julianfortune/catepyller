# Read Me

## Sequences

### Create ???
- [-] count
- [-] cycle
- [-] repeat
- [-] repeatedly
- [-] iterate
- [-] re_all
- [-] re_iter

### Access
- [X] first (head)
- [-] second
- [X] last (last)
- [X] nth (get)
- [?] some -- first item matching predicate
- [ ] take (TODO)

### Slice
- [+] take
- [ ] drop (TODO)
- [X] rest (tail)
- [X] butlast (init)
- [-] takewhile
- [-] dropwhile
- [ ] split_at (TODO)
- [-] split_by

### Transform
- [X] map
- [?] mapcat (flat_map)
- [-] keep (filter(map(...)))
- [-] pluck
- [-] pluck_attr
- [-] invoke

### Filter
- [ ] filter
- [ ] remove (filter_not)
- [-] keep (duplicate)
- [-] distinct (just do set(List))
- [-] where
- [?] without(seq, *items) -- returns sequence with items removed

### Join
- [X] cat (flatten)
- [-] concat
- [-] flatten
- [+] mapcat
- [?] interleave
- [ ] interpose (intercalate) (TODO)

### Partition
- [-] chunks(seq, length, include_remainder=False)
- [ ] (NEW) chunk(seq, n)
- [-] partition
- [-] partition_by
- [+] split_at
- [-] split_by

### Group
- [ ] split (partition)
- [-] count_by
- [-] count_reps
- [ ] group_by
- [-] group_by_keys
- [?] group_values

### Aggregate
- [-] ilen
- [-] reductions
- [-] sums
- [-] all
- [-] any
- [-] none
- [-] one
- [-] count_by
- [-] count_reps

### Iterate
- [-] pairwise
- [-] with_prev
- [-] with_next
- [-] zip_values
- [-] zip_dicts
- [-] tree_leaves
- [-] tree_nodes
