; p1: easy should have both strong and strong-cyclic solutions - just do sq and get the goal
(define (domain nooptest)
	(:requirements :strips)
	(:predicates
		(p)
		(q)
		(r)	;; totally irrelevant predicate
	)

	;; deterministically make q true
	(:action setq
		:parameters ()
		:precondition (p)
		:effect (q) 
	)
)
