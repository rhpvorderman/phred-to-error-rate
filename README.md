# phred-to-error-rate
Convert FASTQ phred scores to probabilities

## Calculating the score
Actually calculating the score requires calculating an exponent of 10. 
This is a lot slower than doing the lookup. Doing this is not recommended.

## Using a lookup table

FASTQ phred scores have a maximum of 94 discrete values. The lower bound is 33
the upper bound is 126. The current fastest 
way is to use a lookup table. One can be easily generated in python:

```python3
PHRED_TO_SCORE_LOOKUP = [10 ** (-(i -33) / 10) for i in range (127)]
```

Using [dnaio](https://github.com/marcelm/dnaio) one can easily calculate
the average probability for each read:
```python3

import math 

import dnaio

PHRED_TO_SCORE_LOOKUP = [10 ** (-(i -33) / 10) for i in range (127)]

for read in dnaio.open("my.fastq"):
    phreds = read.qualities_as_bytes()
    total_expected_errors = 0.0
    for phred in phreds:  # iterating over bytes gives integers
        total_expected_errors += PHRED_TO_SCORE_LOOKUP[phred]
    average_error_rate = total_expected_errors / len(read)
    read_phred_score = -10 * math.log10(average_error_rate)
```

This is how to do it in C.

```C
#include <score_to_error_rate.h>
#include <stdint.h>

static inline double
average_error_rate(const uint8_t *phreds, size_t phreds_length) {
    const uint8_t *end_ptr = phreds + phreds_length;
    const uint8_t *cursor = phreds;
    double error_rate = 0.0;
    while (cursor < end_ptr) {
        uint8_t phred = *cursor - 33; 
        /* Because phred is unsigned, we only have to check the upper bound */
        if (phred > 93) {
            return -1.0;  // Error rate should always be positive, so this is a good error value.
        }
        error_rate += SCORE_TO_ERROR_RATE[phred];
        cursor += 1;
    }
    return error_rate / (double)phreds_length;
}
```

Code to generate score_to_error_rate.h is included 
[here](score_to_error_rate.py). An already produced example can be obtained 
[here](score_to_error_rate.h).
