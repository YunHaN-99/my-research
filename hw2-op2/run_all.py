"""
run_all.py - 深度分析版统一入口

默认顺序：
1. 第一章：低秩性分析
2. 第二章：核范数 + ADMM
3. 第三章：非凸替代
4. 第四章：Patch-based + RPCA
5. 第五章：RSLT 稀疏低秩纹理修复
6. 第六章：TILT 变换不变低秩纹理
7. 第七章：多尺度创新方法
8. 第八章：最终横评
"""

import argparse
import importlib.util
import os


ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(ROOT_DIR, 'src')


CHAPTER_MAP = {
    'chapter1': 'chapter1_foundation',
    'chapter2': 'chapter2_nuclear_norm',
    'chapter3': 'chapter3_nonconvex',
    'chapter4': 'chapter4_patch_rpca',
    'chapter5': 'chapter5_rslt',
    'chapter6': 'chapter6_tilt',
    'chapter7': 'chapter7_innovation',
    'chapter8': 'chapter8_comparison',
}


def load_module(module_name):
    path = os.path.join(SRC_DIR, f'{module_name}.py')
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description='运行低秩分解图像修复深度分析版实验')
    parser.add_argument('--quick', action='store_true', help='快速自检模式')
    parser.add_argument('--chapter', choices=['all', *CHAPTER_MAP.keys()], default='all', help='只运行指定章节')
    args = parser.parse_args()

    size = (96, 96) if args.quick else (256, 256)
    print(f'运行模式: {"quick" if args.quick else "full"}')
    print(f'图像尺寸: {size}')

    selected = CHAPTER_MAP.keys() if args.chapter == 'all' else [args.chapter]
    for chapter_name in selected:
        module = load_module(CHAPTER_MAP[chapter_name])
        runner = getattr(module, f'run_{chapter_name}')
        print(f'\n===== Running {chapter_name} =====')
        runner(size=size, quick=args.quick)

    print('\n全部请求的章节已执行完成。')


if __name__ == '__main__':
    main()
