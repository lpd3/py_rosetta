# Find Largest Left Truncatable Prime in a Given Base

'''A truncatable prime is one where all non-empty substrings that finish at the
end of the number (right-substrings) are also primes when understood as numbers
in a particular base. The largest such prime in a given (integer) base is there-
fore computable, provided the base is larger than 2.

Let's consider what happens in base 10. Obviously the right most digit must be
prime, so in base 10 candidates are 2,3,5,7. Putting a digit in the range 1 to 
base-1 in front of each candidate must result in a prime. So 2 and 5, like the 
whale and the petunias in The Hitchhiker's Guide to the Galaxy, come into exis-
tence only to be extinguished before they have time to realize it, because 2
and 5 preceded by any digit in the range 1 to base-1 is not prime. Some numbers
formed by preceding 3 or 7 by a digit in the range 1 to base-1 are prime. So
13,17,23,37,43,47,53,67,73,83,97 are candidates. Again, putting a digit in the
range 1 to base-1 in front of each candidate must be a prime. Repeating until
there are no larger candidates finds the largest left truncatable prime.

Let's work base 3 by hand:

0 and 1 are not prime so the last digit must be 2. 123 = 510 which is prime,
223 = 810 which is not so 123 is the only candidate. 1123 = 1410 which is not
prime, 2123 = 2310 which is, so 2123 is the only candidate. 12123 = 5010 which
is not prime, 22123 = 7710 which also is not prime. So there are no more candi-
dates, therefore 23 is the largest left truncatable prime in base 3.

The task is to reconstruct as much, and possibly more, of the table in the OEIS 
as you are able.'''


from primePy import primes

DIGITS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


