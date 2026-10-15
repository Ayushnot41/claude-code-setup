import socket
import json
import time
import sys
import shutil

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def focus_blender():
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        h_desk = user32.OpenDesktopW("default", 0, False, 0x01FF)
        if h_desk:
            user32.SetThreadDesktop(h_desk)
        
        def enum_cb(hwnd, _):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                if "Blender" in buf.value and "blender.exe" not in buf.value.lower():
                    user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
                    user32.SetForegroundWindow(hwnd)
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
        if h_desk:
            user32.CloseDesktop(h_desk)
    except Exception as e:
        pass

def send_blender_code(code):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(120.0)
    try:
        s.connect(('localhost', 9876))
        cmd = {'type': 'execute_code', 'params': {'code': code}}
        s.sendall(json.dumps(cmd).encode('utf-8'))
        
        chunks = []
        while True:
            chunk = s.recv(8192)
            if not chunk:
                break
            chunks.append(chunk)
            data = b"".join(chunks)
            try:
                json.loads(data.decode('utf-8'))
                break
            except json.JSONDecodeError:
                continue
                
        resp = json.loads(data.decode('utf-8'))
        return resp
    finally:
        s.close()

# The 14 discrete, self-contained stages
STAGES = [
    # STAGE 0: Reset & Viewport Initialization
    (r"""
import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

for m in bpy.data.meshes:
    bpy.data.meshes.remove(m)
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)
for c in bpy.data.cameras:
    bpy.data.cameras.remove(c)
for l in bpy.data.lights:
    bpy.data.lights.remove(l)

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'
                space.region_3d.view_perspective = 'PERSP'
                space.region_3d.view_distance = 32.0
                space.region_3d.view_location = (-0.8, 0.0, 7.5)
                space.region_3d.view_rotation = (0.91, 0.40, -0.06, 0.12)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("Scene reset and viewport ready.")
""", "[STAGE 1/14] Initializing Clean High-Fidelity 3D Workspace..."),

    # STAGE 1: Photorealistic PBR Shaders
    (r"""
import bpy

def make_pbr(name, base_color, roughness=0.35, metallic=0.0, sss_weight=0.0, sss_radius=None, bump_type=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new(type='ShaderNodeOutputMaterial')
    out.location = (400, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = base_color
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    
    if sss_weight > 0 and 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = sss_weight
        if sss_radius and 'Subsurface Radius' in bsdf.inputs:
            bsdf.inputs['Subsurface Radius'].default_value = sss_radius

    if bump_type == 'tile_grooves':
        tex_coord = nodes.new(type='ShaderNodeTexCoord')
        wave = nodes.new(type='ShaderNodeTexWave')
        wave.inputs['Scale'].default_value = 28.0
        wave.inputs['Distortion'].default_value = 0.5
        bump = nodes.new(type='ShaderNodeBump')
        bump.inputs['Strength'].default_value = 0.4
        bump.inputs['Distance'].default_value = 0.08
        links.new(tex_coord.outputs['Object'], wave.inputs['Vector'])
        links.new(wave.outputs['Color'], bump.inputs['Height'])
        links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    if bump_type == 'lacquer_grain':
        noise = nodes.new(type='ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 50.0
        noise.inputs['Detail'].default_value = 6.0
        bump = nodes.new(type='ShaderNodeBump')
        bump.inputs['Strength'].default_value = 0.06
        bump.inputs['Distance'].default_value = 0.02
        links.new(noise.outputs['Color'], bump.inputs['Height'])
        links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

make_pbr("Mat_Vermilion", (0.94, 0.15, 0.015, 1.0), roughness=0.28, metallic=0.01, bump_type='lacquer_grain')
make_pbr("Mat_WhitePlaster", (0.96, 0.96, 0.95, 1.0), roughness=0.85, metallic=0.0)
make_pbr("Mat_RoofTile", (0.16, 0.17, 0.20, 1.0), roughness=0.26, metallic=0.18, bump_type='tile_grooves')
make_pbr("Mat_RidgeTile", (0.28, 0.30, 0.34, 1.0), roughness=0.38, metallic=0.08)
make_pbr("Mat_RafterWhiteTip", (0.99, 0.99, 0.99, 1.0), roughness=0.6)
make_pbr("Mat_GoldLeaf", (0.98, 0.78, 0.12, 1.0), roughness=0.18, metallic=0.92)
make_pbr("Mat_AgedBronze", (0.24, 0.26, 0.22, 1.0), roughness=0.38, metallic=0.85)
make_pbr("Mat_MomijiScarlet", (0.92, 0.02, 0.03, 1.0), roughness=0.45, sss_weight=0.65, sss_radius=(0.95, 0.1, 0.05))
make_pbr("Mat_MomijiOrange", (0.98, 0.32, 0.02, 1.0), roughness=0.45, sss_weight=0.65, sss_radius=(0.98, 0.35, 0.05))
make_pbr("Mat_Bark", (0.10, 0.08, 0.06, 1.0), roughness=0.92)
make_pbr("Mat_MountainBlue", (0.28, 0.44, 0.62, 1.0), roughness=0.95)
make_pbr("Mat_Granite", (0.35, 0.36, 0.38, 1.0), roughness=0.88)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("PBR Shaders synthesized.")
""", "[STAGE 2/14] Formulating Photorealistic Cinnabar, Gold Leaf, Shikkui & SSS Shaders..."),

    # STAGE 2: Distant Kyoto Mountains & Horizon
    (r"""
import bpy

mat_mountain = bpy.data.materials.get("Mat_MountainBlue")
mtn_data = [
    (-36.0, 36.0, 11.5, 14.0),
    (-26.0, 32.0, 9.2, 11.0),
    (-18.0, 28.0, 7.5, 9.5),
    (-42.0, 40.0, 14.0, 15.0),
    (-10.0, 26.0, 6.2, 8.5)
]

for idx, (mx, my, mz, mrad) in enumerate(mtn_data):
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=mrad, depth=mz * 2.2, location=(mx, my, mz - 2.5))
    mtn = bpy.context.active_object
    mtn.name = f"Kyoto_Mountain_{idx}"
    mtn.scale = (1.6, 1.1, 0.7)
    for poly in mtn.data.polygons:
        poly.use_smooth = True
    mtn.data.materials.append(mat_mountain)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("Distant mountains sculpted.")
""", "[STAGE 3/14] Sculpting Distant Blue Kyoto Mountains (Higashiyama Range)..."),

    # STAGE 3: Pagoda Tier 1 Core, Pillars, Walls & Balcony
    (r"""
import bpy

mat_vermilion = bpy.data.materials.get("Mat_Vermilion")
mat_white = bpy.data.materials.get("Mat_WhitePlaster")
mat_gold = bpy.data.materials.get("Mat_GoldLeaf")
mat_stone = bpy.data.materials.get("Mat_Granite")

cx, cy = -0.8, 0.0

# Foundation Stone Base
bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, 0.4))
stone_base = bpy.context.active_object
stone_base.scale = (9.2, 9.2, 0.8)
stone_base.data.materials.append(mat_stone)

# Tier 1 Core Sanctuary
bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, 2.3))
t1_core = bpy.context.active_object
t1_core.scale = (5.6, 5.6, 2.6)
t1_core.data.materials.append(mat_white)

# 12 Vermilion Columns
for dx in [-2.7, -0.9, 0.9, 2.7]:
    for dy in [-2.7, 2.7]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=2.7, location=(cx + dx, cy + dy, 2.3))
        bpy.context.active_object.data.materials.append(mat_vermilion)

for dy in [-0.9, 0.9]:
    for dx in [-2.7, 2.7]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=2.7, location=(cx + dx, cy + dy, 2.3))
        bpy.context.active_object.data.materials.append(mat_vermilion)

# Tier 1 Balcony (Kōran)
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy + (side * 3.15), 1.7))
    rail = bpy.context.active_object
    rail.scale = (6.6, 0.1, 0.12)
    rail.data.materials.append(mat_vermilion)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx + (side * 3.15), cy, 1.7))
    rail_s = bpy.context.active_object
    rail_s.scale = (0.1, 6.6, 0.12)
    rail_s.data.materials.append(mat_vermilion)

    for px in [-3.15, 3.15]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.8, location=(cx + px, cy + (side * 3.15), 1.6))
        bpy.context.active_object.data.materials.append(mat_gold)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("Tier 1 core assembled.")
""", "[STAGE 4/14] Building Tier 1 Core, Vermilion Pillars, White Plaster & Balcony..."),

    # STAGE 4: Tier 1 Flared Roof, White-Tipped Rafters & Wind Bells
    (r"""
import bpy
import bmesh
import math

mat_vermilion = bpy.data.materials.get("Mat_Vermilion")
mat_tile = bpy.data.materials.get("Mat_RoofTile")
mat_ridge = bpy.data.materials.get("Mat_RidgeTile")
mat_tip = bpy.data.materials.get("Mat_RafterWhiteTip")
mat_bronze = bpy.data.materials.get("Mat_AgedBronze")
mat_gold = bpy.data.materials.get("Mat_GoldLeaf")

cx, cy = -0.8, 0.0

# 1. White-Tipped Rafters
for side_x in [-1, 1]:
    for i in range(16):
        t = ((i / 15.0) - 0.5) * 6.2
        bpy.ops.mesh.primitive_cube_add(size=1, location=(cx + t, cy + (side_x * 3.3), 3.4))
        raf = bpy.context.active_object
        raf.scale = (0.09, 1.4, 0.09)
        raf.rotation_euler = (math.radians(side_x * -12.0), 0, 0)
        raf.data.materials.append(mat_vermilion)
        
        bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=0.12, location=(cx + t, cy + (side_x * 3.98), 3.28), rotation=(math.radians(side_x * -12.0 + 90), 0, 0))
        bpy.context.active_object.data.materials.append(mat_tip)

# 2. Flared Roof Mesh
def make_flared_roof(name, loc, width, depth, height, flare=0.62):
    bm = bmesh.new()
    gw, gd = 13, 13
    grid = []
    for j in range(gd):
        row = []
        vy = ((j / (gd - 1)) - 0.5) * depth
        ny = abs(vy) / (depth * 0.5)
        for i in range(gw):
            vx = ((i / (gw - 1)) - 0.5) * width
            nx = abs(vx) / (width * 0.5)
            r = math.sqrt(nx**2 + ny**2) / 1.4142
            z = (1.0 - (r**1.35)) * height
            edge = max(nx, ny)
            if edge > 0.6:
                t = (edge - 0.6) / 0.4
                z += (t**2.5) * (height * flare)
            corner = nx * ny
            if corner > 0.35:
                z += ((corner - 0.35)**2) * (height * flare * 2.2)
            row.append(bm.verts.new((vx, vy, z)))
        grid.append(row)
    bm.verts.ensure_lookup_table()
    for j in range(gd - 1):
        for i in range(gw - 1):
            bm.faces.new((grid[j][i], grid[j][i+1], grid[j+1][i+1], grid[j+1][i]))
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    for p in obj.data.polygons:
        p.use_smooth = True
    mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod.thickness = 0.24
    obj.data.materials.append(mat_tile)
    return obj

make_flared_roof("Pagoda_Roof_Tier1", (cx, cy, 3.55), 9.2, 9.2, 1.35, flare=0.62)

# Hip ridge roll caps
for rx, ry in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=5.6, location=(cx + (rx * 2.4), cy + (ry * 2.4), 4.1), rotation=(math.radians(ry * 23), math.radians(rx * -23), math.radians(rx * ry * 45)))
    bpy.context.active_object.data.materials.append(mat_ridge)

# Hanging Bronze Wind Bells
for bx, by in [(-4.5, -4.5), (4.5, -4.5), (-4.5, 4.5), (4.5, 4.5)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.5, location=(cx + bx, cy + by, 3.8 - 0.25))
    bpy.context.active_object.data.materials.append(mat_bronze)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=0.35, location=(cx + bx, cy + by, 3.8 - 0.6))
    bpy.context.active_object.data.materials.append(mat_bronze)
    bpy.ops.mesh.primitive_cone_add(radius1=0.14, depth=0.2, location=(cx + bx, cy + by, 3.8 - 0.82))
    bpy.context.active_object.data.materials.append(mat_gold)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("Tier 1 roof placed.")
""", "[STAGE 5/14] Crafting Tier 1 Flared Tile Roof, White-Tipped Rafters & Wind Bells..."),

    # STAGE 5: Pagoda Tier 2 with Iconic Golden Railings & Lotus Struts
    (r"""
import bpy
import math

mat_vermilion = bpy.data.materials.get("Mat_Vermilion")
mat_white = bpy.data.materials.get("Mat_WhitePlaster")
mat_gold = bpy.data.materials.get("Mat_GoldLeaf")

cx, cy = -0.8, 0.0

# Tier 2 Core Sanctuary
bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, 5.75))
t2_core = bpy.context.active_object
t2_core.scale = (4.6, 4.6, 2.2)
t2_core.data.materials.append(mat_white)

# Tier 2 Pillars
for dx in [-2.2, -0.73, 0.73, 2.2]:
    for dy in [-2.2, 2.2]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=2.3, location=(cx + dx, cy + dy, 5.75))
        bpy.context.active_object.data.materials.append(mat_vermilion)

for dy in [-0.73, 0.73]:
    for dx in [-2.2, 2.2]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=2.3, location=(cx + dx, cy + dy, 5.75))
        bpy.context.active_object.data.materials.append(mat_vermilion)

# Tier 2 Prominent Gold Balcony (vivid in photo!)
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy + (side * 2.65), 5.25))
    rail2 = bpy.context.active_object
    rail2.scale = (5.6, 0.1, 0.14)
    rail2.data.materials.append(mat_gold)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx + (side * 2.65), cy, 5.25))
    rail2_s = bpy.context.active_object
    rail2_s.scale = (0.1, 5.6, 0.14)
    rail2_s.data.materials.append(mat_gold)

    # Decorative lotus brackets (Kaerumata) beneath balcony
    for kx in [-1.9, -0.65, 0.65, 1.9]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(cx + kx, cy + (side * 2.58), 4.95))
        bpy.context.active_object.scale = (0.38, 0.14, 0.36)
        bpy.context.active_object.data.materials.append(mat_gold)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("Tier 2 core and golden balcony assembled.")
""", "[STAGE 6/14] Assembling Tier 2 Pavilion & Prominent Gilded Balcony with Kaerumata Struts..."),

    # STAGE 6: Tier 2 Flared Roof, White-Tipped Rafters & Wind Bells
    (r"""
import bpy
import bmesh
import math

mat_vermilion = bpy.data.materials.get("Mat_Vermilion")
mat_tile = bpy.data.materials.get("Mat_RoofTile")
mat_ridge = bpy.data.materials.get("Mat_RidgeTile")
mat_tip = bpy.data.materials.get("Mat_RafterWhiteTip")
mat_bronze = bpy.data.materials.get("Mat_AgedBronze")
mat_gold = bpy.data.materials.get("Mat_GoldLeaf")

cx, cy = -0.8, 0.0

# 1. White-tipped rafters
for side_x in [-1, 1]:
    for i in range(14):
        t = ((i / 13.0) - 0.5) * 5.2
        bpy.ops.mesh.primitive_cube_add(size=1, location=(cx + t, cy + (side_x * 2.7), 6.7))
        raf = bpy.context.active_object
        raf.scale = (0.085, 1.3, 0.085)
        raf.rotation_euler = (math.radians(side_x * -12.0), 0, 0)
        raf.data.materials.append(mat_vermilion)
        
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.12, location=(cx + t, cy + (side_x * 3.32), 6.58), rotation=(math.radians(side_x * -12.0 + 90), 0, 0))
        bpy.context.active_object.data.materials.append(mat_tip)

# 2. Flared Roof Mesh
bm = bmesh.new()
gw, gd = 13, 13
width, depth, height, flare = 7.8, 7.8, 1.25, 0.62
grid = []
for j in range(gd):
    row = []
    vy = ((j / (gd - 1)) - 0.5) * depth
    ny = abs(vy) / (depth * 0.5)
    for i in range(gw):
        vx = ((i / (gw - 1)) - 0.5) * width
        nx = abs(vx) / (width * 0.5)
        r = math.sqrt(nx**2 + ny**2) / 1.4142
        z = (1.0 - (r**1.35)) * height
        edge = max(nx, ny)
        if edge > 0.6:
            t = (edge - 0.6) / 0.4
            z += (t**2.5) * (height * flare)
        corner = nx * ny
        if corner > 0.35:
            z += ((corner - 0.35)**2) * (height * flare * 2.2)
        row.append(bm.verts.new((vx, vy, z)))
    grid.append(row)
bm.verts.ensure_lookup_table()
for j in range(gd - 1):
    for i in range(gw - 1):
        bm.faces.new((grid[j][i], grid[j][i+1], grid[j+1][i+1], grid[j+1][i]))
mesh = bpy.data.meshes.new("Pagoda_Roof_Tier2")
bm.to_mesh(mesh)
bm.free()
obj = bpy.data.objects.new("Pagoda_Roof_Tier2", mesh)
bpy.context.collection.objects.link(obj)
obj.location = (cx, cy, 6.85)
for p in obj.data.polygons:
    p.use_smooth = True
mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
mod.thickness = 0.24
obj.data.materials.append(mat_tile)

# Hip ridge roll caps
for rx, ry in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=4.8, location=(cx + (rx * 2.0), cy + (ry * 2.0), 7.35), rotation=(math.radians(ry * 23), math.radians(rx * -23), math.radians(rx * ry * 45)))
    bpy.context.active_object.data.materials.append(mat_ridge)

# Bells
for bx, by in [(-3.8, -3.8), (3.8, -3.8), (-3.8, 3.8), (3.8, 3.8)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.45, location=(cx + bx, cy + by, 7.0 - 0.22))
    bpy.context.active_object.data.materials.append(mat_bronze)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.32, location=(cx + bx, cy + by, 7.0 - 0.52))
    bpy.context.active_object.data.materials.append(mat_bronze)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("Tier 2 roof placed.")
""", "[STAGE 7/14] Sculpting Second Tier Roof Eaves, Hip Caps & Wind Bells..."),

    # STAGE 7: Pagoda Tier 3 Sanctuary & Tokyo Bracket Clusters
    (r"""
import bpy
import math

mat_vermilion = bpy.data.materials.get("Mat_Vermilion")
mat_white = bpy.data.materials.get("Mat_WhitePlaster")

cx, cy = -0.8, 0.0

# Tier 3 Core Sanctuary
bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, 8.75))
t3_core = bpy.context.active_object
t3_core.scale = (3.8, 3.8, 1.9)
t3_core.data.materials.append(mat_white)

# Tier 3 Pillars
for dx in [-1.8, -0.6, 0.6, 1.8]:
    for dy in [-1.8, 1.8]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=2.0, location=(cx + dx, cy + dy, 8.75))
        bpy.context.active_object.data.materials.append(mat_vermilion)

for dy in [-0.6, 0.6]:
    for dx in [-1.8, 1.8]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=2.0, location=(cx + dx, cy + dy, 8.75))
        bpy.context.active_object.data.materials.append(mat_vermilion)

# Upper Tokyo Bracket Blocks
for i in range(16):
    ang = (i / 16.0) * math.pi * 2.0
    bx = math.cos(ang) * 2.0
    by = math.sin(ang) * 2.0
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx + bx, cy + by, 9.6))
    brk = bpy.context.active_object
    brk.scale = (0.34, 0.34, 0.22)
    brk.data.materials.append(mat_vermilion)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("Tier 3 sanctuary assembled.")
""", "[STAGE 8/14] Raising Third Tier Sanctuary Core & Intricate Tokyo Brackets..."),

    # STAGE 8: Grand Top Flared Roof, White-Tipped Rafters & Wind Bells
    (r"""
import bpy
import bmesh
import math

mat_vermilion = bpy.data.materials.get("Mat_Vermilion")
mat_tile = bpy.data.materials.get("Mat_RoofTile")
mat_ridge = bpy.data.materials.get("Mat_RidgeTile")
mat_tip = bpy.data.materials.get("Mat_RafterWhiteTip")
mat_bronze = bpy.data.materials.get("Mat_AgedBronze")

cx, cy = -0.8, 0.0

# White-tipped rafters
for side_x in [-1, 1]:
    for i in range(12):
        t = ((i / 11.0) - 0.5) * 4.2
        bpy.ops.mesh.primitive_cube_add(size=1, location=(cx + t, cy + (side_x * 2.2), 9.65))
        raf = bpy.context.active_object
        raf.scale = (0.08, 1.2, 0.08)
        raf.rotation_euler = (math.radians(side_x * -12.0), 0, 0)
        raf.data.materials.append(mat_vermilion)
        
        bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=0.12, location=(cx + t, cy + (side_x * 2.78), 9.54), rotation=(math.radians(side_x * -12.0 + 90), 0, 0))
        bpy.context.active_object.data.materials.append(mat_tip)

# Grand Top Flared Roof
bm = bmesh.new()
gw, gd = 13, 13
width, depth, height, flare = 6.8, 6.8, 1.45, 0.68
grid = []
for j in range(gd):
    row = []
    vy = ((j / (gd - 1)) - 0.5) * depth
    ny = abs(vy) / (depth * 0.5)
    for i in range(gw):
        vx = ((i / (gw - 1)) - 0.5) * width
        nx = abs(vx) / (width * 0.5)
        r = math.sqrt(nx**2 + ny**2) / 1.4142
        z = (1.0 - (r**1.35)) * height
        edge = max(nx, ny)
        if edge > 0.6:
            t = (edge - 0.6) / 0.4
            z += (t**2.5) * (height * flare)
        corner = nx * ny
        if corner > 0.35:
            z += ((corner - 0.35)**2) * (height * flare * 2.2)
        row.append(bm.verts.new((vx, vy, z)))
    grid.append(row)
bm.verts.ensure_lookup_table()
for j in range(gd - 1):
    for i in range(gw - 1):
        bm.faces.new((grid[j][i], grid[j][i+1], grid[j+1][i+1], grid[j+1][i]))
mesh = bpy.data.meshes.new("Pagoda_Roof_Top")
bm.to_mesh(mesh)
bm.free()
obj = bpy.data.objects.new("Pagoda_Roof_Top", mesh)
bpy.context.collection.objects.link(obj)
obj.location = (cx, cy, 9.8)
for p in obj.data.polygons:
    p.use_smooth = True
mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
mod.thickness = 0.24
obj.data.materials.append(mat_tile)

# Ridge caps
for rx, ry in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=4.2, location=(cx + (rx * 1.7), cy + (ry * 1.7), 10.45), rotation=(math.radians(ry * 23), math.radians(rx * -23), math.radians(rx * ry * 45)))
    bpy.context.active_object.data.materials.append(mat_ridge)

for bx, by in [(-3.3, -3.3), (3.3, -3.3), (-3.3, 3.3), (3.3, 3.3)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.32, location=(cx + bx, cy + by, 10.0 - 0.5))
    bpy.context.active_object.data.materials.append(mat_bronze)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("Grand top roof placed.")
""", "[STAGE 9/14] Sculpting Grand Top Roof, Kiguchi Rafters & Wind Bells..."),

    # STAGE 9: Sacred Bronze Sōrin Spire (9 Sacred Rings)
    (r"""
import bpy

mat_bronze = bpy.data.materials.get("Mat_AgedBronze")
mat_gold = bpy.data.materials.get("Mat_GoldLeaf")

cx, cy = -0.8, 0.0
sz = 11.25

# Dew basin & inverted bowl (Roban & Fukubachi)
bpy.ops.mesh.primitive_cylinder_add(radius=0.65, depth=0.4, location=(cx, cy, sz))
bpy.context.active_object.data.materials.append(mat_bronze)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45, location=(cx, cy, sz + 0.35))
bpy.context.active_object.scale = (1.0, 1.0, 0.6)
bpy.context.active_object.data.materials.append(mat_bronze)

# Central bronze spire shaft
bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=4.5, location=(cx, cy, sz + 2.3))
bpy.context.active_object.data.materials.append(mat_bronze)

# 9 Sacred Bronze Rings (Kurin)
for ri in range(9):
    rz = sz + 0.75 + (ri * 0.24)
    rr = 0.44 - (ri * 0.016)
    bpy.ops.mesh.primitive_torus_add(major_radius=rr, minor_radius=0.05, location=(cx, cy, rz))
    bpy.context.active_object.data.materials.append(mat_bronze)

# Water Flame Pattern (Suien)
bpy.ops.mesh.primitive_cone_add(radius1=0.38, radius2=0.08, depth=0.8, location=(cx, cy, sz + 3.2))
bpy.context.active_object.data.materials.append(mat_gold)

# Sacred Flaming Pearl (Hōju)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(cx, cy, sz + 3.85))
bpy.context.active_object.data.materials.append(mat_gold)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("Sorin spire erected.")
""", "[STAGE 10/14] Raising the Sacred Bronze Sorin Spire with 9 Sacred Rings..."),

    # STAGE 10: Right Temple Hall & Left Pavilion Eave
    (r"""
import bpy
import bmesh
import math

mat_vermilion = bpy.data.materials.get("Mat_Vermilion")
mat_white = bpy.data.materials.get("Mat_WhitePlaster")
mat_tile = bpy.data.materials.get("Mat_RoofTile")
mat_ridge = bpy.data.materials.get("Mat_RidgeTile")
mat_gold = bpy.data.materials.get("Mat_GoldLeaf")

# 1. Right Temple Hall (cutting across the right side of the photo)
hx, hy, hz = 11.8, -1.5, 1.8
bpy.ops.mesh.primitive_cube_add(size=1, location=(hx, hy, hz))
hall_body = bpy.context.active_object
hall_body.scale = (12.0, 9.5, 3.6)
hall_body.data.materials.append(mat_white)

for rx in [7.2, 9.5, 11.8, 14.1, 16.4]:
    for ry in [-5.6, 2.6]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=3.6, location=(rx, ry, hz))
        bpy.context.active_object.data.materials.append(mat_vermilion)

# Right hall sloping roof
bm = bmesh.new()
gw, gd = 13, 13
width, depth, height, flare = 15.0, 12.0, 2.9, 0.48
grid = []
for j in range(gd):
    row = []
    vy = ((j / (gd - 1)) - 0.5) * depth
    ny = abs(vy) / (depth * 0.5)
    for i in range(gw):
        vx = ((i / (gw - 1)) - 0.5) * width
        nx = abs(vx) / (width * 0.5)
        r = math.sqrt(nx**2 + ny**2) / 1.4142
        z = (1.0 - (r**1.35)) * height
        edge = max(nx, ny)
        if edge > 0.6:
            t = (edge - 0.6) / 0.4
            z += (t**2.5) * (height * flare)
        row.append(bm.verts.new((vx, vy, z)))
    grid.append(row)
bm.verts.ensure_lookup_table()
for j in range(gd - 1):
    for i in range(gw - 1):
        bm.faces.new((grid[j][i], grid[j][i+1], grid[j+1][i+1], grid[j+1][i]))
mesh = bpy.data.meshes.new("Right_Hall_Tile_Roof")
bm.to_mesh(mesh)
bm.free()
obj = bpy.data.objects.new("Right_Hall_Tile_Roof", mesh)
bpy.context.collection.objects.link(obj)
obj.location = (hx, hy, hz + 1.8)
for p in obj.data.polygons:
    p.use_smooth = True
mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
mod.thickness = 0.28
obj.data.materials.append(mat_tile)

bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=12.0, location=(hx, hy, hz + 4.7), rotation=(0, math.radians(90), 0))
bpy.context.active_object.data.materials.append(mat_ridge)

# 2. Left Pavilion Eave & Gilded Gegyo
lx, ly, lz = -10.5, -6.5, 0.9
bpy.ops.mesh.primitive_cube_add(size=1, location=(lx, ly, lz))
left_eave = bpy.context.active_object
left_eave.scale = (5.5, 4.2, 1.2)
left_eave.rotation_euler = (math.radians(-6), math.radians(14), math.radians(-16))
left_eave.data.materials.append(mat_tile)

bpy.ops.mesh.primitive_cone_add(radius1=0.52, depth=0.9, location=(-8.5, -7.5, 1.3), rotation=(0, 0, math.radians(45)))
bpy.context.active_object.data.materials.append(mat_gold)

bpy.ops.mesh.primitive_cube_add(size=1, location=(-8.5, -6.8, 0.7))
bpy.context.active_object.scale = (4.4, 0.35, 0.22)
bpy.context.active_object.rotation_euler = (math.radians(-6), math.radians(14), math.radians(-16))
bpy.context.active_object.data.materials.append(mat_vermilion)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("Surrounding temple halls crafted.")
""", "[STAGE 11/14] Constructing Right Temple Hall & Left Gabled Eave with Golden Gegyo..."),

    # STAGE 11: Vibrant Autumn Momiji Foliage (Base Trees & Top-Right Overhang)
    (r"""
import bpy
import math

mat_scarlet = bpy.data.materials.get("Mat_MomijiScarlet")
mat_orange = bpy.data.materials.get("Mat_MomijiOrange")
mat_bark = bpy.data.materials.get("Mat_Bark")

def plant_momiji(name, x, y, z, rad, fol_mat, clusters=7):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=z * 1.3, location=(x, y, z * 0.45))
    trunk = bpy.context.active_object
    trunk.rotation_euler = (math.radians(math.sin(x) * 8), math.radians(math.cos(y) * 8), 0)
    trunk.data.materials.append(mat_bark)
    
    for k in range(clusters):
        ang = (k / clusters) * math.pi * 2.0 + (x * 0.3)
        dist = (0.35 + 0.65 * math.sin(k * 1.7)) * rad * 0.8
        ox = x + math.cos(ang) * dist
        oy = y + math.sin(ang) * dist
        oz = z + (math.cos(k * 2.1) * 0.4 * rad)
        
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=rad * 0.65, location=(ox, oy, oz))
        c = bpy.context.active_object
        c.scale = (1.3, 1.2, 0.7)
        for poly in c.data.polygons:
            poly.use_smooth = True
        c.data.materials.append(fol_mat)

# 1. Base Crimson Maples (covering base of pagoda)
base_maples = [
    ("BaseMomiji_0", 0.8, -5.2, 1.6, 1.9, mat_scarlet),
    ("BaseMomiji_1", -0.6, -5.8, 1.3, 1.6, mat_scarlet),
    ("BaseMomiji_2", 2.6, -4.8, 2.0, 2.0, mat_scarlet),
    ("BaseMomiji_3", 3.8, -4.2, 2.4, 1.7, mat_orange),
    ("BaseMomiji_4", -2.4, -5.5, 1.4, 1.6, mat_scarlet),
    ("BaseMomiji_5", 1.4, -6.5, 1.1, 1.5, mat_scarlet),
]

for name, tx, ty, tz, rad, fmat in base_maples:
    plant_momiji(name, tx, ty, tz, rad, fmat, clusters=7)

# 2. Midground Right Scarlet Maples
plant_momiji("RightMomiji_0", 6.2, -6.5, 3.8, 1.9, mat_orange, clusters=8)
plant_momiji("RightMomiji_1", 7.2, -5.8, 4.4, 2.1, mat_scarlet, clusters=8)
plant_momiji("RightMomiji_2", 5.6, -7.4, 4.6, 1.7, mat_scarlet, clusters=7)

# 3. Top-Right Bokeh Overhanging Branch (in foreground close to camera!)
bokeh_leaves = [
    ("Bokeh_0", 3.8, -19.5, 8.8, 1.1, mat_orange),
    ("Bokeh_1", 4.8, -18.8, 9.4, 1.3, mat_orange),
    ("Bokeh_2", 3.2, -20.2, 8.2, 0.9, mat_scarlet),
    ("Bokeh_3", 5.6, -18.0, 10.0, 1.4, mat_orange),
    ("Bokeh_4", 2.6, -21.0, 7.6, 0.8, mat_scarlet),
]

for name, bx, by, bz, brad, bmat in bokeh_leaves:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=brad, location=(bx, by, bz))
    fol = bpy.context.active_object
    fol.scale = (1.4, 1.2, 0.75)
    for poly in fol.data.polygons:
        poly.use_smooth = True
    fol.data.materials.append(bmat)

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
print("Autumn Momiji planted.")
""", "[STAGE 12/14] Planting Multi-Cluster Fiery Autumn Momiji Foliage with Top-Right Bokeh..."),

    # STAGE 12: Telephoto Camera Framing, Autumn Sunlight & Viewport Setup
    (r"""
import bpy
import math

# 1. 76mm Telephoto Lens Camera
cam_data = bpy.data.cameras.new(name="Camera_Kiyomizudera_Final")
cam_data.lens = 76.0
cam_data.dof.use_dof = True
cam_data.dof.focus_distance = 27.5
cam_data.dof.aperture_fstop = 4.8

cam = bpy.data.objects.new(name="Camera_Kiyomizudera_Final", object_data=cam_data)
bpy.context.collection.objects.link(cam)
cam.location = (0.5, -27.5, 3.8)
cam.rotation_euler = (math.radians(102.5), 0, math.radians(2.2))
bpy.context.scene.camera = cam

# 2. Direct Warm Autumn Sun
sun_data = bpy.data.lights.new(name="Sun_KyotoAutumn", type='SUN')
sun_data.energy = 5.8
sun_data.color = (1.0, 0.98, 0.93)
sun_obj = bpy.data.objects.new(name="Sun_KyotoAutumn", object_data=sun_data)
bpy.context.collection.objects.link(sun_obj)
sun_obj.location = (-16.0, -18.0, 32.0)
sun_obj.rotation_euler = (math.radians(48.0), math.radians(24.0), math.radians(-35.0))

# 3. Ambient Cyan Sky Fill
sky_data = bpy.data.lights.new(name="Sky_AmbientFill", type='SUN')
sky_data.energy = 1.8
sky_data.color = (0.35, 0.72, 1.0)
sky_obj = bpy.data.objects.new(name="Sky_AmbientFill", object_data=sky_data)
bpy.context.collection.objects.link(sky_obj)
sky_obj.location = (18.0, 15.0, 25.0)
sky_obj.rotation_euler = (math.radians(-50.0), math.radians(-15.0), math.radians(140.0))

# 4. Pure Azure Kyoto Autumn Sky World
world = bpy.context.scene.world or bpy.data.worlds.new("World_KyotoAutumnSky")
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.22, 0.60, 0.98, 1.0)
    bg.inputs['Strength'].default_value = 1.35

# 5. 4K UHD Setup & AgX Look
scene = bpy.context.scene
scene.render.resolution_x = 3840
scene.render.resolution_y = 2400
scene.render.resolution_percentage = 100
scene.view_settings.look = 'High Contrast'

# Switch 3D Viewport to Camera Perspective & RENDERED Shading
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.region_3d.view_perspective = 'CAMERA'
                space.shading.type = 'RENDERED'

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=5)
print("Camera, lighting and rendered viewport active!")
""", "[STAGE 13/14] Aligning 76mm Telephoto Lens, Setting Autumn Sunlight & Invoking 4K Viewport..."),

    # STAGE 13: 4K UHD Render Execution & Save Image
    (r"""
import bpy

bpy.ops.render.render()
img = bpy.data.images.get('Render Result')
if img:
    save_path = 'c:/Users/ayush/Downloads/claude code setup/kiyomizudera_4k_render.png'
    img.save_render(save_path)
    print("4K Render saved to:", save_path)
else:
    print("ERROR: Render Result not found!")
""", "[STAGE 14/14] Executing 4K UHD Photorealistic Final Render & Saving to Disk...")
]

