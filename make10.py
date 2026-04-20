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

def make10(nums):
    results = []
    
    for perm in itertools.permutations(nums):
        for op1, op2, op3 in itertools.product(ops, repeat=3):
            a, b, c, d = perm
            
            # ((a op b) op c) op d
            r1 = calc(a, b, op1)
            if r1 is not None:
                r2 = calc(r1, c, op2)
                if r2 is not None:
                    r3 = calc(r2, d, op3)
                    if r3 is not None and abs(r3 - 10) < 1e-6:
                        results.append(f"(({a}{op1}{b}){op2}{c}){op3}{d}")
    
    return results

# --- UI ---
st.title("Make 10 🎯")

nums_input = st.text_input("4つの数字をスペース区切りで入力（例: 1 3 4 6）")

if st.button("計算する"):
    try:
        nums = list(map(int, nums_input.split()))
        
        if len(nums) != 4:
            st.error("4つ入力してね！")
        else:
            results = make10(nums)
            
            if results:
                st.success("作れた！")
                for r in set(results):
                    st.write(r)
            else:
                st.warning("10は作れません…")
                
    except:
        st.error("入力形式がおかしいかも")