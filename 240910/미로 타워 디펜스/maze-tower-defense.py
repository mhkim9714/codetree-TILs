n,m = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]

# →0  ↓1  ←2  ↑3
di = [0, 1, 0, -1]
dj = [1, 0, -1, 0]

loc = [(0,0)]
monster = [arr[0][0]]

i,j,d = 0,0,0
mx_cnt, cnt, flag = n,1,1
M = n//2

while True:
    cnt += 1
    i,j = i+di[d], j+dj[d]

    loc.append((i,j))
    monster.append(arr[i][j])

    if (i,j) == (M,M-1):
        break
    else:
        if cnt == mx_cnt: # 방향 변경
            cnt = 0
            d = (d+1) % 4
            if flag == 0: # 두번에 한번씩 길이 감소
                flag = 1
            else:
                flag = 0
                mx_cnt -= 1

loc = loc[::-1]
monster = monster[::-1]

def fill():
    global monster
    new_monster = [0 for _ in range(len(loc))]
    cnt = 0
    for i in range(len(loc)):
        if monster[i] > 0:
            new_monster[cnt] = monster[i]
            cnt += 1
    monster = new_monster

def check_4():
    global monster, score
    exist = 0
    indices_4, val = [], 0
    for i in range(len(loc)):
        if monster[i] > 0:
            if val == monster[i]:
                indices_4.append(i)
            else:
                if len(indices_4) >= 4:
                    exist = 1
                    for idx in indices_4:
                        score += monster[idx]
                        monster[idx] = 0
                indices_4 = [i]
                val = monster[i]

    if len(indices_4) >= 4:
        exist = 1
        for idx in indices_4:
            score += monster[idx]
            monster[idx] = 0

    return exist



score = 0
for _ in range(m):
    # 플레이어 공격
    d,p = map(int, input().split())
    for a in range(1,p+1):
        attk_i,attk_j = M+a*di[d], M+a*dj[d]
        idx = loc.index((attk_i,attk_j))
        score += monster[idx]
        monster[idx] = 0

    # 빈공간 채우기
    fill()

    # 4반복 처리
    while True:
        if check_4() == 0:  # 4반복 없음
            break
        else:
            fill()
    
    # 몬스터 나열 및 변환
    new_monster = []
    cnt, val = 0, 0
    for i in range(len(loc)):
        if monster[i] > 0:
            if val == monster[i]:
                cnt += 1
            else:
                if cnt >= 1:
                    new_monster.append(cnt)
                    new_monster.append(val)

                cnt = 1
                val = monster[i]

    if cnt >= 1:
        new_monster.append(cnt)
        new_monster.append(val)

    if len(new_monster) > len(monster):
        new_monster = new_monster[:len(monster)]
    elif len(new_monster) < len(monster):
        for _ in range(len(monster) - len(new_monster)):
            new_monster.append(0)

    monster = new_monster

print(score)