import math
import time
import cv2
import mediapipe as mp
import numpy as np

# --- MEDIAPIPE SETUP ---
# MediaPipe import pera dey onak shomoy, so safety check
try:
    import mediapipe.python.solutions.face_mesh as mp_face_mesh
    import mediapipe.python.solutions.hands as mp_hands
except ImportError:
    mp_hands = mp.solutions.hands
    mp_face_mesh = mp.solutions.face_mesh

# Confidence high rakhsilam jate potato webcam hand hallucinate na kore
hands = mp_hands.Hands(
    max_num_hands=2, min_detection_confidence=0.80, min_tracking_confidence=0.80
)

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1, min_detection_confidence=0.6, min_tracking_confidence=0.6
)

cap = cv2.VideoCapture(0)

# Window Configuration 
WIN_TITLE = "Mama Hand FX Studio v3.0 - Zen Mode Edition"
cv2.namedWindow(WIN_TITLE, cv2.WINDOW_NORMAL)

FX_LIST = [
    "INVERT",
    "THERMAL MAP",
    "CYBER EDGES",
    "8-BIT PIXELATE",
    "RETRO SEPIA",
    "SOFT BLUR",
    "RGB GLITCH",
    "NIGHT VISION",
    "3D - SUNGLASSES",
]
current_fx = 8  # 3d chosma
fullscreen_mode = False
ui_hidden = False  # Toggle for FOCUS Mode

COLOR_GOLD = (255, 200, 100)
COLOR_NEON = (180, 255, 180)
COLOR_WHITE = (240, 240, 240)
COLOR_DIM = (140, 140, 140)
COLOR_LOCK = (0, 215, 255)
glasses_xy = [320.0, 240.0]
glasses_rot = 0.0
glasses_zoom = 1.0
is_pinching = False
locked_layers = []

# --- SMOOTHING TRACKING (JITTER FIX) ---(ts was soo hard 😭😭)
smoothed_points = {}
SMOOTH_FACTOR = 0.35

# Timing logic
t_prev = 0
HOLD_LIMIT = 0.85
COOLDOWN = 0.8

fist_start_time = None
last_trigger = 0
banner_txt = ""
banner_timer = 0


def check_fist(hand_lms):
    finger_tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    folded = sum(
        1
        for tip, pip in zip(finger_tips, pips)
        if hand_lms.landmark[tip].y > hand_lms.landmark[pip].y
    )
    return folded >= 4


def get_palm_center(hand_lms, width, height):
    knuckles = [0, 5, 9, 13, 17]
    cx = sum(hand_lms.landmark[i].x for i in knuckles) / len(knuckles)
    cy = sum(hand_lms.landmark[i].y for i in knuckles) / len(knuckles)
    return int(cx * width), int(cy * height)


def smooth_pt(pt_key, rx, ry):
    if pt_key not in smoothed_points:
        smoothed_points[pt_key] = (float(rx), float(ry))

    ox, oy = smoothed_points[pt_key]
    nx = ox * (1.0 - SMOOTH_FACTOR) + rx * SMOOTH_FACTOR
    ny = oy * (1.0 - SMOOTH_FACTOR) + ry * SMOOTH_FACTOR
    smoothed_points[pt_key] = (nx, ny)
    return int(nx), int(ny)


def draw_choshma(img, pos, angle, scale=1.0):
    cx, cy = int(pos[0]), int(pos[1])
    rad = math.radians(angle)
    c_a, s_a = math.cos(rad), math.sin(rad)

    def rot_p(x, y):
        sx, sy = x * scale, y * scale
        rx = sx * c_a - sy * s_a
        ry = sx * s_a + sy * c_a
        return (int(cx + rx), int(cy + ry))

    left_lens = np.array(
        [
            rot_p(-55, -20),
            rot_p(-10, -20),
            rot_p(-12, 25),
            rot_p(-38, 32),
            rot_p(-58, 12),
        ],
        dtype=np.int32,
    )

    right_lens = np.array(
        [
            rot_p(10, -20),
            rot_p(55, -20),
            rot_p(58, 12),
            rot_p(38, 32),
            rot_p(12, 25),
        ],
        dtype=np.int32,
    )

    cv2.fillPoly(img, [left_lens], (20, 20, 20), cv2.LINE_AA)
    cv2.fillPoly(img, [right_lens], (20, 20, 20), cv2.LINE_AA)

    cv2.polylines(img, [left_lens], True, COLOR_GOLD, 3, cv2.LINE_AA)
    cv2.polylines(img, [right_lens], True, COLOR_GOLD, 3, cv2.LINE_AA)

    cv2.line(img, rot_p(-10, -18), rot_p(10, -18), COLOR_GOLD, 3, cv2.LINE_AA)
    cv2.line(img, rot_p(-8, -10), rot_p(8, -10), COLOR_GOLD, 2, cv2.LINE_AA)

    cv2.line(
        img, rot_p(-48, -12), rot_p(-28, 15), (255, 255, 255), 2, cv2.LINE_AA
    )
    cv2.line(
        img, rot_p(18, -12), rot_p(38, 15), (255, 255, 255), 2, cv2.LINE_AA
    )


