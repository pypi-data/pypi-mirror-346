class DetectionResult:
    def __init__(self, has_repetition, substring='', repetition_count=0, sequence_length=0, start_pos=-1):
        self.has_repetition = has_repetition
        self.substring = substring
        self.repetition_count = repetition_count
        self.sequence_length = sequence_length
        self.start_pos = start_pos

RepetitionResult = DetectionResult

class StringRepetitionDetector:
    def __init__(self, min_length, min_repeats):
        self.min_length = min_length
        self.min_repeats = min_repeats

    def detect(self, s: str) -> DetectionResult:
        n = len(s)
        if n < self.min_length:
            return DetectionResult(False)
    
        # 定义后缀自动机状态
        class State:
            __slots__ = ('next', 'link', 'len', 'occ', 'max_pos')
            def __init__(self):
                self.next = {}
                self.link = -1
                self.len = 0
                self.occ = 0
                self.max_pos = -1
    
        # 构建自动机
        st = [State()]
        last = 0
        for i, c in enumerate(s):
            cur = len(st)
            st.append(State())
            st[cur].len = st[last].len + 1
            st[cur].occ = 1
            st[cur].max_pos = i
            p = last
            while p >= 0 and c not in st[p].next:
                st[p].next[c] = cur
                p = st[p].link
            if p == -1:
                st[cur].link = 0
            else:
                q = st[p].next[c]
                if st[p].len + 1 == st[q].len:
                    st[cur].link = q
                else:
                    clone = len(st)
                    st.append(State())
                    st[clone].len = st[p].len + 1
                    st[clone].next = st[q].next.copy()
                    st[clone].link = st[q].link
                    st[clone].occ = 0
                    st[clone].max_pos = st[q].max_pos
                    while p >= 0 and st[p].next[c] == q:
                        st[p].next[c] = clone
                        p = st[p].link
                    st[q].link = st[cur].link = clone
            last = cur
    
        # 线性时间拓扑排序（按状态长度降序）
        max_len = max(state.len for state in st)
        bucket = [0] * (max_len + 1)
        for state in st:
            bucket[state.len] += 1
        # 前缀和计算位置
        for i in range(1, len(bucket)):
            bucket[i] += bucket[i - 1]
        order = [0] * len(st)
        # 按长度从小到大填充order
        for idx in range(len(st) - 1, -1, -1):
            l = st[idx].len
            bucket[l] -= 1
            order[bucket[l]] = idx
        # 现在order是按长度升序，反转为降序
        order.reverse()

        # 累加出现次数
        for v in order:
            link = st[v].link
            if link >= 0:
                st[link].occ += st[v].occ
    
        # 遍历状态，寻找最佳重复子串
        best = None  # (occ, length, start, state_index)
        for i in range(1, len(st)):
            low = st[st[i].link].len + 1
            L = max(low, self.min_length)
            if L <= st[i].len and st[i].occ >= self.min_repeats:
                start = st[i].max_pos - L + 1
                cand = (st[i].occ, L, start, i)
                if (best is None or
                    cand[0] > best[0] or
                    (cand[0] == best[0] and cand[1] < best[1]) or
                    (cand[0] == best[0] and cand[1] == best[1] and cand[2] < best[2])):
                    best = cand
    
        if best is None:
            return DetectionResult(False)
    
        occ, length, start, idx = best
        substr = s[start:start + length]
        return DetectionResult(True, substr, occ, length, start)