def main():
    print("==========================================================================")
    print("  LAUNCHING VISIBLE MASTERPIECE BUILD IN BLENDER APP (KIYOMIZU-DERA)      ")
    print("==========================================================================")
    
    focus_blender()
    
    for idx, (code, desc) in enumerate(STAGES):
        print(f"\n{desc}")
        focus_blender()
        resp = send_blender_code(code)
        status = resp.get('status')
        result_text = resp.get('result', {}).get('result', '')
        print(f"Blender Execution: {status} | {result_text.strip()}")
        # Pause 2.2 seconds between stages so the user's eyes track every single piece being assembled!
        time.sleep(2.2)

    # Copy to web page asset folder
    try:
        shutil.copy2(
            r"c:\Users\ayush\Downloads\claude code setup\kiyomizudera_4k_render.png",
            r"c:\Users\ayush\Downloads\claude code setup\samurai_temple_webpage\kiyomizudera_4k_render.png"
        )
        print("Updated web page render asset: samurai_temple_webpage/kiyomizudera_4k_render.png")
    except Exception as e:
        print("Copy error:", e)

    print("\n==========================================================================")
    print("  BUILD COMPLETE: 4K REPLICA VISIBLE IN BLENDER & SAVED TO DISK!          ")
    print("==========================================================================")

if __name__ == '__main__':
    main()
