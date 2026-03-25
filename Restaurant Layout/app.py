import streamlit as st
import matplotlib.pyplot as plt
import math

st.title("Restaurant Layout Generator")

# Inputs
area = st.number_input("Total Area (sqm)", value=150)
num_tables = st.number_input("Number of Tables", value=12)
num_chairs = st.number_input("Chairs per Table", value=4)
floors = st.number_input("Number of Floors", value=1)
transport = st.selectbox("Transportation", ["Stairs", "Elevator", "Escalator"])

if st.button("Generate Layout"):

    ratio = 4 / 3
    room_width = math.sqrt(area * ratio)
    room_height = area / room_width

    fig, ax = plt.subplots(figsize=(6, 5))

    padding = 2
    ax.set_xlim(-padding, room_width + padding)

    floor_gap = 2
    total_height = floors * room_height + (floors - 1) * floor_gap
    ax.set_ylim(-padding, total_height + padding)

    ax.set_aspect('equal')
    ax.set_title(f"{floors} Floor(s) | {area} sqm")
    ax.axis('off')

    table_w, table_h = 0.8, 0.8
    chair_r = 0.25
    module_w, module_h = 2.5, 2.5

    tables_per_floor = num_tables // floors

    for f in range(floors):
        y_offset = f * (room_height + floor_gap)

        floor_rect = plt.Rectangle((0, y_offset), room_width, room_height,
                                   edgecolor='gray', facecolor='#f5f5f5')
        ax.add_patch(floor_rect)

        cols = max(1, int(room_width // module_w))
        rows = math.ceil(tables_per_floor / cols)

        start_x = (room_width - cols * module_w) / 2 + 1
        start_y = y_offset + (room_height - rows * module_h) / 2 + 1

        count = 0
        for r in range(rows):
            for c in range(cols):
                if count >= tables_per_floor:
                    break

                x = start_x + (c * module_w)
                y = start_y + (r * module_h)

                table = plt.Rectangle((x, y), table_w, table_h,
                                      edgecolor='black', facecolor='brown')
                ax.add_patch(table)

                center_x = x + table_w / 2
                center_y = y + table_h / 2
                radius = (table_w / 2) + chair_r + 0.1

                for ch in range(num_chairs):
                    angle = (2 * math.pi * ch / num_chairs)
                    chair_x = center_x + radius * math.cos(angle)
                    chair_y = center_y + radius * math.sin(angle)

                    chair = plt.Circle((chair_x, chair_y), chair_r,
                                       facecolor='blue')
                    ax.add_patch(chair)

                count += 1

    st.pyplot(fig)