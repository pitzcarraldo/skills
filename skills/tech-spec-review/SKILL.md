---
name: tech-spec-review
description: Review a tech spec document written in the team's Notion template format (Summary, Background, Goals, Non-Goals, Plan, Measuring Impact, Security/Privacy/Risks, Other Considerations, Milestones, Open Questions). Use when the user asks to "테크 스펙 리뷰", "tech spec 리뷰", "스펙 문서 리뷰", "이 스펙 봐줘", or provides a Notion/Google Docs/Markdown tech spec link or file and asks for feedback, critique, or readiness check before sharing with the team.
---

# Tech Spec Review

팀 Notion 템플릿을 따르는 테크 스펙 문서를 리뷰한다. Lyft "How to Write Awesome Tech Specs"와 뱅크샐러드 "테크 스펙" 블로그의 원칙을 기반으로, 섹션별 체크리스트에 따라 구조적·정성적 피드백을 한국어로 제공한다.

## 템플릿 섹션 (순서 고정)

1. Summary (요약)
2. Background (배경)
3. Goals (목표)
4. Non-Goals (목표가 아닌 것)
5. Plan (계획)
6. Measuring Impact (임팩트 측정)
7. Security, Privacy, Risks (보안·개인정보·리스크)
8. Other Considerations (이 외 고려사항)
9. Milestones (마일스톤)
10. Open Questions (질문들)

## 워크플로우

1. **문서 수집**
   - Notion URL이면 `mcp__claude_ai_Notion__notion-fetch`로 본문을 가져온다.
   - Google Docs면 가능한 MCP 도구를, 로컬 파일이면 Read로 읽는다.
   - 본문이 placeholder(템플릿 설명문)뿐인 "Not started" 상태인지 먼저 식별한다. 비어있으면 리뷰 대신 "아직 템플릿 상태입니다. 작성 후 다시 요청해주세요"라고 알리고 종료한다.

2. **메타 정보 파악**
   - 제목, 작성자(Owner), Status, Last edited time을 기록한다.
   - 테크 스펙의 **목적(purpose)**을 추론한다: stakeholder buy-in용 하이레벨인지, 구현 착수 직전 로우레벨인지. 이에 따라 기대하는 상세 수준이 달라진다.

3. **섹션별 평가**
   - `references/rubric.md`를 읽고 각 섹션을 체크리스트에 따라 평가한다.
   - 각 섹션에 대해 **Pass / Needs work / Missing** 셋 중 하나로 판정한다.
   - 구체적인 근거(해당 문장 인용 또는 누락 사실)를 반드시 포함한다. 추상적 칭찬·비난 금지.

4. **횡단 점검**
   - Goals ↔ Measuring Impact의 1:1 매핑이 있는가
   - Goals ↔ Non-Goals가 상호 보완적으로 스코프를 고정하는가
   - Plan에 등장하는 모든 외부 의존성이 Security/Risks에 언급되는가
   - Milestones가 Plan의 작업 단위와 일치하는가
   - Open Questions이 실제로 답이 필요한 질문인가, 아니면 리뷰어에게 떠넘기는 미정 사항인가

5. **출력**
   - 아래 "리뷰 출력 포맷"을 정확히 따른다.
   - 한국어로 작성한다 (팀 규약: AI 리뷰는 한국어).

## 리뷰 출력 포맷

```markdown
# 테크 스펙 리뷰: <문서 제목>

**대상**: <URL 또는 파일 경로>
**상태**: <Status 값> / 마지막 수정: <Last edited>
**추정 목적**: <buy-in | 구현 직전 | 포스트모템 등>
**총평**: 2~3줄. 가장 중요한 강점 1개 + 가장 크리티컬한 개선점 1~2개.

## 섹션별 평가

### 1. Summary — [Pass | Needs work | Missing]
- **관찰**: <현재 작성된 내용 또는 누락 사실>
- **개선 제안**: <구체적 문장 수준의 제안>

(2~10번 섹션 동일 포맷으로 반복)

## 횡단 이슈
- <Goals-Impact 매핑 문제 등 섹션 간 일관성 이슈>

## 블로커 (머지 전 반드시 해결)
1. <...>
2. <...>

## 선택 개선 (nice-to-have)
1. <...>
```

## 리뷰 원칙

- **증거 기반**: 모든 지적은 문서에서 인용하거나 "해당 내용 없음"이라고 명시. "더 명확하게 써주세요" 같은 공허한 피드백 금지.
- **문장 수준의 개선안**: "이렇게 바꾸면 어떨까요: <대체 문장>" 형태로 제안하면 작성자가 바로 반영할 수 있다.
- **스코프 확장 경계**: 리뷰어가 새 기능·새 스코프를 제안하지 말 것. Non-Goals를 존중한다. 스코프 관련 우려는 "Non-Goals에 명시적으로 추가하는 것을 권장"으로 표현한다.
- **목적 맞춤 깊이**: buy-in 단계의 스펙에 "JSON 스키마가 없다"고 지적하지 말 것. 구현 직전 스펙이면 반대로 로우레벨 디테일 부재가 블로커가 된다.
- **살아있는 문서**: 마지막 수정일이 오래됐거나 마일스톤이 과거 날짜에 멈춰있으면 지적한다.
- **블로커와 nice-to-have 분리**: 머지/착수를 막을 수준의 문제와 단순 개선 제안을 섞지 않는다.

## 상세 체크리스트

섹션별 체크리스트, 안티패턴, 좋은/나쁜 예시는 `references/rubric.md`에 있다. 리뷰 시작 전에 반드시 이 파일을 읽는다.
