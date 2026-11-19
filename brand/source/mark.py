# Foxcrest mark: a fox head whose ears form a crest/roofline; muzzle doubles as a doorway.
def mark(bg="#0b2545", face="#2f7de1", muzzle="#ffffff", detail="#0b2545", inner="#bcd5f5", rounded=True, bgshape=True, eye=None):
    eye = eye or detail
    p = []
    if bgshape:
        p.append(f'<rect width="64" height="64" rx="{15 if rounded else 0}" fill="{bg}"/>')
    # head (ears + cheeks) as one shape
    p.append(f'<path d="M11 11 L25 21 H39 L53 11 L52 33 L32 54 L12 33 Z" fill="{face}"/>')
    # inner ears
    p.append(f'<path d="M15 17 L23 23 L17 27 Z M49 17 L41 23 L47 27 Z" fill="{inner}"/>')
    # white muzzle / roof-gable
    p.append(f'<path d="M19 35 L32 26 L45 35 L32 50 Z" fill="{muzzle}"/>')
    # eyes
    p.append(f'<path d="M19.5 28.6 l6.2 -2.4 l-1.6 4 z M44.5 28.6 l-6.2 -2.4 l1.6 4 z" fill="{eye}"/>')
    # nose = little door
    p.append(f'<path d="M29.5 41 h5 v3.2 l-2.5 2.3 l-2.5 -2.3 z" fill="{detail}"/>')
    return "".join(p)

def svg(inner, w=64, h=64, vb="0 0 64 64"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}">{inner}</svg>'

