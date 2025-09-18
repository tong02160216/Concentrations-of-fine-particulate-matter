# 新数据源：读取 data.csv
import pandas as pd

def extract_total_pm25_from_csv(csv_path):
    df = pd.read_csv(
        csv_path,
        encoding='utf-8',
    usecols=['Location', 'FactValueNumericLow'],
    dtype={'Location': str, 'FactValueNumericLow': float},
        engine='c',
    nrows=300
    )
    data = []
    for idx, row in df.iterrows():
        country = str(row.get('Location', '')).strip()
        value = row.get('FactValueNumericLow', None)
        try:
            value = float(value)
            if country and not pd.isna(value):
                data.append((country, value))
        except:
            pass
    return data


import pygame
import math
import sys

WIDTH, HEIGHT = 900, 900
BG_COLOR = (10, 10, 30)
SPIRAL_COLOR = (0, 200, 255)
FPS = 30

def normalize(data):
    min_v, max_v = min(data), max(data)
    return [(v - min_v) / (max_v - min_v) if max_v > min_v else 0.5 for v in data]

def main():
    pm25_data = extract_total_pm25_from_csv('f:/code/PM2.5/data.csv')
    if not pm25_data:
        print('未提取到数据，无法可视化。')
        sys.exit(1)
    countries = [c for c, v in pm25_data]
    levels = [v for c, v in pm25_data]
    norm_levels = normalize(levels)

    # 插值和插入逻辑，修正缩进
    dense_levels = []
    dense_countries = []
    dense_values = []
    interp_num = 1  # 每两个点之间只插入1个点，减少线条密度
    n = len(norm_levels)
    for i in range(n):
        next_i = (i + 1) % n
        dense_levels.append(norm_levels[i])
        dense_countries.append(countries[i])
        dense_values.append(levels[i])
        for k in range(1, interp_num + 1):
            interp = norm_levels[i] + (norm_levels[next_i] - norm_levels[i]) * k / (interp_num + 1)
            interp_value = levels[i] + (levels[next_i] - levels[i]) * k / (interp_num + 1)
            dense_levels.append(interp)
            dense_countries.append(f'{countries[i]}-{countries[next_i]}')
            dense_values.append(interp_value)

    # 插值后插入倒序前50条数据到200位置
    dense_len = len(dense_levels)
    insert_start = min(200, dense_len)
    first_50_countries = dense_countries[:50][::-1]
    first_50_levels = dense_values[:50][::-1]
    first_50_norm = dense_levels[:50][::-1]
    dense_countries = dense_countries[:insert_start] + first_50_countries + dense_countries[insert_start:]
    dense_values = dense_values[:insert_start] + first_50_levels + dense_values[insert_start:]
    dense_levels = dense_levels[:insert_start] + first_50_norm + dense_levels[insert_start:]

    norm_levels = dense_levels
    countries = dense_countries
    levels = dense_values
    # 多点线性插值，提升线条密度（每两个点之间插入3个点，密度提升为4倍）
    dense_levels = []
    dense_countries = []
    dense_values = []
    interp_num = 1  # 每两个点之间只插入1个点，减少线条密度
    n = len(norm_levels)
    for i in range(n):
        next_i = (i + 1) % n
        dense_levels.append(norm_levels[i])
        dense_countries.append(countries[i])
        dense_values.append(levels[i])
        for k in range(1, interp_num + 1):
            interp = norm_levels[i] + (norm_levels[next_i] - norm_levels[i]) * k / (interp_num + 1)
            interp_value = levels[i] + (levels[next_i] - levels[i]) * k / (interp_num + 1)
            dense_levels.append(interp)
            dense_countries.append(f'{countries[i]}-{countries[next_i]}')
            dense_values.append(interp_value)
    norm_levels = dense_levels
    countries = dense_countries
    levels = dense_values

    # 增加前50条数据并倒序插入到第201-250位置
    insert_start = 200
    insert_end = 250
    first_50_countries = countries[:50][::-1]
    first_50_levels = levels[:50][::-1]
    first_50_norm = norm_levels[:50][::-1]
    countries = countries[:insert_start] + first_50_countries + countries[insert_start:]
    levels = levels[:insert_start] + first_50_levels + levels[insert_start:]
    norm_levels = norm_levels[:insert_start] + first_50_norm + norm_levels[insert_start:]

    # 第二组数据（演示用：逆序）
    norm_levels2 = list(reversed(norm_levels))
    levels2 = list(reversed(levels))

    # 颜色变量定义提前
    color_start = (75, 0, 130)
    color_midA  = (90, 0, 160)   # 深紫到蓝的过渡色
    color_midB  = (60, 0, 180)   # 深紫到蓝的过渡色
    color_end   = (0, 0, 139)
    color_mid0  = (72, 61, 139)
    color_mid1  = (138, 43, 226)
    color_mid2  = (123, 104, 238)
    color_mid3  = (186, 85, 211)
    color_mid4  = (135, 206, 250)
    color_mid5  = (70, 130, 180)

    n_points = len(norm_levels)
    def lerp(a, b, t):
        return int(a + (b - a) * t)
    def desaturate(rgb, factor=0.5):
        avg = sum(rgb) // 3
        return tuple(int(avg * factor + c * (1 - factor)) for c in rgb)
    colors = []
    for i in range(n_points):
        t = i / (n_points - 1)
        if t < 0.08:
            tt = t / 0.08
            rgb = (
                lerp(color_start[0], color_midA[0], tt),
                lerp(color_start[1], color_midA[1], tt),
                lerp(color_start[2], color_midA[2], tt)
            )
        elif t < 0.16:
            tt = (t - 0.08) / 0.08
            rgb = (
                lerp(color_midA[0], color_midB[0], tt),
                lerp(color_midA[1], color_midB[1], tt),
                lerp(color_midA[2], color_midB[2], tt)
            )
        elif t < 0.24:
            tt = (t - 0.16) / 0.08
            rgb = (
                lerp(color_midB[0], color_end[0], tt),
                lerp(color_midB[1], color_end[1], tt),
                lerp(color_midB[2], color_end[2], tt)
            )
        elif t < 0.32:
            tt = (t - 0.24) / 0.08
            rgb = (
                lerp(color_end[0], color_mid0[0], tt),
                lerp(color_end[1], color_mid0[1], tt),
                lerp(color_end[2], color_mid0[2], tt)
            )
        elif t < 0.44:
            tt = (t - 0.32) / 0.12
            rgb = (
                lerp(color_mid0[0], color_mid1[0], tt),
                lerp(color_mid0[1], color_mid1[1], tt),
                lerp(color_mid0[2], color_mid1[2], tt)
            )
        elif t < 0.56:
            tt = (t - 0.44) / 0.12
            rgb = (
                lerp(color_mid1[0], color_mid2[0], tt),
                lerp(color_mid1[1], color_mid2[1], tt),
                lerp(color_mid1[2], color_mid2[2], tt)
            )
        elif t < 0.68:
            tt = (t - 0.56) / 0.12
            rgb = (
                lerp(color_mid2[0], color_mid3[0], tt),
                lerp(color_mid2[1], color_mid3[1], tt),
                lerp(color_mid2[2], color_mid3[2], tt)
            )
        elif t < 0.80:
            tt = (t - 0.68) / 0.12
            rgb = (
                lerp(color_mid3[0], color_mid4[0], tt),
                lerp(color_mid3[1], color_mid4[1], tt),
                lerp(color_mid3[2], color_mid4[2], tt)
            )
        elif t < 0.92:
            tt = (t - 0.80) / 0.12
            rgb = (
                lerp(color_mid4[0], color_mid5[0], tt),
                lerp(color_mid4[1], color_mid5[1], tt),
                lerp(color_mid4[2], color_mid5[2], tt)
            )
        else:
            tt = (t - 0.92) / 0.08
            rgb = (
                lerp(color_mid5[0], color_end[0], tt),
                lerp(color_mid5[1], color_end[1], tt),
                lerp(color_mid5[2], color_end[2], tt)
            )
        colors.append(desaturate(rgb, factor=0.5))

    # 动画渐变参数
    transition_frames = 8  # 渐变帧数，越大越平滑
    total_frames = transition_frames * 2

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('PM2.5 Total 螺旋动画')
    clock = pygame.time.Clock()

    running = True
    frame = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        spiral_center = (WIDTH // 2, HEIGHT // 2)
        base_radius = 0
        max_radius = min(WIDTH, HEIGHT) // 2 - 40
        angle_step = 2 * math.pi / n_points
        offset = (frame % n_points)

        # 动态渐变权重
        phase = (frame % total_frames)
        if phase < transition_frames:
            alpha = phase / transition_frames
        else:
            alpha = 1 - (phase - transition_frames) / transition_frames

        # 绘制从圆心出发的无数条直线，数据渐变
        for i in range(n_points):
            idx = (i + offset) % n_points
            color = colors[idx]
            angle = i * angle_step + frame * 0.03
            radius1 = base_radius + norm_levels[idx] * (max_radius - base_radius)
            radius2 = base_radius + norm_levels2[idx] * (max_radius - base_radius)
            radius = (1 - alpha) * radius1 + alpha * radius2
            start_pos = spiral_center
            end_pos = (spiral_center[0] + radius * math.cos(angle), spiral_center[1] + radius * math.sin(angle))
            pygame.draw.aaline(screen, color, start_pos, end_pos)

        # 显示当前国家名和数值（渐变）
        cur_idx = offset
        value1 = levels[cur_idx]
        value2 = levels2[cur_idx]
        show_value = (1 - alpha) * value1 + alpha * value2
        show_country = countries[cur_idx]
        font = pygame.font.SysFont(None, 36)
        country_text = font.render(f'{show_country}: {show_value:.2f}', True, (255, 255, 255))
        screen.blit(country_text, (20, 20))

        pygame.display.flip()
        frame += 1
        clock.tick(FPS)

pygame.quit()

# 确保调试信息在颜色生成逻辑的最后一行内

if __name__ == '__main__':
    main()
