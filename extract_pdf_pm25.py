import PyPDF2
import re

pdf_path = '数据pdf.pdf'

def extract_total_pm25(pdf_path):
    data = []
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                # 匹配国家名和 Total 列的第一个数值（如 Afghanistan 62.49 ...）
                match = re.match(r'^(\w[\w\s\(\)-]+)\s+(\d+\.\d+)', line)
                if match:
                    country = match.group(1).strip()
                    value = float(match.group(2))
                    data.append((country, value))
    return data


import pygame
import math
import sys

WIDTH, HEIGHT = 900, 900
BG_COLOR = (10, 10, 30)
SPIRAL_COLOR = (0, 200, 255)
FPS = 60

def normalize(data):
    min_v, max_v = min(data), max(data)
    return [(v - min_v) / (max_v - min_v) if max_v > min_v else 0.5 for v in data]

def main():
    pm25_data = extract_total_pm25(pdf_path)
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
    interp_num = 3  # 每两个点之间插入3个点
    for i in range(len(norm_levels) - 1):
        dense_levels.append(norm_levels[i])
        dense_countries.append(countries[i])
        dense_values.append(levels[i])
        for k in range(1, interp_num + 1):
            interp = norm_levels[i] + (norm_levels[i+1] - norm_levels[i]) * k / (interp_num + 1)
            interp_value = levels[i] + (levels[i+1] - levels[i]) * k / (interp_num + 1)
            dense_levels.append(interp)
            dense_countries.append(f'{countries[i]}-{countries[i+1]}')
            dense_values.append(interp_value)
    # 补最后一个点
    dense_levels.append(norm_levels[-1])
    dense_countries.append(countries[-1])
    dense_values.append(levels[-1])
    norm_levels = dense_levels
    countries = dense_countries
    levels = dense_values

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


        # 渐变色列表：深紫、中紫、浅紫、浅蓝、中蓝、深蓝
        colors = [
            (75, 0, 130),    # 深紫
            (138, 43, 226),  # 中紫
            (186, 85, 211),  # 浅紫
            (135, 206, 250), # 浅蓝
            (70, 130, 180),  # 中蓝
            (0, 0, 139)      # 深蓝
        ]
        n_colors = len(colors)
        # 绘制从圆心出发的无数条直线
        for i in range(n_points):
            idx = (i + offset) % n_points
            radius = base_radius + norm_levels[idx] * (max_radius - base_radius)
            angle = i * angle_step + frame * 0.01
            x = spiral_center[0] + radius * math.cos(angle)
            y = spiral_center[1] + radius * math.sin(angle)
            color = colors[i % n_colors]
            pygame.draw.line(screen, color, spiral_center, (x, y), 2)



        # 显示当前国家名和数值
        cur_idx = offset
        font = pygame.font.SysFont(None, 36)
        country_text = font.render(f'{countries[cur_idx]}: {levels[cur_idx]}', True, (255, 255, 255))
        screen.blit(country_text, (spiral_center[0] - 120, spiral_center[1] - max_radius - 40))

        pygame.display.flip()
        frame += 1
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
