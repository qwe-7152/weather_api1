"""weather.csv의 시간별 습도와 풍속을 그래프로 저장하고 화면에 표시한다."""

import csv
import math
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "weather.csv"
IMAGE_PATH = BASE_DIR / "humidity_wind.png"


def _read_weather_csv() -> list[tuple[datetime, float, float]]:
    """CSV를 읽어 datetime, 습도, 풍속을 시간 자료형과 수치로 변환한다."""
    records: list[tuple[datetime, float, float]] = []
    with CSV_PATH.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required_columns = {"datetime", "humidity_pct", "wind_speed_ms"}
        if reader.fieldnames is None or required_columns - set(reader.fieldnames):
            raise ValueError("weather.csv에 datetime, humidity_pct 또는 wind_speed_ms 열이 없습니다.")

        for line_number, row in enumerate(reader, start=2):
            try:
                timestamp_value = row["datetime"]
                humidity_value = row["humidity_pct"]
                wind_value = row["wind_speed_ms"]
                if timestamp_value is None or humidity_value is None or wind_value is None:
                    raise ValueError("필수 값이 비어 있습니다.")
                timestamp = datetime.fromisoformat(timestamp_value.strip())
                humidity = float(humidity_value.strip()) if humidity_value.strip() else math.nan
                wind_speed = float(wind_value.strip()) if wind_value.strip() else math.nan
            except (TypeError, ValueError) as error:
                raise ValueError(f"{line_number}번째 행을 변환할 수 없습니다.") from error
            records.append((timestamp, humidity, wind_speed))
    return records


def _make_hourly_series(
    records: list[tuple[datetime, float, float]],
) -> tuple[list[datetime], list[float], list[float], list[datetime]]:
    """자료를 시간순으로 정렬하고 누락 시각을 NaN으로 채운다."""
    if not records:
        raise ValueError("weather.csv에 그래프로 그릴 자료가 없습니다.")

    records.sort(key=lambda record: record[0])
    if len({timestamp for timestamp, _, _ in records}) != len(records):
        raise ValueError("weather.csv에 중복 datetime이 있습니다.")

    values = {timestamp: (humidity, wind_speed) for timestamp, humidity, wind_speed in records}
    start = records[0][0]
    end = records[-1][0]
    timestamps: list[datetime] = []
    humidities: list[float] = []
    wind_speeds: list[float] = []
    missing_timestamps: list[datetime] = []
    current = start
    while current <= end:
        timestamps.append(current)
        humidity, wind_speed = values.get(current, (math.nan, math.nan))
        humidities.append(humidity)
        wind_speeds.append(wind_speed)
        if current not in values:
            missing_timestamps.append(current)
        current += timedelta(hours=1)
    return timestamps, humidities, wind_speeds, missing_timestamps


def _plot_weather(
    timestamps: list[datetime],
    humidities: list[float],
    wind_speeds: list[float],
) -> None:
    """시간별 습도와 풍속을 그려 PNG로 저장하고 화면에 표시한다."""
    figure, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    axes[0].plot(timestamps, humidities, color="tab:blue", marker="o", linewidth=1.5)
    axes[0].set_title("Humidity over time")
    axes[0].set_ylabel("Humidity (%)")
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(timestamps, wind_speeds, color="tab:green", marker="o", linewidth=1.5)
    axes[1].set_title("Wind speed over time")
    axes[1].set_xlabel("Time (KST)")
    axes[1].set_ylabel("Wind speed (m/s)")
    axes[1].grid(True, alpha=0.3)
    figure.autofmt_xdate()
    figure.tight_layout()
    figure.savefig(IMAGE_PATH, dpi=150)
    print(f"그래프 저장 위치: {IMAGE_PATH}")
    plt.show()


def main() -> None:
    records = _read_weather_csv()
    timestamps, humidities, wind_speeds, missing_timestamps = _make_hourly_series(records)
    print(f"누락 시각 수: {len(missing_timestamps)}")
    if missing_timestamps:
        print(
            "누락 시각: "
            + ", ".join(timestamp.isoformat(sep=" ") for timestamp in missing_timestamps)
        )
    _plot_weather(timestamps, humidities, wind_speeds)


if __name__ == "__main__":
    main()
