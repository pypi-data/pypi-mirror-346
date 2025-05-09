(define (domain nooptest)
    (:requirements :strips)
    (:predicates (p) (q) (r))
    (:action sq_DETDUP_1
        :parameters ()
        :precondition (p)
        :effect (q)
    )
     (:action sq_DETDUP_2
        :parameters ()
        :precondition (p)
        :effect (and )
    )
)
