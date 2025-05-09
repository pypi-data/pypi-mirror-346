(define (domain nooptest)
	(:requirements :strips)
	(:predicates
		(p)
		(q)
	)

	;; deterministically make q true
	(:action setq
		:parameters ()
		:precondition (p)
		:effect (q) 
	)
	(:action bad
		:parameters ()
		:precondition ()
		:effect (not (p))
	)
)
