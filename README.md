# Planning Optimization

## Data
- Sample
```
{"N": 10, "m": 10, "M": 15, "d": [2, 2, 2, 1, 4, 4, 3, 1, 5, 1], "s": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], "e": [1, 1, 1, 0, 1, 1, 1, 1, 1, 1]}
```

### Data version 1

### Data version 2 (Use to evaluate)

- **Chỉ số**
    - r: max total time between start time and end time to harvest
    - K1: lower bound of number of field to harvest in a day
    - K2: upper bound of number of field to harvest in a day
    - low: list of lower bound of total yield in a day
    - high: list of upper bound of total yield in a day
    - N: number of fields

```
r = [5, 5, 5, 10, 10]
K1 = [4, 2, 10, 4, 2]
K2 = [6, 3, 10, 6, 3]
```

- **Large**

```
low = [20, 30, 40, 50, 60]
high = [30, 50, 75, 100, 125]
N = [100, 250, 500, 750, 1000]
```

- **Small**

```
low = [10, 20, 30, 40, 50]
high = [15, 30, 50, 75, 100]
N = [10, 20, 30, 40, 50]
```

### Data version 3

## Results
- Have solution
```
{"Time": 0.005537986755371094, "Result": 1.0, "Solution": [0, 1, 1, 0, 1, 0, 0, 0, 1, 0]}
```
- Have no solution
```
{"Time": 0.014167070388793945, "Result": "No Solution"}
```
## Tabu Search

- **Quy trình thuật toán**

- **Chi tiết thuật toán**

- **Đánh giá:**

## Genetic Algorithm

- **Quy trình thuật toán**
    - Khởi tạo quần thể
    - Lai ghép, đột biến sinh ra thế hệ sau
    - Loại bỏ các cá thể yếu kém trong thế hệ cũ
- **Chi tiết thuật toán**
    - Khởi tạo quần thể: Hàm initialSolution() để sinh ra một cá thể ngẫu nhiên trong quần thể. Số lượng quần thể là 150 cá thể
    - Lai ghép và đột biến tạo thế hệ mới
        - 90%: Lai ghép
            - 90%: Sử dụng lai ghép 2 điểm cắt, chọn parent theo prob của cost, sử dụng phương pháp roulette_wheel_selection()
            - 10%: Giữ lại cá thể tốt nhất của thế hệ cũ
        - 10%: Đột biến
            - Đột biến một điểm trên gen cá thể, thay thế cho cá thể yếu kém trong cá thể cũ
- **Đánh giá:**
    - Kết quả nghiệm hợp lệ và tối ưu
    - Thang đô RPD
    - Tốc độ hội tụ so với Tabu Search trên các bộ
    - Tốc độ hội tụ theo số lượng cá thể: 50, 150, 300 trên bộ Type1Small
