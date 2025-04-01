import sys
sys.stdin = open('input.txt', 'r')

R, C, K = map(int, input().split())

di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

arr = [[0 for _ in range(C)] for _ in range(R+3)]
golem = dict()

# 골렘 북쪽에서 들어올때 마다,
answer = 0
for idx in range(1, K+1):  # O(1000)
    c_idx, d_idx = map(int, input().split())

    i, j = 1, c_idx-1
    while True:  # O(70)
        # (1) 남쪽으로 한칸 내려감 (3칸 체크)
        if 0<=i+2<R+3 and 0<=j-1<C and 0<=j+1<C and arr[i+1][j-1]==0 and arr[i+2][j]==0 and arr[i+1][j+1]==0:
            i, j = i+1, j

        # (2) (1)이 안되면 -> 서쪽 방향으로 회전하면서 내려감, 출구 반시계 이동 (5칸 체크)
        elif 0<=i+2<R+3 and 0<=j-2<C and arr[i-1][j-1]==0 and arr[i][j-2]==0 and arr[i+1][j-2]==0 and arr[i+1][j-1]==0 and arr[i+2][j-1]==0:
            i, j = i+1, j-1
            d_idx = (d_idx-1)%4

        # (3) (1),(2)이 안되면 -> 동쪽 방향으로 회전하면서 내려감, 출구 시계 이동 (5칸 체크)
        elif 0<=i+2<R+3 and 0<=j+2<C and arr[i-1][j+1]==0 and arr[i][j+2]==0 and arr[i+1][j+2]==0 and arr[i+1][j+1]==0 and arr[i+2][j+1]==0:
            i, j = i+1, j+1
            d_idx = (d_idx+1)%4

        # (4) 아무 이동도 못하면:
        else:
            # IF 골렘 몸이 격자 밖에 삐져나가 있으면:
            if 0<=i-1<3:
                # 전체 초기화 후 break (while 문 나가서 다음 골렘 받음)
                arr = [[0 for _ in range(C)] for _ in range(R+3)]
                golem = dict()
                break

            else:
                # 골렘 최종 위치 저장
                arr[i-1][j], arr[i][j-1], arr[i][j], arr[i][j+1], arr[i+1][j] = idx, idx, idx, idx, idx
                golem[idx] = [(i, j), d_idx]  # [중앙 좌표, 출구 방향 인덱스]

                # 정령 이동할 수 있는 가장 남쪽의 칸 찾기
                max_i = -1
                golem_idx_stack = [idx]
                visited = [idx]
                while golem_idx_stack:
                    g_idx = golem_idx_stack.pop(0)

                    # 현재 가장 남쪽
                    max_i = max(max_i, golem[g_idx][0][0]+1)
                    # 출구
                    exi, exj = golem[g_idx][0][0]+di[golem[g_idx][1]], golem[g_idx][0][1]+dj[golem[g_idx][1]]
                    for d in range(4):
                        nexi, nexj = exi+di[d], exj+dj[d]
                        if 0<=nexi<R+3 and 0<=nexj<C and arr[nexi][nexj]!=0 and arr[nexi][nexj] not in visited:
                            golem_idx_stack.append(arr[nexi][nexj])
                            visited.append(arr[nexi][nexj])

                # 정령 최종 위치 누적
                answer += (max_i-2)
                # break (while 문 나가서 다음 골렘 받음)
                break

print(answer)
