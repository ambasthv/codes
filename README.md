categorization for each variable then directly map to the treatments for invalid values, with the following logic:

1 Negative handling:
If only the denominator has potential for being negative: set to max
If both the numerator and denominator have potential for being negative: set to min if the denominator is negative
2 Zero handling:
If the numerator is not expected to have a zero value: set to null
3 Infinite handling (waterfall logic):
If both the numerator and denominator have potential for being negative: none (inf handled through capping and flooring)
If the denominator is not expected to have a zero value: set to null
If neither of the conditions above are met: set to max

