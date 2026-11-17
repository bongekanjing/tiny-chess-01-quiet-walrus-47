import json
import os
import random
import sys
import urllib.error
import urllib.request
MATE = 29000
INF = 30000
BUDGET = int(os.environ.get('TC_NODES', '300000'))
VAL = (0, 100, 320, 330, 500, 900, 0)
Q = '0123456789ABCDEFGHIJK'
PS = (
    'AAAAAAAAKKKKKKKKCCEGGECCBBCFFCBBAAAEEAAAB98AA89BBCC66CCBAAAAAAAA',
    '0244442026AAAA624ACDDCA44BDEEDB44ADEEDA44BCDDCB426ABBA6202444420',
    '688888868AAAAAA88ABCCBA88BBCCBB88ACCCCA88CCCCCC88BAAAAB868888886',
    'AAAAAAAABCCCCCCB9AAAAAA99AAAAAA99AAAAAA99AAAAAA99AAAAAA9AAABBAAA',
    '688998868AAAAAA88ABBBBA89ABBBBA9AABBBBA98BBBBBA88ABAAAA868899886',
    '422002244220022442200224422002246442244686666668EEAAAAEEEGCAACGE',
)
PST = ((),) + tuple(tuple((Q.index(c) - 10) * 5 for c in s) for s in PS)
KD = (31, 33, 14, 18, -14, -18, -31, -33)
GD = (1, -1, 16, -16, 15, 17, -15, -17)
BD = (15, 17, -15, -17)
RD = (1, -1, 16, -16)
KEEP = [15] * 128
KEEP[0] = 13
KEEP[7] = 14
KEEP[4] = 12
KEEP[112] = 7
KEEP[119] = 11
KEEP[116] = 3
R = random.Random(20261116)
Z = [[R.randrange(1 << 64) for _ in range(128)] for _ in range(12)]
ZS = R.randrange(1 << 64)
ZE = [R.randrange(1 << 64) for _ in range(8)]
ZC = [R.randrange(1 << 64) for _ in range(16)]
B = [0] * 128
STM = 0
CR = 0
EP = -1
H = 0
EV = 0
WKS = 4
BKS = 116
U = []
T = {}
KIL = [[0, 0] for _ in range(64)]
SEEN = []
CG = 0
N = 0
def pi(p):
    return (abs(p) - 1) * 2 + (0 if p > 0 else 1)
def pv(p, sq):
    a = abs(p)
    i = ((7 - (sq >> 4)) * 8 + (sq & 7)) if p > 0 else ((sq >> 4) * 8 + (sq & 7))
    v = VAL[a] + PST[a][i]
    return v if p > 0 else -v
def attacked(sq, byw):
    if byw:
        for t in (sq - 15, sq - 17):
            if 0 <= t < 128 and not t & 0x88 and B[t] == 1:
                return True
    else:
        for t in (sq + 15, sq + 17):
            if 0 <= t < 128 and not t & 0x88 and B[t] == -1:
                return True
    for d in KD:
        t = sq + d
        if 0 <= t < 128 and not t & 0x88 and B[t] == (2 if byw else -2):
            return True
    for d in GD:
        t = sq + d
        if 0 <= t < 128 and not t & 0x88 and B[t] == (6 if byw else -6):
            return True
    for d in BD:
        t = sq + d
        while 0 <= t < 128 and not t & 0x88:
            c = B[t]
            if c:
                if c == (3 if byw else -3) or c == (5 if byw else -5):
                    return True
                break
            t += d
    for d in RD:
        t = sq + d
        while 0 <= t < 128 and not t & 0x88:
            c = B[t]
            if c:
                if c == (4 if byw else -4) or c == (5 if byw else -5):
                    return True
                break
            t += d
    return False
