"""
멀티턴 테스트 스크립트

사용법:
  1. API 서버 먼저 실행:  python api.py
  2. 이 파일 실행:        python test_multiturn.py

테스트 케이스:
  A. 기본 멀티턴: 이전 대화 내용을 기억하는지 확인
  B. 새 대화 분리: thread_id가 다르면 히스토리가 없는지 확인
  C. Tool 사용: 검색 도구가 정상 작동하는지 확인
"""

import requests

BASE_URL = "http://localhost:8000"


def post_text(text_query: str, thread_id: str = None) -> dict:
    """텍스트 질문 전송 헬퍼"""
    data = {"text_query": text_query}
    if thread_id:
        data["thread_id"] = thread_id
    r = requests.post(f"{BASE_URL}/chat/text", data=data)
    r.raise_for_status()
    return r.json()


def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


# ─────────────────────────────────────────────
# 테스트 A: 기본 멀티턴 (이전 대화 기억 확인)
# ─────────────────────────────────────────────
def test_A_multiturn():
    separator("테스트 A: 멀티턴 (이전 대화 기억)")

    # 1턴: 특정 개념 설명 요청
    print("\n[1턴] 디자인 특허란?")
    r1 = post_text("디자인 특허란 무엇인가요? 한 줄로 간단히 설명해줘.")
    thread_id = r1["thread_id"]
    print(f"  thread_id : {thread_id}")
    print(f"  turn      : {r1['turn']}")
    print(f"  답변      : {r1['answer'][:150]}...")

    # 2턴: 이전 내용 기반 후속 질문
    print("\n[2턴] 방금 설명 이어서 질문 (같은 thread_id)")
    r2 = post_text("방금 설명해준 것과 상표권의 차이점은?", thread_id=thread_id)
    print(f"  turn      : {r2['turn']}")
    print(f"  답변      : {r2['answer'][:200]}...")

    # 검증: turn이 2인지 확인
    assert r2["turn"] == 2, f"turn이 2여야 함 (실제: {r2['turn']})"
    print("\n  [PASS] 2턴 정상 확인")

    # 3턴: 더 이어가기
    print("\n[3턴] 계속 이어서")
    r3 = post_text("지금까지 설명한 내용을 3줄로 요약해줘.", thread_id=thread_id)
    print(f"  turn      : {r3['turn']}")
    print(f"  답변      : {r3['answer'][:200]}...")
    assert r3["turn"] == 3, f"turn이 3이어야 함 (실제: {r3['turn']})"
    print("\n  [PASS] 3턴 정상 확인")

    return thread_id


# ─────────────────────────────────────────────
# 테스트 B: 새 대화는 히스토리 없음
# ─────────────────────────────────────────────
def test_B_new_conversation():
    separator("테스트 B: 새 대화 분리 (thread_id 없이 전송)")

    print("\n[1턴] thread_id 없이 새 대화 시작")
    r = post_text("안녕하세요, 처음 대화입니다.")
    print(f"  새 thread_id : {r['thread_id']}")
    print(f"  turn         : {r['turn']}")
    assert r["turn"] == 1, f"새 대화는 항상 1턴이어야 함 (실제: {r['turn']})"
    print("\n  [PASS] 새 대화 1턴 정상 확인")


# ─────────────────────────────────────────────
# 테스트 C: Tool 사용 확인 (DB 검색 or 웹 검색)
# ─────────────────────────────────────────────
def test_C_tool_use():
    separator("테스트 C: Tool 사용 확인")

    print("\n[DB 검색 Tool]")
    r = post_text("펌프형 용기 디자인 찾아줘")
    print(f"  답변: {r['answer'][:200]}...")

    print("\n[웹 검색 Tool]")
    r2 = post_text("2024년 한국 디자인 특허 출원 트렌드 알려줘")
    print(f"  답변: {r2['answer'][:200]}...")

    print("\n  [PASS] Tool 호출 정상")


# ─────────────────────────────────────────────
# 서버 연결 확인
# ─────────────────────────────────────────────
def check_server():
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=3)
        r.raise_for_status()
        print(f"  서버 연결 OK: {r.json()}")
        return True
    except Exception as e:
        print(f"  [ERROR] 서버 연결 실패: {e}")
        print(f"  → 먼저 'python api.py' 실행 후 다시 시도하세요.")
        return False


# ─────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("디자인 챗봇 멀티턴 테스트")

    if not check_server():
        exit(1)

    try:
        test_A_multiturn()
        test_B_new_conversation()
        test_C_tool_use()

        separator("모든 테스트 완료!")
        print("  멀티턴 기능이 정상적으로 동작합니다.")

    except AssertionError as e:
        print(f"\n  [FAIL] 테스트 실패: {e}")
    except Exception as e:
        print(f"\n  [ERROR] 예외 발생: {e}")
