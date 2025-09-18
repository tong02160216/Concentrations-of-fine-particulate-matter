
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
FPS = 120

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

    # 第二组数据（演示用：逆序）
    norm_levels2 = list(reversed(norm_levels))
    levels2 = list(reversed(levels))

    # 动画渐变参数
    transition_frames = 8  # 渐变帧数，越大越平滑
    total_frames = transition_frames * 2

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('PM2.5 Total 螺旋动画')
    clock = pygame.time.Clock()

    running = True
    frame = 0
    n_points = len(norm_levels)

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

        # 生成紫到蓝的细腻渐变色，降低纯度（整体更灰、更淡）
        def lerp(a, b, t):
            return int(a + (b - a) * t)
        def desaturate(rgb, factor=0.5):
            # factor=0.5 表示降低到50%纯度
            avg = sum(rgb) // 3
            return tuple(int(avg * factor + c * (1 - factor)) for c in rgb)
        color_start = (75, 0, 130)
        color_end   = (0, 0, 139)
        color_mid0  = (72, 61, 139)
        color_mid1  = (138, 43, 226)
        color_mid2  = (123, 104, 238)
        color_mid3  = (186, 85, 211)
        color_mid4  = (135, 206, 250)
        color_mid5  = (70, 130, 180)
        n_grad = n_points
        colors = []
        for i in range(n_grad):
            t = i / (n_grad - 1)
            if t < 0.125:
                tt = t / 0.125
                rgb = (
                    lerp(color_start[0], color_mid0[0], tt),
                    lerp(color_start[1], color_mid0[1], tt),
                    lerp(color_start[2], color_mid0[2], tt)
                )
            elif t < 0.25:
                tt = (t - 0.125) / 0.125
                rgb = (
                    lerp(color_mid0[0], color_mid1[0], tt),
                    lerp(color_mid0[1], color_mid1[1], tt),
                    lerp(color_mid0[2], color_mid1[2], tt)
                )
            elif t < 0.375:
                tt = (t - 0.25) / 0.125
                rgb = (
                    lerp(color_mid1[0], color_mid2[0], tt),
                    lerp(color_mid1[1], color_mid2[1], tt),
                    lerp(color_mid1[2], color_mid2[2], tt)
                )
            elif t < 0.5:
                tt = (t - 0.375) / 0.125
                rgb = (
                    lerp(color_mid2[0], color_mid3[0], tt),
                    lerp(color_mid2[1], color_mid3[1], tt),
                    lerp(color_mid2[2], color_mid3[2], tt)
                )
            elif t < 0.625:
                tt = (t - 0.5) / 0.125
                rgb = (
                    lerp(color_mid3[0], color_mid4[0], tt),
                    lerp(color_mid3[1], color_mid4[1], tt),
                    lerp(color_mid3[2], color_mid4[2], tt)
                )
            elif t < 0.75:
                tt = (t - 0.625) / 0.125
                rgb = (
                    lerp(color_mid4[0], color_mid5[0], tt),
                    lerp(color_mid4[1], color_mid5[1], tt),
                    lerp(color_mid4[2], color_mid5[2], tt)
                )
            else:
                tt = (t - 0.75) / 0.25
                rgb = (
                    lerp(color_mid5[0], color_end[0], tt),
                    lerp(color_mid5[1], color_end[1], tt),
                    lerp(color_mid5[2], color_end[2], tt)
                )
            colors.append(desaturate(rgb, factor=0.5))
        # 绘制从圆心出发的无数条直线，数据渐变
        # 每条曲线由圆心出发，沿螺旋路径延展
        # 直线绘制，每个数据点从圆心向外发射一条直线
        for i in range(n_points):
            idx = (i + offset) % n_points
            color = colors[i]
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
        # 左上角显示（距离左边20像素，距离顶部20像素）
        screen.blit(country_text, (20, 20))

        pygame.display.flip()
        frame += 1
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
