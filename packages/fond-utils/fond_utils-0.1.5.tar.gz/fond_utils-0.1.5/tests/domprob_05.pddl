; domain + propblem in one file
(define (domain blocks-domain)
  (:requirements :non-deterministic :equality :typing)
  (:types
    block
  )
  (:predicates
    (holding ?b - block)
    (emptyhand)
    (emptyhead)
    (on-table ?b - block)
    (on ?b1 ?b2 - block)
    (clear ?b - block)
  )
  (:action pick-up
    :parameters (?b1 ?b2 - block)
    :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
    :effect (oneof
      (and (holding ?b1) (clear ?b2) (not (emptyhand)) (not (clear ?b1)) (not (on ?b1 ?b2)))
      (and (clear ?b2) (on-table ?b1) (not (on ?b1 ?b2))))
  )
  (:action pick-up-empty
    :parameters (?b1 ?b2 - block)
    :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
    :effect (oneof
      (and)
      (and (clear ?b2) (on-table ?b1) (not (on ?b1 ?b2))))
  )
  (:action pick-up-complex01
    :parameters (?b1 ?b2 - block)
    :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
    :effect (and
      (clear ?b2) (clear ?b1)
      (oneof
        (and (holding ?b1) (clear ?b2) (not (emptyhand)) (not (clear ?b1)) (not (on ?b1 ?b2)))
        (and (clear ?b2) (on-table ?b1) (not (on ?b1 ?b2))))
    )
  )
  (:action pick-up-super-complex
    :parameters (?b1 ?b2 - block)
    :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
    :effect (and
      (emptyhead)
      (oneof
        (and (clear ?b2) (clear ?b1))
        (and (holding ?b2) (holding ?b1)))
      (oneof
        (and (emptyhand) (holding ?b1))
        (and (emptyhand) (oneof (holding ?b2) (on ?b1 ?b2)))))

    ;; RESULT NORMALIZED:
    ;:effect (oneof
    ;  (and (emptyhead) (clear ?b2) (clear ?b1) (emptyhand) (holding ?b1))
    ;  (and (emptyhead) (clear ?b2) (clear ?b1) (emptyhand) (holding ?b2))
    ;  (and (emptyhead) (clear ?b2) (clear ?b1) (emptyhand) (on ?b1 ?b2))
    ;  (and (emptyhead) (holding ?b2) (holding ?b1) (emptyhand))
    ;  (and (emptyhead) (holding ?b2) (holding ?b1) (emptyhand))
    ;  (and (emptyhead) (holding ?b2) (holding ?b1) (emptyhand) (on ?b1 ?b2)))
  )
)
(define (problem bw_5_1)
  (:domain blocks-domain)
  (:objects
    b1 b2 b3 b4 b5 - block
  )
  (:init
    (emptyhand)
    (on b1 b3)
    (on b2 b1)
    (on-table b3)
    (on-table b4)
    (on b5 b4)
    (clear b2)
    (clear b5)
  )
  (:goal
    (and (emptyhand) (on b1 b2) (on b2 b5) (on-table b3) (on-table b4) (on-table b5) (clear b1) (clear b3) (clear b4))
  )
)