"""
regen_demos.py - 重新生成 gui_demos/ 下的展示图
用每种方法在最能体现优势的场景下运行，产出高质量示例。
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gui import (
    create_corruption,
    load_and_prepare_image,
    run_repair,
    to_display,
)
from src.utils import compute_metrics, normalize_image, to_gray, resize_image

DEMO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui_demos')


def save_png(arr, path):
    Image.fromarray(to_display(arr)).save(path)


def make_demo(tag, img_name, corr_type, rate, method, label_extra=''):
    img = load_and_prepare_image(img_name, None, image_size=256)
    corr, mask = create_corruption(img, corr_type, rate)
    rep, _, _ = run_repair(img, corr, mask, method, corr_type)
    m = compute_metrics(img, rep)
    save_png(img, os.path.join(DEMO_DIR, f'{tag}_orig.png'))
    save_png(corr, os.path.join(DEMO_DIR, f'{tag}_corrupt.png'))
    save_png(rep, os.path.join(DEMO_DIR, f'{tag}_repair.png'))
    info = f'{img_name}|{corr_type}({int(rate*100)}%){label_extra}|{method}|{method}|PSNR={m["PSNR"]:.2f}|SSIM={m["SSIM"]:.4f}'
    with open(os.path.join(DEMO_DIR, f'{tag}_info.txt'), 'w', encoding='utf-8') as f:
        f.write(info)
    print(f'[{tag}] {img_name} {corr_type}@{rate} {method}  PSNR={m["PSNR"]:.2f} SSIM={m["SSIM"]:.3f}')


def make_real_demo(tag, img_name, method):
    """真实划痕旧照片：没有 ground truth，用 mask 粗略估计。"""
    from src.utils import get_test_image
    img = get_test_image(img_name, gray=True, size=(256, 256))
    # 使用亮度阈值生成一个近似划痕 mask（划痕是亮白条纹）
    mask = (img < 0.92).astype(np.float64)
    corr = img.copy()
    # 对于真实划痕图：直接把原图作为观测，mask=1 表示可信像素
    rep, _, _ = run_repair(img, corr, mask, method, '划痕')
    save_png(img, os.path.join(DEMO_DIR, f'{tag}_orig.png'))
    save_png(corr, os.path.join(DEMO_DIR, f'{tag}_corrupt.png'))
    save_png(rep, os.path.join(DEMO_DIR, f'{tag}_repair.png'))
    info = f'{img_name}|真实划痕旧照|{method}|{method}|PSNR=N/A|SSIM=N/A'
    with open(os.path.join(DEMO_DIR, f'{tag}_info.txt'), 'w', encoding='utf-8') as f:
        f.write(info)
    print(f'[{tag}] real photo {img_name} {method}')


if __name__ == '__main__':
    os.makedirs(DEMO_DIR, exist_ok=True)
    # 每个方法选一个最能展现优势的组合
    make_demo('demo1_rpca_text',     'lena',     '文字叠加',    0.10, 'RPCA')
    make_demo('demo2_rslt_scratch',  'barbara',  '划痕',       0.08, 'RSLT')
    make_demo('demo3_patchwnn_pix',  'lena',     '随机像素缺失', 0.30, 'Patch-WNN')
    make_demo('demo4_rslt_pix',      'barbara',  '随机像素缺失', 0.20, 'RSLT')
    make_demo('demo5_rpca_scratch',  'peppers',  '划痕',       0.08, 'RPCA')
    make_demo('demo6_patchwnn_text', 'cameraman','文字叠加',    0.10, 'Patch-WNN')
    # 真实旧照片
    make_real_demo('demo7_real_photo1', 'old_scratch2', 'RPCA')
    make_real_demo('demo8_real_photo2', 'old_scratch3', 'RPCA')

    # 清理旧的 demo 文件
    import glob
    old_tags = ['demo1_rpca_real', 'demo2_rpca_text', 'demo3_rslt_scratch',
                'demo4_rslt_inpaint', 'demo5_patchwnn_inpaint', 'demo6_rpca_real2']
    for tag in old_tags:
        for path in glob.glob(os.path.join(DEMO_DIR, f'{tag}_*')):
            os.remove(path)
            print(f'removed {os.path.basename(path)}')
