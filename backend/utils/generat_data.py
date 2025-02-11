import csv
import random
from datetime import datetime, timedelta


def generate_sensor_data():
    # 生成传感器参数代码
    sensor_codes = [f"Z{str(random.randint(1, 9999)).zfill(4)}" for _ in range(20)]
    data = [["Time"] + sensor_codes]
    start_time = datetime.now()
    for i in range(3600):
        current_time = start_time + timedelta(seconds=i)
        row = [current_time.strftime("%Y-%m-%d %H:%M:%S")]
        for _ in range(20):
            # 随机生成不同类型的数据
            param_type = random.randint(1, 3)
            if param_type == 1:
                # 温度，范围在 20 到 30 度之间
                value = round(random.uniform(20, 30), 2)
            elif param_type == 2:
                # 电压，范围在 2 到 5 伏之间
                value = round(random.uniform(2, 5), 2)
            else:
                # 电流，范围在 0.5 到 2 安培之间
                value = round(random.uniform(0.5, 2), 2)
            row.append(value)
        data.append(row)
    return data


def save_to_csv(data, filename="sensor_data.csv"):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


if __name__ == "__main__":
    sensor_data = generate_sensor_data()
    save_to_csv(sensor_data)