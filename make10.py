import streamlit as st
import itertools

ops = ['+', '-', '*', '/']

def calc(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0:
            return None
        return a / b

# 指定した演算子(op)で連続している項をすべて集める再帰関数
def collect_terms(tree, op):
    # 木がタプルでない、あるいは演算子が違う場合は、これ以上フラットにできない
    if not isinstance(tree, tuple) or tree[0] != op:
        return [get_canonical_form(tree)]
    
    # 演算子が同じなら、左右に分解して再帰的に集める
    return collect_terms(tree[1], op) + collect_terms(tree[2], op)

def get_canonical_form(tree):
    if not isinstance(tree, tuple):
        return str(tree)
    
    op, left, right = tree
    
    # + と * は結合法則・交換法則が成り立つため、
    # 連続している演算をすべてバラしてリスト化（フラット化）し、ソートする
    if op in ('+', '*'):
        terms = collect_terms(tree, op)
        terms.sort()
        # リストを演算子で結合する
        return f"({f'{op}'.join(terms)})"
    else:
        # - と / は結合法則がないため、そのまま再帰的に処理
        return f"({get_canonical_form(left)}{op}{get_canonical_form(right)})"

def get_all_expressions(nums):
    if len(nums) == 1:
        yield nums[0], nums[0]
        return

    for i in range(1, len(nums)):
        left_part = nums[:i]
        right_part = nums[i:]
        
        for l_val, l_tree in get_all_expressions(left_part):
            for r_val, r_tree in get_all_expressions(right_part):
                for op in ['+', '-', '*', '/']:
                    res = calc(l_val, r_val, op)
                    if res is not None:
                        yield res, (op, l_tree, r_tree)

def make10(nums):
    results = set()
    for perm in itertools.permutations(nums):
        for val, tree in get_all_expressions(perm):
            if abs(val - 10) < 1e-6:
                results.add(get_canonical_form(tree))
    return sorted(list(results))

# --- UI ---
st.title("Make 10 🎯")

nums_input = st.text_input("4桁の数字を入力してください（例: 1234）")

if st.button("計算する"):
    # 4文字で、かつすべて数字であるかチェック
    if len(nums_input) == 4 and nums_input.isdigit():
        # 1文字ずつ取り出して整数リストに変換
        nums = [int(d) for d in nums_input]
        
        # あとはここで計算処理を呼び出す
        results = make10(nums)
        
        if results:
            st.success("作れた！")
            for r in set(results):
                st.write(r)
        else:
            st.warning("10は作れません…")
                
    else:
        st.error("入力形式がおかしいかも")
