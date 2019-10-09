### function to return a list of consecutive slices, up to the length of the full list
### for [1,2,3] the return should be [[1,2,3], [2,3], [1,2], [3], [2], [1]]
### longer sets and sets towards the back end of the original list come first

### this is the foundation to be used to start looking for wordifications or shorter length,


ex_digits = [1,2,3,4,5,6,7]

def return_consecutive_slices(test_list):
    slice_options = []
    for i in reversed(range(len(test_list))):
        slots_to_grab = i + 1
        index_f = len(test_list) 
        while index_f - slots_to_grab >= 0: 
            index_i = index_f - slots_to_grab
            new_slice = test_list[index_i:index_f]
            slice_options.append(new_slice)
            index_f -= 1
    return slice_options

        
    
test = return_consecutive_slices(ex_digits)
for t in test:
    print t