def do_effect(src, fx_id):
    if fx_id == 0:
        return cv2.bitwise_not(src)
    elif fx_id == 1:
        g = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        return cv2.applyColorMap(g, cv2.COLORMAP_JET)
    elif fx_id == 2:
        edges = cv2.Canny(src, 70, 150)
        e_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        e_bgr[edges > 0] = COLOR_GOLD
        return e_bgr
    elif fx_id == 3:
        h, w = src.shape[:2]
        small = cv2.resize(
            src, (max(1, w // 14), max(1, h // 14)), interpolation=cv2.INTER_LINEAR
        )
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    elif fx_id == 4:
        sepia = np.array(
            [
                [0.272, 0.534, 0.131],
                [0.349, 0.686, 0.168],
                [0.393, 0.769, 0.189],
            ]
        )
        v = cv2.transform(src, sepia)
        return np.clip(v, 0, 255).astype(np.uint8)
    elif fx_id == 5:
        return cv2.GaussianBlur(src, (35, 35), 0)
    elif fx_id == 6:
        g = src.copy()
        s = 10
        g[:, :-s, 2] = src[:, s:, 2]
        g[:, s:, 0] = src[:, :-s, 0]
        return g
    elif fx_id == 7:
        g = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        hud_g = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
        hud_g[:, :, 0] = 0
        hud_g[:, :, 2] = 0
        return hud_g
    elif fx_id == 8:
        draw_choshma(src, glasses_xy, glasses_rot, glasses_zoom)
        return src
    return src


def draw_fingertip(img, pt, color):
    cv2.circle(img, pt, 5, color, -1, cv2.LINE_AA)
    cv2.circle(img, pt, 2, (255, 255, 255), -1, cv2.LINE_AA)


def draw_brackets(img, p1, p2, color):
    x1, y1 = p1
    x2, y2 = p2
    L = 14
    cv2.line(img, (x1, y1), (x1 + L, y1), color, 1, cv2.LINE_AA)
    cv2.line(img, (x1, y1), (x1, y1 + L), color, 1, cv2.LINE_AA)
    cv2.line(img, (x2, y1), (x2 - L, y1), color, 1, cv2.LINE_AA)
    cv2.line(img, (x2, y1), (x2, y1 + L), color, 1, cv2.LINE_AA)
    cv2.line(img, (x1, y2), (x1 + L, y2), color, 1, cv2.LINE_AA)
    cv2.line(img, (x1, y2), (x1, y2 - L), color, 1, cv2.LINE_AA)
    cv2.line(img, (x2, y2), (x2 - L, y2), color, 1, cv2.LINE_AA)
    cv2.line(img, (x2, y2), (x2, y2 - L), color, 1, cv2.LINE_AA)


print(
    "Trendy Thingy with no name running"
)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("camera off ?")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    t_curr = time.time()
    fps = int(1 / (t_curr - t_prev)) if (t_curr - t_prev) > 0 else 0
    t_prev = t_curr

    pts_finger = []
    fists_found = []
    is_pinching = False
    has_selection = False
    mask = np.zeros((h, w), dtype=np.uint8)
    if not ui_hidden:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res_hands = hands.process(rgb)
        res_face = face_mesh.process(rgb)
        active_keys = set()

        # Hand Logic
        if res_hands.multi_hand_landmarks:
            for idx, h_lms in enumerate(res_hands.multi_hand_landmarks):
                if check_fist(h_lms):
                    fists_found.append(get_palm_center(h_lms, w, h))
                else:
                    t_raw = (h_lms.landmark[4].x * w, h_lms.landmark[4].y * h)
                    i_raw = (h_lms.landmark[8].x * w, h_lms.landmark[8].y * h)

                    k_thumb, k_index = f"h{idx}_t", f"h{idx}_i"
                    active_keys.update([k_thumb, k_index])

                    pt_thumb = smooth_pt(k_thumb, t_raw[0], t_raw[1])
                    pt_index = smooth_pt(k_index, i_raw[0], i_raw[1])

                    pts_finger.append(pt_thumb)
                    pts_finger.append(pt_index)

                    # Pinch check for choshma drag
                    dist_pinch = math.hypot(
                        pt_thumb[0] - pt_index[0], pt_thumb[1] - pt_index[1]
                    )
                    if dist_pinch < 45 and current_fx == 8:
                        is_pinching = True
                        mid_x = (pt_thumb[0] + pt_index[0]) / 2.0
                        mid_y = (pt_thumb[1] + pt_index[1]) / 2.0

                        glasses_xy[0] += (mid_x - glasses_xy[0]) * 0.35
                        glasses_xy[1] += (mid_y - glasses_xy[1]) * 0.35

                    draw_fingertip(frame, pt_thumb, COLOR_GOLD)
                    draw_fingertip(frame, pt_index, COLOR_NEON)

        # Clean inactive keys
        for k in list(smoothed_points.keys()):
            if k not in active_keys:
                del smoothed_points[k]

        # Face Mesh Logic(i used Ai here because im dumb and cooked)
        if not is_pinching and current_fx == 8 and res_face.multi_face_landmarks:
            face_lms = res_face.multi_face_landmarks[0]
            eye_l = (
                int(face_lms.landmark[33].x * w),
                int(face_lms.landmark[33].y * h),
            )
            eye_r = (
                int(face_lms.landmark[263].x * w),
                int(face_lms.landmark[263].y * h),
            )

            e_cx = (eye_l[0] + eye_r[0]) / 2.0
            e_cy = (eye_l[1] + eye_r[1]) / 2.0

            dx = eye_r[0] - eye_l[0]
            dy = eye_r[1] - eye_l[1]
            dist_eyes = math.hypot(dx, dy)

            target_rot = math.degrees(math.atan2(dy, dx))
            target_zoom = max(0.5, dist_eyes / 110.0)

            glasses_xy[0] += (e_cx - glasses_xy[0]) * 0.4
            glasses_xy[1] += (eye_l[1] - glasses_xy[1]) * 0.4
            glasses_rot += (target_rot - glasses_rot) * 0.4
            glasses_zoom += (target_zoom - glasses_zoom) * 0.4

        # Region Selection Mask
        if len(pts_finger) == 2:
            p1, p2 = pts_finger[0], pts_finger[1]
            cx, cy = (p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2
            rad = int(np.hypot(p2[0] - p1[0], p2[1] - p1[1]) / 2)

            if rad > 10:
                cv2.circle(mask, (cx, cy), rad, 255, -1)
                has_selection = True
                cv2.circle(frame, (cx, cy), rad, COLOR_GOLD, 1, cv2.LINE_AA)

        elif len(pts_finger) == 4:
            xs = [p[0] for p in pts_finger]
            ys = [p[1] for p in pts_finger]

            min_x, max_x = max(0, min(xs)), min(w, max(xs))
            min_y, max_y = max(0, min(ys)), min(h, max(ys))

            bw, bh = max_x - min_x, max_y - min_y

            if bw > 20 and bh > 20:
                cv2.rectangle(mask, (min_x, min_y), (max_x, max_y), 255, -1)
                has_selection = True
                cv2.rectangle(
                    frame,
                    (min_x, min_y),
                    (max_x, max_y),
                    COLOR_GOLD,
                    1,
                    cv2.LINE_AA,
                )
                draw_brackets(
                    frame, (min_x, min_y), (max_x, max_y), COLOR_GOLD
                )

        fist_cnt = len(fists_found)
        if (
            fist_cnt > 0
            and not has_selection
            and (t_curr - last_trigger > COOLDOWN)
        ):
            if fist_start_time is None:
                fist_start_time = t_curr

            dt = t_curr - fist_start_time
            prog = min(1.0, dt / HOLD_LIMIT)

            for center in fists_found:
                deg = int(prog * 360)
                cv2.ellipse(
                    frame,
                    center,
                    (22, 22),
                    -90,
                    0,
                    deg,
                    COLOR_NEON,
                    2,
                    cv2.LINE_AA,
                )
                cv2.circle(frame, center, 3, COLOR_GOLD, -1, cv2.LINE_AA)

            if prog >= 1.0:
                if fist_cnt == 1:
                    current_fx = (current_fx + 1) % len(FX_LIST)
                    banner_txt = f"SWITCHED >> {FX_LIST[current_fx]}"
                elif fist_cnt >= 2:
                    current_fx = (current_fx - 1) % len(FX_LIST)
                    banner_txt = f"SWITCHED << {FX_LIST[current_fx]}"

                last_trigger = t_curr
                banner_timer = t_curr
                fist_start_time = None
        else:
            fist_start_time = None

    # 1. Render all locked layers
    for l_mask, l_fx in locked_layers:
        locked_fx_frame = do_effect(frame, l_fx)
        frame = np.where(l_mask[:, :, None] == 255, locked_fx_frame, frame)
        if not ui_hidden:
            contours, _ = cv2.findContours(
                l_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            cv2.drawContours(frame, contours, -1, COLOR_LOCK, 1, cv2.LINE_AA)

    # 2. Render live active effect
    if current_fx == 8:
        frame = do_effect(frame, current_fx)
    elif has_selection and not ui_hidden:
        processed_frame = do_effect(frame, current_fx)
        frame = np.where(mask[:, :, None] == 255, processed_frame, frame)

    # --- RENDER HUD OVERLAY ---
    if not ui_hidden:
        hud = frame.copy()
        cv2.rectangle(hud, (0, 0), (w, 38), (15, 15, 15), -1)
        cv2.rectangle(hud, (0, h - 28), (w, h), (15, 15, 15), -1)
        cv2.rectangle(hud, (15, 50), (200, 295), (15, 15, 15), -1)
        frame = cv2.addWeighted(hud, 0.7, frame, 0.3, 0)

        # Left Side Menu
        cv2.putText(
            frame,
            "EFFECT ENGINE",
            (25, 68),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            COLOR_DIM,
            1,
            cv2.LINE_AA,
        )
        for idx, name in enumerate(FX_LIST):
            active = idx == current_fx
            col = COLOR_NEON if active else COLOR_WHITE
            prefix = "> " if active else "  "
            cv2.putText(
                frame,
                f"{prefix}{name}",
                (25, 88 + (idx * 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.38,
                col,
                1,
                cv2.LINE_AA,
            )

        cv2.putText(
            frame,
            f"LOCKED: {len(locked_layers)}",
            (25, 280),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            COLOR_LOCK,
            1,
            cv2.LINE_AA,
        )

        # Banner message
        if t_curr - banner_timer < 0.8:
            b_w = 360
            cv2.rectangle(  
                frame,
                (w // 2 - b_w // 2, 48),
                (w // 2 + b_w // 2, 76),
                (20, 20, 20),
                -1,
            )
            cv2.rectangle(
                frame,
                (w // 2 - b_w // 2, 48),
                (w // 2 + b_w // 2, 76),
                COLOR_GOLD,
                1,
            )
            cv2.putText(
                frame,
                banner_txt,
                (w // 2 - b_w // 2 + 12, 66),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.38,
                COLOR_WHITE,
                1,
                cv2.LINE_AA,
            )

        # FPS
        cv2.putText(
            frame,
            f"FPS: {fps}",
            (w - 80, 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            COLOR_WHITE,
            1,
            cv2.LINE_AA,
        )

        cv2.putText(
            frame,
            "[H] FOCUS MODE  |  [L] LOCK REGION  |  [C] CLEAR LOCKS  |  [Q] QUIT",
            (20, h - 9),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            COLOR_DIM,
            1,
            cv2.LINE_AA,
        )

    cv2.imshow(WIN_TITLE, frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif ord("1") <= key <= ord("9"):
        current_fx = key - ord("1")
    elif key in [ord("f"), ord("F")]:
        fullscreen_mode = not fullscreen_mode
        prop = cv2.WINDOW_FULLSCREEN if fullscreen_mode else cv2.WINDOW_NORMAL
        cv2.setWindowProperty(WIN_TITLE, cv2.WND_PROP_FULLSCREEN, prop)

    # FOCUS MODE TOGGLE
    elif key in [ord("h"), ord("H")]:
        ui_hidden = not ui_hidden
        banner_txt = (
            "FOCUS ACTIVATED 🔕" if ui_hidden else "UI RESTORED 🔔"
        )
        banner_timer = t_curr

    # LOCK & CLEAR CONTROLS
    elif key in [ord("l"), ord("L")]:
        if has_selection and not ui_hidden:
            locked_layers.append((mask.copy(), current_fx))
            banner_txt = f"LOCKED {FX_LIST[current_fx]} LAYER 🔒"
            banner_timer = t_curr   
        else:
            banner_txt = "SELECT REGION WITH FINGERS FIRST!"
            banner_timer = t_curr
    elif key in [ord("c"), ord("C")]:
        locked_layers.clear()
        banner_txt = "ALL LOCKED LAYERS CLEARED 🧹"
        banner_timer = t_curr

cap.release()
cv2.destroyAllWindows()
