from data import Office, Cohort

import itertools as it
import copy


def do_pick(pair, avail, n_cohort, ucc_left, pick):
    if pair.cohort != Cohort.ssenior:
        n_cohort[pair.cohort] += 1
        ucc_left[pair.cohort] -= pair.ucc
    alley, room = pick
    pair.result = (alley, room)
    avail[alley].remove(room)


def try_pick(pair, avail, n_cohort, ucc_left):
    for alley, room in p.prefs:
        if room not in avail[alley]:
            continue
        if not p.ucc and len(avail[alley]) == 1:
            continue
        do_pick(p, avail, n_cohort, ucc_left, (alley, room))
        return True
    return False


def run_roompicks(avail, pairs):
    """Run roompicks, modifying p.result for each pair p, and returning the list.

    avail -- a dictionary mapping each alley to the list of non-frosh rooms
    pairs - a list of `data.RoommatePair`s
    """

    avail = copy.copy(avail)
    n = sum(len(rooms) for rooms in avail.values())
    pairs.sort()

    it_ = iter(pairs)
    norm_pairs = list(it.takewhile(lambda p: p.cohort != Cohort.ssenior, it_))
    sseniors = list(it_)

    ucc_left = [0, 0, 0]
    for p in norm_pairs:
        if p.ucc:
            ucc_left[p.cohort] += 1
    n_cohort = [0, 0, 0]
    prez = norm_pairs[0]
    assert prez.pick.office == Office.president
    do_pick(prez, avail, n_cohort, ucc_left, prez.prefs[0])

    guaranteed_healthads = prez.healthad + sum(p.healthad for p in norm_pairs[1:] if p.ucc)
    not_guaranteed_healthads = [p.healthad for p in norm_pairs[1:] if p.healthad and not p.ucc]

    pass_number = 0
    while True:
        if pass_number > 0:
            n_cohort = [0, 0, 0]
            assert ucc_left == [0, 0, 0] and guaranteed_healthads >= 2
        cur = Cohort.senior
        n_cur = (4*n + 9) // 10
        n -= n_cur
        for p in norm_pairs[1:]:
            if p.result != None:
                continue
            if cur != p.cohort:
                if p.cohort == Cohort.junior:
                    n_cur = (n + n_cur - n_cohort[cur] + 1) // 2
                    n -= n_cur
                else:
                    n_cur = n + n_cur - n_cohort[cur]
                    n = 0
                cur = p.cohort
            if p.healthad and not p.ucc:
                not_guaranteed_healthads.pop(0)
            if not p.ucc and n_cohort[cur] + ucc_left[cur] >= n_cur:
                continue
            if cur == Cohort.junior and not p.ucc and not p.healthad and guaranteed_healthads < 2:
                n_free = n_cur - n_cohort[cur] - ucc_left[cur]
                if guaranteed_healthads == 1 or not_guaranteed_healthads[0] == 2:
                    if n_free <= 1:
                        continue
                else:
                    if n_free <= 2:
                        continue
            got_one = try_pick(p, avail, n_cohort, ucc_left)
            if got_one and not p.ucc:
                guaranteed_healthads += p.healthad
        n = n_cur - n_cohort[cur]
        pass_number += 1
        if n == 0 or not any(p.result == None for p in norm_pairs[1:]):
            break

    for p in sseniors:
        try_pick(p, avail, n_cohort, ucc_left)

    return pairs
