N,M,K = map(int, input().split())

gun = [[set() for _ in range(N)] for _ in range(N)] # set: set.add(n), set.remove(n)
for i in range(N):
    temp = list(map(int, input().split()))
    for j in range(N):
        gun[i][j].add(temp[j])

# 방향 0(상) 1(우) 2(하) 3(좌)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

player = [] # [i,j,d,n,g,score]
for _ in range(M):
    temp = list(map(int, input().split()))
    temp[0], temp[1] = temp[0]-1, temp[1]-1
    temp += [0,0]
    player.append(temp)


for _ in range(K):
    for p in player:
        # [1] 플레이어 이동
        ni = p[0] + di[p[2]]
        nj = p[1] + dj[p[2]]
        if 0<=ni<N and 0<=nj<N:
            p[0], p[1] = ni, nj
        else:
            p[2] = (p[2]+2)%4
            ni = p[0] + di[p[2]]
            nj = p[1] + dj[p[2]]
            p[0], p[1] = ni, nj

        # [2] 전투
        cur_player_loc = []
        for pp in player:
            if p == pp:
                cur_player_loc.append((-1,-1)) # dummy value for myself
            else:
                cur_player_loc.append((pp[0],pp[1]))

        # [2-1] 총 줍기
        if (p[0],p[1]) not in cur_player_loc:
            max_val = max(gun[p[0]][p[1]])
            if max_val > p[-2]:
                gun[p[0]][p[1]].remove(max_val)
                gun[p[0]][p[1]].add(p[-2])
                p[-2] = max_val

        # [2-2] 전투
        else:
            pp = player[cur_player_loc.index((p[0],p[1]))] # 상대
            if p[3]+p[4] > pp[3]+pp[4]:
                win, lose = p, pp
            elif p[3]+p[4] < pp[3]+pp[4]:
                win, lose = pp, p
            else:
                if p[3] > pp[3]:
                    win, lose = p, pp
                elif p[3] < pp[3]:
                    win, lose = pp, p
                else:
                    break

            win[-1] += (win[3]+win[4]-lose[3]-lose[4])

            # lose 총 버리기
            gun[p[0]][p[1]].add(lose[-2])
            lose[-2] = 0

            # lose 이동
            while True:
                lni = lose[0]+di[lose[2]]
                lnj = lose[1]+dj[lose[2]]
                if 0<=lni<N and 0<=lnj<N and (lni,lnj) not in cur_player_loc:
                    lose[0],lose[1] = lni,lnj
                    break
                else:
                    lose[2] = (lose[2]+1)%4
                    continue

            # lose 총 줍기
            max_val = max(gun[lose[0]][lose[1]])
            if max_val > 0:
                gun[lose[0]][lose[1]].remove(max_val)
                gun[lose[0]][lose[1]].add(0)
                lose[-2] = max_val

            # win 총 줍기
            max_val = max(gun[win[0]][win[1]])
            if max_val > win[-2]:
                gun[win[0]][win[1]].remove(max_val)
                gun[win[0]][win[1]].add(win[-2])
                win[-2] = max_val

str = ""
for p in player:
    str += f"{p[-1]} "
print(str)