def gen(cap=False):
    ms = []
    w = STM == 0
    for s in range(128):
        if s & 0x88:
            continue
        p = B[s]
        if not p or (p > 0) != w:
            continue
        a = abs(p)
        if a == 1:
            d = 16 if w else -16
            t = s + d
            if not cap and B[t] == 0:
                last = (t >> 4) == (7 if w else 0)
                if last:
                    for pr in (5, 2, 4, 3):
                        ms.append(s | t << 7 | pr << 14)
                else:
                    ms.append(s | t << 7)
                    if (s >> 4) == (1 if w else 6) and B[t + d] == 0:
                        ms.append(s | (t + d) << 7 | 1 << 19)
            for dd in (d - 1, d + 1):
                t = s + dd
                if t & 0x88:
                    continue
                c = B[t]
                if (c and (c > 0) != w) or t == EP:
                    ep = 1 << 17 if t == EP and not c else 0
                    if (t >> 4) == (7 if w else 0):
                        for pr in (5, 2, 4, 3):
                            ms.append(s | t << 7 | pr << 14 | ep)
                    else:
                        ms.append(s | t << 7 | ep)
        elif a == 2 or a == 6:
            for dd in KD if a == 2 else GD:
                t = s + dd
                if t & 0x88:
                    continue
                c = B[t]
                if not c:
                    if not cap:
                        ms.append(s | t << 7)
                elif (c > 0) != w:
                    ms.append(s | t << 7)
        else:
            for dd in BD if a == 3 else RD if a == 4 else BD + RD:
                t = s + dd
                while not t & 0x88:
                    c = B[t]
                    if not c:
                        if not cap:
                            ms.append(s | t << 7)
                    else:
                        if (c > 0) != w:
                            ms.append(s | t << 7)
                        break
                    t += dd
    if not cap:
        if w:
            if CR & 1 and B[5] == 0 and B[6] == 0 and B[7] == 4 \
                    and not attacked(4, 0) and not attacked(5, 0) and not attacked(6, 0):
                ms.append(4 | 6 << 7 | 1 << 18)
            if CR & 2 and B[1] == 0 and B[2] == 0 and B[3] == 0 and B[0] == 4 \
                    and not attacked(4, 0) and not attacked(3, 0) and not attacked(2, 0):
                ms.append(4 | 2 << 7 | 1 << 18)
        else:
            if CR & 4 and B[117] == 0 and B[118] == 0 and B[119] == -4 \
                    and not attacked(116, 1) and not attacked(117, 1) and not attacked(118, 1):
                ms.append(116 | 118 << 7 | 1 << 18)
            if CR & 8 and B[113] == 0 and B[114] == 0 and B[115] == 0 and B[112] == -4 \
                    and not attacked(116, 1) and not attacked(115, 1) and not attacked(114, 1):
                ms.append(116 | 114 << 7 | 1 << 18)
    return ms
def make(m):
    global STM, CR, EP, H, EV, WKS, BKS
    f = m & 127
    t = (m >> 7) & 127
    pr = (m >> 14) & 7
    p = B[f]
    ct = (t - 16 if p > 0 else t + 16) if m & 1 << 17 else t
    cap = B[ct]
    U.append((m, cap, ct, CR, EP, H, EV, WKS, BKS))
    if EP >= 0:
        H ^= ZE[EP & 7]
    H ^= ZC[CR]
    H ^= ZS
    H ^= Z[pi(p)][f]
    EV -= pv(p, f)
    B[f] = 0
    if cap:
        H ^= Z[pi(cap)][ct]
        EV -= pv(cap, ct)
        B[ct] = 0
    q = (pr if p > 0 else -pr) if pr else p
    if abs(p) == 6:
        if p > 0:
            WKS = t
        else:
            BKS = t
        if m & 1 << 18:
            rf, rt = (7, 5) if t == 6 else (0, 3) if t == 2 \
                else (119, 117) if t == 118 else (112, 115)
            r = B[rf]
            H ^= Z[pi(r)][rf]
            EV -= pv(r, rf)
            B[rf] = 0
            B[rt] = r
            H ^= Z[pi(r)][rt]
            EV += pv(r, rt)
    B[t] = q
    H ^= Z[pi(q)][t]
    EV += pv(q, t)
    CR &= KEEP[f] & KEEP[t]
    H ^= ZC[CR]
    EP = (f + 16 if p > 0 else f - 16) if m & 1 << 19 else -1
    if EP >= 0:
        H ^= ZE[EP & 7]
    STM ^= 1
def unmake(m):
    global STM, CR, EP, H, EV, WKS, BKS
    _, cap, ct, CR, EP, H, EV, WKS, BKS = U.pop()
    f = m & 127
    t = (m >> 7) & 127
    pr = (m >> 14) & 7
    q = B[t]
    B[t] = 0
    if cap:
        B[ct] = cap
    B[f] = (1 if q > 0 else -1) if pr else q
    if m & 1 << 18:
        rf, rt = (7, 5) if t == 6 else (0, 3) if t == 2 \
            else (119, 117) if t == 118 else (112, 115)
        B[rt] = 0
        B[rf] = 4 if t < 16 else -4
    STM ^= 1
