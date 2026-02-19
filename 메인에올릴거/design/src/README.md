### LangGraph 기반 멀티모달 Agentic RAG 시스템

본 시스템은 단순 RAG를 넘어, LangGraph StateGraph로 구현된 에이전틱 아키텍처를 채택하였다.
이미지/텍스트 입력을 라우터 노드가 분기하며, 텍스트 경로에서는 LLM이 웹 검색(web_search)과 벡터DB 검색(search_design_db) 도구를 자율적으로 선택·실행하는 Tool-calling Agent 패턴을 적용하였다.
이미지 경로에서는 CLIP 임베딩 기반 벡터 검색(RAG)과 VLM 분석을 결합하고, interrupt 메커니즘을 통한 Human-in-the-Loop 구조로 사용자가 중간 결과를 선택하면 상세 비교 및 FTO 리포트를 생성한다

- RAG 요소: ChromaDB + CLIP 벡터 검색 (검색 후 생성)

- Agent 요소: LLM의 자율적 tool 선택, LangGraph 오케스트레이션, interrupt(Human-in-the-Loop), 조건부 분기

- 최종 명칭: Agentic RAG 또는 LangGraph 기반 멀티모달 에이전트

