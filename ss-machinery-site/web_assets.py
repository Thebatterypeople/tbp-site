"""Build optimised web assets for the S&S machine pages.
- spin frames: same-scale, bottom-anchored, 1200x1200 transparent webp, ordered front -> right -> rear -> left -> front
- hero priced tile (1080x1080 jpg) from the HERO angle
- angle gallery: white_square 1200 jpg
- logo
"""
import os, json, shutil
import numpy as np
from PIL import Image

NEW = '/home/claude/work/new'
VAR = '/home/claude/work/variants'
OUT = '/home/claude/work/web_assets'
LOGO = '/mnt/user-data/uploads/Machine picscomplete/Machine pics/SS_Machinery_Photo_Set/Logo'

# spin order per machine (clockwise walk-around starting at the front); only same-pose frames
SPIN = {
    'HM370T':  ['05_front_bucket_down', '03_threequarter_front_right', '02_profile_right_bucket_down',
                '01_rear_controls_engine', '06_profile_left_bucket_down', '08_threequarter_front_left_HERO'],
    'HM380T':  ['04_front_auger', '02_threequarter_front_right_auger', '01_profile_right_auger',
                '08_rear_controls', '07_profile_left_auger', '05_threequarter_front_left_auger'],
    'HM750T':  ['08_front_bucket_down', '06_threequarter_front_right_HERO', '03_profile_right',
                '01_rear_engine', '04_profile_left', '05_threequarter_front_left'],
    'HM1000T': ['05_front_bucket_down', '03_threequarter_front_right', '02_profile_right',
                '01_rear_engine', '07_profile_left', '06_threequarter_front_left'],
    'HM1500S': ['07_front_straight', '08_front_threequarter_right_HERO', '09_profile_left_full',
                '01_profile_right_rear', '02_rear_threequarter', '03_rear_straight',
                '04_rear_threequarter_left', '05_profile_left', '06_front_threequarter_left'],
    'HME30T':  ['01_front_straight_boom_forward', '02_front_threequarter_right', '03_profile_right',
                '09_rear_threequarter_right', '08_rear_straight', '07_rear_threequarter_left_cab',
                '06_profile_left_cab'],
}
HERO = {
    'HM370T': '08_threequarter_front_left_HERO', 'HM380T': '03_threequarter_front_right_tight_HERO',
    'HM750T': '06_threequarter_front_right_HERO', 'HM1000T': '04_threequarter_front_right_tight_HERO',
    'HM1500S': '08_front_threequarter_right_HERO', 'HME30T': '04_front_threequarter_left_boom_raised_HERO',
}
S = 1200


def bbox(im):
    a = np.array(im)[:, :, 3]
    ys, xs = np.where(a > 8)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    manifest = {}
    for m, names in SPIN.items():
        d = f'{OUT}/{m}'; os.makedirs(f'{d}/spin', exist_ok=True); os.makedirs(f'{d}/angles', exist_ok=True)
        ims = [Image.open(f'{NEW}/{m}/{n}.png').convert('RGBA') for n in names]
        crops = [im.crop(bbox(im)) for im in ims]
        maxdim = max(max(c.size) for c in crops)
        scale = S * 0.88 / maxdim
        frames = []
        for i, c in enumerate(crops):
            c2 = c.resize((max(1, round(c.width * scale)), max(1, round(c.height * scale))), Image.LANCZOS)
            canvas = Image.new('RGBA', (S, S), (0, 0, 0, 0))
            x = (S - c2.width) // 2
            y = int(S * 0.94) - c2.height  # bottom anchored on a common ground line
            canvas.alpha_composite(c2, (x, y))
            fn = f'spin/{i:02d}.webp'
            canvas.save(f'{d}/{fn}', 'WEBP', quality=82, method=6)
            frames.append(fn)
        # angle gallery from white_square set (1200 jpg)
        angles = []
        wsq = sorted(os.listdir(f'{VAR}/{m}/white_square'))
        for f in wsq:
            im = Image.open(f'{VAR}/{m}/white_square/{f}').convert('RGB').resize((S, S), Image.LANCZOS)
            fn = f'angles/{os.path.splitext(f)[0]}.jpg'
            im.save(f'{d}/{fn}', 'JPEG', quality=84, optimize=True, progressive=True)
            angles.append(fn)
        # hero priced tile
        price_dir = f'{VAR}/{m}/social_branded_price'
        hero_tile = [f for f in os.listdir(price_dir) if f.startswith(HERO[m]) and f.endswith('1080x1080.jpg')][0]
        im = Image.open(f'{price_dir}/{hero_tile}').convert('RGB')
        im.save(f'{d}/hero_tile.jpg', 'JPEG', quality=86, optimize=True, progressive=True)
        # hero cutout transparent (for OG/listing)
        hc = Image.open(f'{NEW}/{m}/{HERO[m]}.png').convert('RGBA')
        hc.thumbnail((1600, 1600), Image.LANCZOS)
        hc.save(f'{d}/hero_cutout.webp', 'WEBP', quality=86, method=6)
        manifest[m] = dict(spin=frames, angles=angles, hero_tile='hero_tile.jpg', hero_cutout='hero_cutout.webp')
        print(m, len(frames), 'frames', len(angles), 'angles')
    os.makedirs(f'{OUT}/brand', exist_ok=True)
    for src, dst, w in [('SS-Machinery-Logo-White-3000px.png', 'logo-white.png', 900),
                        ('SS-Machinery-Logo-Black-3000px.png', 'logo-black.png', 900),
                        ('SS-Shield-Only-White-2000px.png', 'shield-white.png', 400)]:
        im = Image.open(f'{LOGO}/{src}').convert('RGBA')
        im.thumbnail((w, w), Image.LANCZOS)
        im.save(f'{OUT}/brand/{dst}', 'PNG', optimize=True)
    json.dump(manifest, open(f'{OUT}/manifest.json', 'w'), indent=1)
    os.system(f'du -sh {OUT}; du -sh {OUT}/*')


main()
