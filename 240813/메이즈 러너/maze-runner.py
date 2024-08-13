N,M,K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
people = []
for _ in range(M):
    i,j = map(int, input().split())
    people.append((i-1,j-1))
exi,exj = map(int, input().split())
exi,exj = exi-1,exj-1


def dist(si,sj,ei,ej):
    return abs(si-ei)+abs(sj-ej)


ans = 0
for _ in range(K):
    if len(people) == 0:
        break

    # 모든 참가자 동시에 이동
    new_people = []
    for (i,j) in people:
        min_dist = dist(i,j,exi,exj)
        new_coord = (i,j)
        for ni,nj in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
            if 0<=ni<N and 0<=nj<N and arr[ni][nj]==0 and dist(ni,nj,exi,exj)<min_dist:
                min_dist = dist(ni,nj,exi,exj)
                new_coord = (ni,nj)
        if new_coord != (i,j):
            ans += 1
        if new_coord != (exi,exj):
            new_people.append(new_coord)
    people = new_people

    # 미로 회전
    min_i,min_j,min_square = N,N,N+1
    for (i,j) in people:
        square = dist(i,j,exi,exj)+1
        pi = max(0, max(i,exi)-(square-1))
        pj = max(0, max(j,exj)-(square-1))

        if min_square > square:
            min_i,min_j,min_square = pi,pj,square
        elif min_square == square:
            if min_i > pi:
                min_i,min_j,min_square = pi,pj,square
            elif min_i == pi:
                if min_j > pj:
                    min_i,min_j,min_square = pi,pj,square

    narr = [x[:] for x in arr]
    nexi,nexj = exi,exj
    for i in range(min_i,min_i+min_square):
        for j in range(min_j,min_j+min_square):
            narr[min_i+j-min_j][min_j+min_square-1-i+min_i] = max(arr[i][j]-1,0)
            if (i,j) == (exi,exj):
                nexi,nexj = min_i+j-min_j, min_j+min_square-1-i+min_i
    arr = narr
    exi,exj = nexi,nexj

    new_people = []
    for (i,j) in people:
        if min_i<=i<min_i+min_square and min_j<=j<min_j+min_square:
            new_people.append((min_i+j-min_j, min_j+min_square-1-i+min_i))
        else:
            new_people.append((i,j))
    people = new_people

print(ans)
print(f'{exi+1} {exj+1}')