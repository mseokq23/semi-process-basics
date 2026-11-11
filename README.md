# semi-process-basics

velog 시리즈 "반도체 공정 기초부터 정리"에 넣은 그림과 그림 코드.

| 폴더 | 내용 |
| --- | --- |
| `img/NN/` | NN편 그림 |
| `figs/NN_*.py` | NN편 그림 코드 |
| `figs/common.py` | 공통 설정 (글꼴, 재료별 색, 그리기 함수) |
| `figs/cmos.py` | CMOS 인버터 단면 (1, 2, 29, 32, 34, 35편에서 같이 씀) |

## 다시 그리기
```bash
pip install -r requirements.txt
cd figs
for f in [0-9]*.py; do python "$f"; done
```
한글 글꼴은 Noto Sans CJK KR을 씀 (없으면 한글이 네모로 나옴).

## 참고
주 참고 자료는 딴딴's 반도체사관학교 (https://sshmyb.tistory.com). 그림은 전부 새로 그림.