def parse(fen):
    global B, STM, CR, EP, H, EV, WKS, BKS, U, N
    B = [0] * 128
    U = []
    N = 0
    parts = fen.split()
    for r, row in enumerate(parts[0].split('/')):
        sq = (7 - r) * 16
        for ch in row:
            if ch.isdigit():
                sq += int(ch)
            else:
                p = 'PNBRQK'.index(ch.upper()) + 1
                if ch.islower():
                    p = -p
                B[sq] = p
                sq += 1
    STM = 0 if parts[1] == 'w' else 1
    CR = 0
    if len(parts) > 2 and parts[2] != '-':
        for i, ch in enumerate('KQkq'):
            if ch in parts[2]:
                CR |= 1 << i
    EP = -1
    if len(parts) > 3 and parts[3] != '-':
        f = ord(parts[3][0]) - 97
        r = int(parts[3][1]) - 1
        EP = r * 16 + f
    WKS = 4
    BKS = 116
    H = 0
    EV = 0
    for s in range(128):
        if s & 0x88:
            continue
        p = B[s]
        if p:
            H ^= Z[pi(p)][s]
            EV += pv(p, s)
            if p == 6:
                WKS = s
            elif p == -6:
                BKS = s
    if STM:
        H ^= ZS
    H ^= ZC[CR]
    if EP >= 0:
        H ^= ZE[EP & 7]
def om(m, hm, ply):
    f = m & 127
    s = 0
    if m == hm:
        s += 20000
    t = (m >> 7) & 127
    pr = (m >> 14) & 7
    c = B[t]
    if c:
        s = 10000 + VAL[abs(c)] * 10 - VAL[abs(B[f])] // 16
    if pr:
        s += 9000 + VAL[pr]
    if ply < 64:
        if KIL[ply][0] == m:
            s += 5000
        elif KIL[ply][1] == m:
            s += 4000
    return s
class Abort(Exception):
 pass
def search(d, a, b, ply):
    global N, STM, H, EP
    N += 1
    if N > BUDGET:
        raise Abort
    w = STM == 0
    inck = attacked(WKS if w else BKS, not w)
    if inck:
        d += 1
    if d <= 0:
        return qs(a, b, ply)
    a0 = a
    e = T.get(H)
    hm = 0
    if e and e[0] >= d:
        if e[2] == 0:
            return e[1]
        if e[2] == 1 and e[1] >= b:
            return e[1]
        if e[2] == 2 and e[1] <= a:
            return e[1]
        hm = e[3]
    ms = gen()
    ms.sort(key=lambda m: om(m, hm, ply), reverse=True)
    if d >= 3 and not inck and ply > 0 and abs(b) < MATE - 200:
        oe = EP
        EP = -1
        H ^= ZS
        STM ^= 1
        v = -search(d - 3, -b, -b + 1, ply + 1)
        STM ^= 1
        H ^= ZS
        EP = oe
        if v >= b:
            return b
    best = -MATE
    bm = 0
    legal = 0
    i = 0
    for m in ms:
        w2 = STM == 0
        make(m)
        if attacked(WKS if w2 else BKS, not w2):
            unmake(m);continue
        legal += 1
        rd = 0
        if i > 3 and d >= 3 and not inck and not m >> 14 and not B[(m >> 7) & 127]:
            rd = 1 if i < 12 else 2
            if rd >= d - 1:rd = d - 2
        if rd:
            s = -search(d - 1 - rd, -a - 1, -a, ply + 1)
            if s > a:
                s = -search(d - 1, -a - 1, -a, ply + 1)
            if s > a and s < b:
                s = -search(d - 1, -b, -a, ply + 1)
        elif i == 0:
            s = -search(d - 1, -b, -a, ply + 1)
        else:
            s = -search(d - 1, -a - 1, -a, ply + 1)
            if s > a and s < b:
                s = -search(d - 1, -b, -a, ply + 1)
        i += 1
        unmake(m)
        if s > best:
            best = s
            bm = m
        if s > a:
            a = s
        if a >= b:
            if ply < 64 and not B[(m >> 7) & 127] and not (m >> 14) & 7:
                if KIL[ply][0] != m:
                    KIL[ply][1] = KIL[ply][0]
                    KIL[ply][0] = m
            break
    if not legal:
        return -MATE + ply if attacked(WKS if w else BKS, not w) else 0
    fl = 0 if best > a0 and best < b else (1 if best >= b else 2)
    T[H] = (d, best, fl, bm)
    return best
