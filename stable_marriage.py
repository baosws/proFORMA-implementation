def marry(men_prefers, women_prefers):
    n = len(men_prefers)
    wives = [-1] * n
    husbands = [-1] * n
    women_prefers_index = [[0] * n for i in range(n)]
    for woman in range(n):
        for i, man in zip(range(n), women_prefers[woman]):
            women_prefers_index[woman][man] = i
    while -1 in wives:
        single_man = wives.index(-1)
        for woman in men_prefers[single_man]:
            if husbands[woman] == -1:
                husbands[woman] = single_man
                wives[single_man] = woman
                break
            else:
                old_husband = husbands[woman]
                if women_prefers_index[woman][single_man] < women_prefers_index[woman][old_husband]:
                    wives[old_husband] = -1
                    husbands[woman] = single_man
                    wives[single_man] = woman
                    break
    return husbands, wives

men_prefers = [[0, 2, 1, 3],
               [2, 3, 0, 1],
               [3, 1, 2, 0],
               [2, 1, 0, 3]]

women_prefers = [[1, 0, 2, 3],
                 [3, 0, 1, 2],
                 [0, 2, 1, 3],
                 [1, 2, 0, 3]]

husbands, wives = marry(men_prefers, women_prefers)

for man in range(4):
    print(man, wives[man])
