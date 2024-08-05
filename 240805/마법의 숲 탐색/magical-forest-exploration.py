R,C,K = map(int, input().split())

arr = [[0]*C for _ in range(R+3)]
monster = dict() # [(중앙좌표), 방향인덱스]

# 상(0) 우(1) 하(2) 좌(3)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

ans = 0
for k in range(1,K+1):
    j,d = map(int, input().split())
    i,j = 1,j-1

    while True:
        if 0<=(i+2)<R+3 and arr[i+1][j-1]==0 and arr[i+2][j]==0 and arr[i+1][j+1]==0: # 남쪽 이동 조건
            i,j = i+1,j
            continue
        elif 0<=(i+2)<R+3 and 0<=(j-2)<C and \
            arr[i-1][j-1]==0 and arr[i][j-2]==0 and arr[i+1][j-2]==0 and arr[i+1][j-1]==0 and arr[i+2][j-1]==0: # 서쪽 이동 조건
            i,j = i+1,j-1
            d = (d+3)%4
            continue
        elif 0<=(i+2)<R+3 and 0<=(j+2)<C and \
            arr[i-1][j+1]==0 and arr[i][j+2]==0 and arr[i+1][j+1]==0 and arr[i+1][j+2]==0 and arr[i+2][j+1]==0: # 동쪽 이동 조건
            i,j = i+1,j+1
            d = (d+5)%4
        else: # 아무 이동도 불가능 할때가 다다르면

            if i<4: # 골렘의 몸이 격자 밖에 삐져나온 경우
                arr = [[0]*C for _ in range(R+3)]
                monster = dict()
                break

            else: # 격자내에 안착 후 정령 이동, ans 누적
                # 격자내에 저장
                for fi,fj in ((i,j),(i-1,j),(i,j+1),(i+1,j),(i,j-1)):
                    arr[fi][fj] = k
                monster[k] = [(i,j),d]

                # 정령 이동
                bi,bj = i+1,j
                gi,gj = i+di[d],j+dj[d]

                q,finals,visited = [],[],[] # q:게이트 좌표, finals:bottom의 i좌표, visited:방문한 골렘 인덱스

                finals.append(bi)
                q.append((gi,gj))
                visited.append(k)

                while q:
                    ci,cj = q.pop(0)
                    for ni,nj in ((ci-1,cj),(ci,cj+1),(ci+1,cj),(ci,cj-1)):
                        if 0<=ni<(R+3) and 0<=nj<C and arr[ni][nj]!=0 and arr[ni][nj]!=arr[ci][cj] and arr[ni][nj] not in visited:
                            bi,bj = monster[arr[ni][nj]][0][0]+1, monster[arr[ni][nj]][0][1]
                            gi,gj = monster[arr[ni][nj]][0][0]+di[monster[arr[ni][nj]][1]], monster[arr[ni][nj]][0][1]+dj[monster[arr[ni][nj]][1]]
                            finals.append(bi)
                            q.append((gi,gj))
                            visited.append(arr[ni][nj])

                ans += (max(finals)-2)
                break

print(ans)