def qs(a, b, ply):
    global N
    N += 1
    if N > BUDGET:
        raise Abort
    w = STM == 0
    if attacked(WKS if w else BKS, not w):
        return search(1, a, b, ply)
    s = EV if w else -EV
    if s >= b:
        return b
    if s > a:
        a = s
    sp = s
    ms = gen(cap=True)
    ms.sort(key=lambda m: om(m, 0, ply), reverse=True)
    for m in ms:
        t = (m >> 7) & 127
        v = 100 if m & 1 << 17 else VAL[abs(B[t])]
        if not (m >> 14) & 7 and sp + v + 200 < a:
            continue
        w2 = STM == 0
        make(m)
        if attacked(WKS if w2 else BKS, not w2):
            unmake(m)
            continue
        s = -qs(-b, -a, ply + 1)
        unmake(m)
        if s > a:
            a = s
        if a >= b:
            return b
    return a
def uci(m):
    f = m & 127
    t = (m >> 7) & 127
    pr = (m >> 14) & 7
    s = 'abcdefgh'[f & 7] + str((f >> 4) + 1) + 'abcdefgh'[t & 7] + str((t >> 4) + 1)
    return s + ('', 'n', 'b', 'r', 'q')[pr - 1] if pr else s
def choose(fen, legal):
    global N
    parse(fen)
    SEEN.append(H)
    if len(T) > 300000:
        T.clear()
    ms = gen()
    u = {uci(m): m for m in ms}
    root = [u[x] for x in legal if x in u]
    if not root:
        root = ms
    if len(root) == 1:
        return [uci(root[0])]
    root.sort(key=lambda m: om(m, 0, 0), reverse=True)
    scores = {}
    try:
        for d in range(1, 64):
            a = -INF
            bm = None
            for m in root:
                w = STM == 0
                make(m)
                if attacked(WKS if w else BKS, not w):
                    unmake(m)
                    scores[m] = -INF
                    continue
                hp = H
                if a == -INF:
                    s = -search(d - 1, -INF, -a, 1)
                else:
                    s = -search(d - 1, -a - 1, -a, 1)
                    if s > a:
                        s = -search(d - 1, -INF, -a, 1)
                unmake(m)
                if s > 0 and SEEN.count(hp) >= 2:
                    s = 0
                scores[m] = s
                if s > a:
                    a = s
                    bm = m
            if bm is None:
                break
            root.sort(key=lambda m: scores.get(m, -INF), reverse=True)
    except Abort:
        pass
    n = N
    parse(fen)
    N = n
    w = STM == 0
    make(root[0])
    if not attacked(WKS if w else BKS, not w):
        SEEN.append(H)
    unmake(root[0])
    return [uci(m) for m in root] + [x for x in legal if x not in u]
URL = os.environ.get('MAKEFUN_ENV_URL', '')
def post(path, body):
    req = urllib.request.Request(URL + path, data=json.dumps(body).encode(),
                                 headers={'content-type': 'application/json'})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            try:
                return json.load(e)
            except Exception:
                return {'error': 'http %d' % e.code}
        except Exception:
            continue
    sys.exit('env unreachable')
def main():
    global CG
    if not URL:
        sys.exit('MAKEFUN_ENV_URL is not set')
    while True:
        g = post('/game', {})
        if g['status'] == 'done':
            break
        if g.get('game') is not None and g['game'] != CG:
            CG = g['game']
            SEEN.clear()
        while g['status'] == 'your_move':
            try:
                cands = choose(g['fen'], g['legal_moves'])
            except Exception:
                cands = g['legal_moves']
            for mv in cands:
                r = post('/move', {'game': g['game'], 'move': mv})
                if 'error' not in r:
                    g = r
                    break
            else:
                g = post('/resign', {'game': g['game']})
        print('game %d: %s by %s' % (g['game'], g.get('outcome'), g.get('reason')),
              file=sys.stderr)
    print('done: %s won, %s drawn, %s lost' % (g.get('wins'), g.get('draws'), g.get('losses')),
          file=sys.stderr)
if __name__ == '__main__':
    main()
