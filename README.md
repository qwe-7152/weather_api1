# Weather API 수집 및 시각화

기상청 API에서 서울 관측소(지점 `108`)의 시간별 지상관측자료를 수집하고, 습도와 풍속을 그래프로 표시하는 Python 프로젝트입니다.

## 기능

- 기상청 `kma_sfctm3.php` API 호출
- 실행 중 터미널에서 API 인증키 입력
- 2025-09-24 00:00부터 2025-09-30 23:00까지의 자료 조회
- API 응답의 헤더를 확인하여 `TM`, `WS`, `TA`, `HM` 열 파싱
- 시간순 정렬 및 중복 시각 확인
- 결측값을 빈 값으로 유지한 CSV 저장
- 원본 API 응답 보관
- 1시간 간격의 누락 시각을 확인한 습도·풍속 그래프 생성

## 요구 사항

- Python 3.10 이상 권장
- `requests`
- `matplotlib`

설치:

```powershell
python -m pip install requests matplotlib
```

## 사용 방법

### 1. 관측자료 수집

```powershell
python collect_weather.py
```

실행 후 기상청 API 인증키를 입력합니다. 인증키는 화면에 표시되지 않습니다.

수집이 완료되면 다음 파일이 생성됩니다.

- `weather.csv`: 변환된 관측자료
- `weather_raw.txt`: API 원본 응답

`weather.csv`의 열은 다음 순서입니다.

```text
datetime,temperature_C,humidity_pct,wind_speed_ms
```

### 2. 습도·풍속 그래프 생성

```powershell
python plot_weather.py
```

`weather.csv`를 다시 API에 요청하지 않고 읽어 시간순으로 정렬합니다. 누락된 시각은 1시간 간격으로 추가하며, 해당 시각의 값은 결측으로 두어 그래프 선이 이어지지 않게 합니다.

그래프는 다음 파일로 저장되고 실행 중 화면에도 표시됩니다.

- `humidity_wind.png`

## API

공식 API 문서:

<https://apihub.kma.go.kr/api/typ01/url/kma_sfctm3.php>

인증키는 코드나 파일에 저장하지 말고 실행 시 직접 입력하세요.

## 주요 함수

### `collect_weather.py`

- `_decode_response`: 응답 charset에 맞춰 본문을 디코딩합니다.
- `_split_response`: `#` 설명줄과 자료행을 분리합니다.
- `_find_column_positions`: 헤더에서 `TM(1)`, `WS(4)`, `TA(12)`, `HM(14)` 위치를 검증합니다.
- `_parse_rows`: 공백으로 분리한 자료행을 CSV용 표 구조로 변환합니다.
- `_save_csv`: UTF-8-SIG 인코딩으로 `weather.csv`를 저장합니다.

### `plot_weather.py`

- `_read_weather_csv`: CSV의 시각·습도·풍속을 Python 자료형으로 변환합니다.
- `_make_hourly_series`: 시간순 정렬, 누락 시각 생성, 결측값 처리를 수행합니다.
- `_plot_weather`: 습도·풍속 그래프를 저장하고 화면에 표시합니다.

## 주의 사항

- API 인증키를 공개 저장소에 올리지 마세요.
- `weather.csv`가 먼저 생성되어 있어야 그래프를 그릴 수 있습니다.
- 그래프 창을 닫으면 `plot_weather.py`가 종료됩니다.
