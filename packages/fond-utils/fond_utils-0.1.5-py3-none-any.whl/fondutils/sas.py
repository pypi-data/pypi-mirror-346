

def confirm_all_outcomes(domain, sfile, detdup="_DETDUP"):
    """
    Confirm that every outcome in the domain file is also in the sas file for every ground action.
    """

    print("\n  Confirming outcomes in sas file...\n")

    assert "(oneof" not in str(domain), "Domain should be deterministic"

    action_to_outcome_count = {}
    for action in domain.actions:
        nondet_action = action.name.split(detdup)[0]
        if nondet_action not in action_to_outcome_count:
            action_to_outcome_count[nondet_action] = 0
        action_to_outcome_count[nondet_action] += 1

    ground_action_details = {}
    with open(sfile, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("begin_operator"):
            action = lines[i + 1].strip()
            args = " ".join(action.split(" ")[1:])
            action_name = action.split(' ')[0].split(detdup.lower())[0]

            if action_name not in ground_action_details:
                ground_action_details[action_name] = {}

            if args not in ground_action_details[action_name]:
                ground_action_details[action_name][args] = 0

            ground_action_details[action_name][args] += 1

    wrong = 0
    for a in ground_action_details:
        for args in ground_action_details[a]:
            if ground_action_details[a][args] != action_to_outcome_count[a]:
                print(f"Error: Action {a} with args {args} has {ground_action_details[a][args]} outcome(s) in sas file, but {action_to_outcome_count[a]} in domain file.")
                wrong += 1

    if wrong == 0:
        print("\nAll outcomes confirmed.\n")
    else:
        print(f"\n{wrong} outcome(s) not confirmed.\n")
