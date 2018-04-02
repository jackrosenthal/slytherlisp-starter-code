#!/usr/bin/env slyther
(define (prng seed)
  ; Lehmer random number generator
  (lambda ()
    (set! seed (remainder (* 16807 seed) 2147483647))
    seed))

(define (n-calls f args n)
  (if (< n 1)
      NIL
      ((lambda ()
         (print (eval (cons f args)))
         (n-calls f args (- n 1))))))

(define rng1 (prng 1))
(print "Testing rng1...")
(n-calls rng1 () 8)

(define rng2 (prng 1))
(print "\nTesting rng2...")
(n-calls rng2 () 8)

(print "\nThe original pRNG should be unharmed!")
(n-calls rng1 () 8)

(print "\nShould be the same as:")
(n-calls rng2 () 8)
