n = int(input())
arr = [list(map(int, input().split())) for _ in range(n)]
ans = 0

# 좌(0) 하(1) 우(2) 상(3)
di = [0, 1, 0, -1]
dj = [-1, 0, 1, 0]

length = 1
cnt = 0

pi,pj = int(n/2), int(n/2)
d = 0
end_flag = 0

def clean(ci,cj,d):
    global ans
    dust_total = arr[ci][cj]
    dust_processed = 0

    if 0<=ci+2*di[(d+3)%4]<n and 0<=cj+2*dj[(d+3)%4]<n:
        arr[ci+2*di[(d+3)%4]][cj+2*dj[(d+3)%4]] += int(dust_total * 0.02)
    else:
        ans += int(dust_total * 0.02)
    dust_processed += int(dust_total * 0.02)
    if 0<=ci+di[d]+di[(d+3)%4]<n and 0<=cj+dj[d]+dj[(d+3)%4]<n:
        arr[ci+di[d]+di[(d+3)%4]][cj+dj[d]+dj[(d+3)%4]] += int(dust_total * 0.1)
    else:
        ans += int(dust_total * 0.1)
    dust_processed += int(dust_total * 0.1)
    if 0<=ci+di[(d+3)%4]<n and 0<=cj+dj[(d+3)%4]<n:
        arr[ci+di[(d+3)%4]][cj+dj[(d+3)%4]] += int(dust_total * 0.07)
    else:
        ans += int(dust_total * 0.07)
    dust_processed += int(dust_total * 0.07)
    if 0<=ci+di[(d+3)%4]+di[(d+2)%4]<n and 0<=cj+dj[(d+3)%4]+dj[(d+2)%4]<n:
        arr[ci+di[(d+3)%4]+di[(d+2)%4]][cj+dj[(d+3)%4]+dj[(d+2)%4]] += int(dust_total * 0.01)
    else:
        ans += int(dust_total * 0.01)
    dust_processed += int(dust_total * 0.01)
    if 0<=ci+2*di[d]<n and 0<=cj+2*dj[d]<n:
        arr[ci+2*di[d]][cj+2*dj[d]] += int(dust_total * 0.05)
    else:
        ans += int(dust_total * 0.05)
    dust_processed += int(dust_total * 0.05)
    if 0<=ci+di[d]+di[(d+1)%4]<n and 0<=cj+dj[d]+dj[(d+1)%4]<n:
        arr[ci+di[d]+di[(d+1)%4]][cj+dj[d]+dj[(d+1)%4]] += int(dust_total * 0.1)
    else:
        ans += int(dust_total * 0.1)
    dust_processed += int(dust_total * 0.1)
    if 0<=ci+di[(d+1)%4]<n and 0<=cj+dj[(d+1)%4]<n:
        arr[ci+di[(d+1)%4]][cj+dj[(d+1)%4]] += int(dust_total * 0.07)
    else:
        ans += int(dust_total * 0.07)
    dust_processed += int(dust_total * 0.07)
    if 0<=ci+di[(d+2)%4]+di[(d+1)%4]<n and 0<=cj+dj[(d+2)%4]+dj[(d+1)%4]<n:
        arr[ci+di[(d+2)%4]+di[(d+1)%4]][cj+dj[(d+2)%4]+dj[(d+1)%4]] += int(dust_total * 0.01)
    else:
        ans += int(dust_total * 0.01)
    dust_processed += int(dust_total * 0.01)
    if 0<=ci+2*di[(d+1)%4]<n and 0<=cj+2*dj[(d+1)%4]<n:
        arr[ci+2*di[(d+1)%4]][cj+2*dj[(d+1)%4]] += int(dust_total * 0.02)
    else:
        ans += int(dust_total * 0.02)
    dust_processed += int(dust_total * 0.02)
    if 0<=ci+di[d]<n and 0<=cj+dj[d]<n:
        arr[ci+di[d]][cj+dj[d]] += (dust_total - dust_processed)
    else:
        ans += (dust_total - dust_processed)
    
while True:
    # 전진
    for _ in range(length):
        ci,cj = pi+di[d],pj+dj[d]
        # 먼지 청소
        clean(ci,cj,d)
        if (ci,cj) == (0,0):
            end_flag = 1
            break
        pi,pj = ci,cj
    
    if end_flag == 1:
        break

    cnt += 1
    d = (d+1)%4

    if cnt == 2:
        length += 1
        cnt = 0

print(ans)