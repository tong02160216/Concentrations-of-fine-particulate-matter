
import pandas as pd
import pygame
import math
import sys
import heapq
import random

WIDTH, HEIGHT = 900, 900
BG_COLOR = (255, 255, 255)
FPS = 30

def extract_total_pm25_from_csv(csv_path):
    df = pd.read_csv(
        csv_path,
        encoding='utf-8',
        usecols=['Location', 'FactValueNumericLow'],
        dtype={'Location': str, 'FactValueNumericLow': float},
        engine='c',
        nrows=300
    )
    df = df.dropna(subset=['Location', 'FactValueNumericLow'])
    df['Location'] = df['Location'].str.strip()
    data = list(zip(df['Location'], df['FactValueNumericLow']))
    return data

def normalize(data):
    min_v, max_v = min(data), max(data)
    return [(v - min_v) / (max_v - min_v) if max_v > min_v else 0.5 for v in data]


def main():
    # 颜色变量和插值函数提前定义
    color_start = (75, 0, 130)
    color_midA  = (90, 0, 160)
    color_midB  = (60, 0, 180)
    color_end   = (0, 0, 139)
    color_mid0  = (72, 61, 139)
    color_mid1  = (138, 43, 226)
    color_mid2  = (123, 104, 238)
    color_mid3  = (186, 85, 211)
    color_mid4  = (135, 206, 250)
    color_mid5  = (70, 130, 180)
    def lerp(a, b, t):
        return int(a + (b - a) * t)
    def desaturate(rgb, factor=0.5):
        avg = sum(rgb) // 3
        return tuple(int(avg * factor + c * (1 - factor)) for c in rgb)

    pm25_data = extract_total_pm25_from_csv('f:/code/PM2.5/data.csv')
    if not pm25_data:
        print('未提取到数据，无法可视化。')
        sys.exit(1)
    countries = [c for c, v in pm25_data]
    levels = [v for c, v in pm25_data]
    # 找到最大10条数据的索引，并将其缩小为原来的三分之二
    if len(levels) >= 10:
        largest_indices = heapq.nlargest(10, range(len(levels)), key=lambda i: levels[i])
        for idx in largest_indices:
            levels[idx] = levels[idx] * (2/3)
    norm_levels = normalize(levels)

    # 插值一轮
    dense_levels = []
    dense_countries = []
    dense_values = []
    interp_num = 1
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
    first_50_countries = countries[:50][::-1]
    first_50_levels = levels[:50][::-1]
    first_50_norm = norm_levels[:50][::-1]
    countries = countries[:insert_start] + first_50_countries + countries[insert_start:]
    levels = levels[:insert_start] + first_50_levels + levels[insert_start:]
    norm_levels = norm_levels[:insert_start] + first_50_norm + norm_levels[insert_start:]

    n_points = len(norm_levels)
    norm_levels2 = list(reversed(norm_levels))
    levels2 = list(reversed(levels))

    # 生成颜色渐变
    grad_colors = []
    for i in range(n_points):
        t = i / (n_points - 1)
        if t < 0.08:
            tt = t / 0.08
            rgb = (lerp(color_start[0], color_midA[0], tt), lerp(color_start[1], color_midA[1], tt), lerp(color_start[2], color_midA[2], tt))
        elif t < 0.16:
            tt = (t - 0.08) / 0.08
            rgb = (lerp(color_midA[0], color_midB[0], tt), lerp(color_midA[1], color_midB[1], tt), lerp(color_midA[2], color_midB[2], tt))
        elif t < 0.24:
            tt = (t - 0.16) / 0.08
            rgb = (lerp(color_midB[0], color_end[0], tt), lerp(color_midB[1], color_end[1], tt), lerp(color_midB[2], color_end[2], tt))
        elif t < 0.32:
            tt = (t - 0.24) / 0.08
            rgb = (lerp(color_end[0], color_mid0[0], tt), lerp(color_end[1], color_mid0[1], tt), lerp(color_end[2], color_mid0[2], tt))
        elif t < 0.44:
            tt = (t - 0.32) / 0.12
            rgb = (lerp(color_mid0[0], color_mid1[0], tt), lerp(color_mid0[1], color_mid1[1], tt), lerp(color_mid0[2], color_mid1[2], tt))
        elif t < 0.56:
            tt = (t - 0.44) / 0.12
            rgb = (lerp(color_mid1[0], color_mid2[0], tt), lerp(color_mid1[1], color_mid2[1], tt), lerp(color_mid1[2], color_mid2[2], tt))
        elif t < 0.68:
            tt = (t - 0.56) / 0.12
            rgb = (lerp(color_mid2[0], color_mid3[0], tt), lerp(color_mid2[1], color_mid3[1], tt), lerp(color_mid2[2], color_mid3[2], tt))
        elif t < 0.80:
            tt = (t - 0.68) / 0.12
            rgb = (lerp(color_mid3[0], color_mid4[0], tt), lerp(color_mid3[1], color_mid4[1], tt), lerp(color_mid3[2], color_mid4[2], tt))
        elif t < 0.92:
            tt = (t - 0.80) / 0.12
            rgb = (lerp(color_mid4[0], color_mid5[0], tt), lerp(color_mid4[1], color_mid5[1], tt), lerp(color_mid4[2], color_mid5[2], tt))
        else:
            tt = (t - 0.92) / 0.08
            rgb = (lerp(color_mid5[0], color_end[0], tt), lerp(color_mid5[1], color_end[1], tt), lerp(color_mid5[2], color_end[2], tt))
        grad_colors.append(desaturate(rgb, factor=0.5))
    colors = grad_colors.copy()
    random.shuffle(colors)

    # 动画参数和主循环
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('PM2.5 Total 螺旋动画')
    clock = pygame.time.Clock()
    spiral_center = (WIDTH // 2, HEIGHT // 2)
    base_radius = 0
    max_radius = min(WIDTH, HEIGHT) // 2 - 40
    angle_step = 2 * math.pi / n_points
    transition_frames = 8
    total_frames = transition_frames * 2

    running = True
    frame = 0
    # 背景圆属性，缓慢变化实现
    num_circles = 30
    bg_circles = []
    # 初始化圆属性
    for i in range(num_circles):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(60, max_radius * 0.95)
        x = spiral_center[0] + dist * math.cos(angle)
        y = spiral_center[1] + dist * math.sin(angle)
        radius = random.randint(12, 44)
        # 纯度（亮度）和透明度都随机
        fade = random.randint(160, 230)
        alpha = random.randint(38, 80)
        # 淡蓝色：R低，G略高，B高
        color = (int(fade*0.7), int(fade*0.85), fade, alpha)
        dx = random.uniform(-0.7, 0.7)
        dy = random.uniform(-0.7, 0.7)
        dr = random.uniform(-0.13, 0.13)
        bg_circles.append({'x': x, 'y': y, 'radius': radius, 'color': color, 'dx': dx, 'dy': dy, 'dr': dr})

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 只生成一次径向渐变背景，提高性能
        if frame == 0:
            grad_center = (spiral_center[0], spiral_center[1])
            grad_r = int(max_radius * 1.05)
            color_center = (220, 200, 255)
            color_edge = (255, 255, 255)
            bg_surf = pygame.Surface((WIDTH, HEIGHT))
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    dist = math.hypot(x - grad_center[0], y - grad_center[1])
                    t = min(dist / grad_r, 1.0)
                    col = (
                        int(color_center[0] * (1-t) + color_edge[0] * t),
                        int(color_center[1] * (1-t) + color_edge[1] * t),
                        int(color_center[2] * (1-t) + color_edge[2] * t)
                    )
                    bg_surf.set_at((x, y), col)
        if frame == 0:
            cached_bg = bg_surf.copy()
        screen.blit(cached_bg, (0, 0))

        # 每帧微调圆的位置和半径，实现缓慢变化
        for c in bg_circles:
            c['x'] += c['dx']
            c['y'] += c['dy']
            c['radius'] += c['dr']
            c['dx'] += random.uniform(-0.03, 0.03)
            c['dy'] += random.uniform(-0.03, 0.03)
            c['dr'] += random.uniform(-0.012, 0.012)
            dist = math.hypot(c['x'] - spiral_center[0], c['y'] - spiral_center[1])
            max_dist = max_radius * 0.93
            if dist > max_dist:
                angle = math.atan2(c['y'] - spiral_center[1], c['x'] - spiral_center[0])
                c['x'] = spiral_center[0] + max_dist * math.cos(angle)
                c['y'] = spiral_center[1] + max_dist * math.sin(angle)
                c['dx'] *= -0.5
                c['dy'] *= -0.5
            c['radius'] = max(8, min(48, c['radius']))
            # 使用Surface实现透明度
            circle_surf = pygame.Surface((int(c['radius']*2+2), int(c['radius']*2+2)), pygame.SRCALPHA)
            pygame.draw.circle(circle_surf, c['color'], (int(c['radius'])+1, int(c['radius'])+1), int(c['radius']), 0)
            screen.blit(circle_surf, (int(c['x']-c['radius']), int(c['y']-c['radius'])))

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

        # 左上角只显示一行地区名和数值，每秒切换
        font = pygame.font.SysFont(None, 28)
        x0, y0 = 18, 18
        # 每秒切换一个地区
        idx = (frame // FPS) % len(countries)
        txt = f'{countries[idx]}: {levels[idx]:.2f}'
        country_text = font.render(txt, True, (40, 40, 80))
        screen.blit(country_text, (x0, y0))

        pygame.display.flip()
        frame += 1
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()