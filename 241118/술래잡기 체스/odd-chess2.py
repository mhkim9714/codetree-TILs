import copy

# ↑0, ↖1, ←2, ↙3, ↓4, ↘5, →6, ↗7
di = [-1,-1,0,1,1,1,0,-1]
dj = [0,-1,-1,-1,0,1,1,1]

arr = [[0 for _ in range(4)] for _ in range(4)]  # 각 좌표별 -> 숫자 인덱스
numbers = dict()  # 각 숫자 인덱스 별 -> [(좌표),방향]
for i in range(4):
    tmp = list(map(int, input().split()))
    arr[i][0] = tmp[0]
    numbers[tmp[0]] = [(i, 0), tmp[1]-1]
    arr[i][1] = tmp[2]
    numbers[tmp[2]] = [(i, 1), tmp[3]-1]
    arr[i][2] = tmp[4]
    numbers[tmp[4]] = [(i, 2), tmp[5]-1]
    arr[i][3] = tmp[6]
    numbers[tmp[6]] = [(i, 3), tmp[7]-1]


def backtracking(score, arr, numbers, Ti, Tj, Td):  # arr/numbers <- 술래가 located인 상태
    global max_score

    # 도둑말 이동 (arr, numbers update)
    sorted_numbers = dict(sorted(numbers.items()))
    for cn, info in sorted_numbers.items():
        ci,cj,cd = info[0][0],info[0][1],info[1]
        for dd in range(8):
            final_cd = (cd+dd)%8
            ni,nj = ci+di[final_cd], cj+dj[final_cd]
            if 0<=ni<4 and 0<=nj<4 and (ni,nj) != (Ti,Tj):  # 이동 가능 {cn,ci,cj,final_cd} <-> {nn,ni,nj,nd}
                if arr[ni][nj] == 0:  # 빈칸
                    arr[ci][cj] = 0
                    arr[ni][nj] = cn
                    sorted_numbers[cn] = [(ni,nj),final_cd]
                else:  # 다른 도둑말 칸
                    nn,nd = arr[ni][nj], sorted_numbers[arr[ni][nj]][1]
                    arr[ci][cj] = nn
                    arr[ni][nj] = cn
                    sorted_numbers[cn] = [(ni,nj),final_cd]
                    sorted_numbers[nn] = [(ci,cj),nd]
                break

    # 잡을 수 있는 술래 candidate 구하기
    candidates = []
    nTi,nTj = Ti,Tj
    while True:
        nTi,nTj = nTi+di[Td], nTj+dj[Td]
        if 0<=nTi<4 and 0<=nTj<4:
            if arr[nTi][nTj] != 0:  # 도둑말이 있는 경우 -> candidates에 추가
                candidates.append(arr[nTi][nTj])
            else:  # 빈칸인 경우
                continue
        else:
            break

    if len(candidates) == 0:  # candidate 없으면 -> max_score 업데이트하고 return
        max_score = max(max_score, score)
        return
    else:  # candidate 있으면 -> candidate for loop 돌리면서 backtracking 재귀
        for n in candidates:  # n이라는 도둑말을 잡은 상태 (score, arr, numbers, Ti, Tj, Td update)
            Ti,Tj,Td = sorted_numbers[n][0][0], sorted_numbers[n][0][1], sorted_numbers[n][1]
            n_arr = [x[:] for x in arr]
            n_numbers = copy.deepcopy(sorted_numbers)
            n_arr[Ti][Tj] = 0
            del n_numbers[n]
            backtracking(score+n, n_arr, n_numbers, Ti, Tj, Td)


max_score = arr[0][0]
Ti,Tj,Td = 0,0,numbers[arr[0][0]][1]
del numbers[arr[0][0]]
arr[0][0] = 0
backtracking(max_score, arr, numbers, Ti, Tj, Td)
print(max_score)
