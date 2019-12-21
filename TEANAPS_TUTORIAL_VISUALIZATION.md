# TEANAPS Tutorial: Visualization

---
## Install
- `install.ipynb` 파일을 참조해주세요.
- 링크를 통해 설치용 `Jupyter Notebook` 파일을 `Google Colabotory`로 열 수 있습니다. [(Link)](https://colab.research.google.com/github/fingeredman/teanaps/blob/master/install.ipynb)
- 로컬 환경에 철치가 필요하신 경우, [teanaps_install.py](https://github.com/fingeredman/teanaps/blob/master/teanaps_setup.py) 파일을 참고 바랍니다.
- 본 패키지는 `pip`를 통한 설치를 지원하지 않습니다.
- `Windows 운영체제`에서 일부 기능에 제한이 있을 수 있습니다.

Python Code:
```python
!git clone https://github.com/fingeredman/teanaps.git
!python "teanaps/teanaps_setup.py"
```

---
## Tutorial

### 시각화 (Visualization)
#### 1. 히스토그램 & 라인그래프 (Histogram & Line-graph)
> 히스토그램 또는 라인그래프 생성을 위한 기본코드는 아래와 같습니다.  

Python Code:
```python
from teanaps.visualization import GraphVisualizer

gv = GraphVisualizer()
```
Output:

---
## Update History
> 2019.12.22. 초안입력  
