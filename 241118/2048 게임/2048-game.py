n = int(input())
arr = [list(map(int, input().split())) for _ in range(n)]

def backtracking(cnt, val, arr):
    global max_val
    if cnt == 5:
        max_val = max(max_val, val)
        return

    for d in range(4):
        # 고른 방향에 대한 중력 작용 코드 -> narr 생성
        narr = [[0 for _ in range(n)] for _ in range(n)]

        if d == 0:  # 위쪽 중력
            for j in range(n):  # 각 열에 대해 처리
                tmp = []
                for i in range(n):
                    if arr[i][j] != 0:
                        tmp.append(arr[i][j])
                r_idx = 0
                while tmp:
                    cn = tmp.pop(0)
                    if len(tmp) == 0 or cn != tmp[0]:  # narr에 입력
                        narr[r_idx][j] = cn
                        r_idx += 1
                    else:  # 융합
                        nn = tmp.pop(0)
                        narr[r_idx][j] = 2*cn
                        r_idx += 1

        elif d == 1:  # 아래쪽 중력
            for j in range(n):  # 각 열에 대해 처리
                tmp = []
                for i in range(n-1,-1,-1):
                    if arr[i][j] != 0:
                        tmp.append(arr[i][j])
                r_idx = n-1
                while tmp:
                    cn = tmp.pop(0)
                    if len(tmp) == 0 or cn != tmp[0]:  # narr에 입력
                        narr[r_idx][j] = cn
                        r_idx -= 1
                    else:  # 융합
                        nn = tmp.pop(0)
                        narr[r_idx][j] = 2*cn
                        r_idx -= 1

        elif d == 2:  # 왼쪽 중력
            for i in range(n):  # 각 행에 대해 처리
                tmp = []
                for j in range(n):
                    if arr[i][j] != 0:
                        tmp.append(arr[i][j])
                c_idx = 0
                while tmp:
                    cn = tmp.pop(0)
                    if len(tmp) == 0 or cn != tmp[0]:  # narr에 입력
                        narr[i][c_idx] = cn
                        c_idx += 1
                    else:  # 융합
                        nn = tmp.pop(0)
                        narr[i][c_idx] = 2*cn
                        c_idx += 1

        else:  # 오른쪽 중력
            for i in range(n):  # 각 행에 대해 처리
                tmp = []
                for j in range(n-1,-1,-1):
                    if arr[i][j] != 0:
                        tmp.append(arr[i][j])
                c_idx = n-1
                while tmp:
                    cn = tmp.pop(0)
                    if len(tmp) == 0 or cn != tmp[0]:  # narr에 입력
                        narr[i][c_idx] = cn
                        c_idx -= 1
                    else:  # 융합
                        nn = tmp.pop(0)
                        narr[i][c_idx] = 2*cn
                        c_idx -= 1

        backtracking(cnt+1, max(max(row) for row in narr), narr)


max_val = -1
backtracking(0, max(max(row) for row in arr), arr)
print(max_val)

