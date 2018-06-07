# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

A word meaning lung disease caused by inhaling very fine ash and sand dust.

## According to its man page, what does `getrusage` do?

getrusage() get information about resource utilization.

## Per that same man page, how many members are in a variable of type `struct rusage`?

2 members are always present in the variable of type `struct rusage`, 14 are optional members.

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

This is because the function `calculate` dereferences the members of `before` and `after`, it would not make sense to create an unnecessary copy with the same original data performance wise.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

First, we create an `int` variable named `c` and use `fgetc` to obtain a character from `file`. Then, we place it inside `c`, and make sure its not an `EOF` character, or a `\0` character before iterating through the loop. Then, we check if `c` is an alphabetical character or apostrophe. If it is, append the character in `c` to the character array `word` and increase the `index` counter by one. While you are appending the characters in `c`, also check if `index` is larger than `LENGTH` which indicates that it is too long to be words. If however `c` is not an alphabetical character, such as being a number, this indicates the string is not a word. If `index` is larger than `LENGTH`, or if `c` contains a number, consume the remainder of the alphabetical string, and then reset the `index` to `0` to prepare for a new word. If however, `c` is a `\0`, also known as a `EOF` character, thus breaking the loop, and the `index` is not `0`, we can conclude the string is a word. Because the loop ends when `fgetc` reads the `\0` character into `c` and before it passes the `\0` character into `word`, we will have to terminate the current `word` array by adding another `\0` to the end of the string. Then, we will have to increase `words` counter by 1 to keep track of how many words we found. Afterwards, we call the `getrusage` function, passing the argument `RUSAGE_SELF` to keep a record of the resource and time usage by the calling process before the checking process starts, storing it in the `rusage` structure named `before`, then calling the function `check()` to check on the `word` if it exist in the dictionary, and storing the result in `misspelled` to indicate if the word is not found in the dictionary. Then, we call `getrusage` again and pass the argument `RUSAGE_SELF` to get the total time passed and resource used while check the spelling, and store the result in the `rusage` structure named `after`. Afterwards, we will update the benchmark by calling the calculate function and passing the pointers to the time values stored in `before` and `after`, acquring the time taken to check the  spelling, and add the return value by `calculate()`  to `time_check`, to record down how long it takes to check the spelling for all the words in `text`. Afterwards, if the word is mispelled, we will print it on the screen and increment the `mispellings` counter by 1. Regardless, to prepare for the next new word, we reset `index` to `0` before restarting the entire loop.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

Because by using `fscanf` we will not be able to evaluate how many words have been inputted into `word` while it is being passed into `word`. It would be possible that the user might have typed in something excessively long, causing the `word` array to overflow and might unintentionally write over other data in the memory.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

This is because we want to pass the parameters as reference to improve performance over making an entire copy of the same variable. However, we want to prevent those parameters from being modified by the programmer accidentally and potentially causing problems. Therefore, we declare it as a constant so that if any changes were to be made, a `segmentation fault` error would be thrown to stop the parameters from being accidentally altered, thus making tracking of bugs easier.