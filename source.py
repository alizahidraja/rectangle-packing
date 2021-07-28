from rectpack import newPacker
import matplotlib.pyplot as plt
from matplotlib import patches
import svgwrite
import streamlit as st
import base64

red_w = st.text_input("Enter Dimension of Red Box Width:", "137")
red_h = st.text_input("Enter Dimension of Red Box Height:", "300")
green_w = st.text_input("Enter Dimension of Green Box Widtht:", "52")
green_h = st.text_input("Enter Dimension of Green Box Height:", "110")
green_d = st.text_input("Enter Dimension of Green Box Depth:", "17")
amount = st.text_input("Enter Amount:", "2")

if st.button('Pack Boxes!'):
    material_box = [(float(red_w), float(red_h))]
    box = [float(green_w), float(green_h), float(green_d)]
    tot = int(amount)

    total_boxes = []

    for i in range(tot):
        total_boxes.append([box[0], box[1]])
        total_boxes.append([box[1], box[0]])


        total_boxes.append([box[0], box[2]])
        total_boxes.append([box[2], box[0]])

        total_boxes.append([box[1], box[2]])
        
        total_boxes.append([(box[2] + 4.5) / 2, box[1]])
        total_boxes.append([(box[2] + 4.5) / 2, box[1]])

    dwg = svgwrite.Drawing('test.svg', profile='full')

    dwg.add(dwg.rect((0,0), (material_box[0][0], material_box[0][1]), stroke=svgwrite.rgb(255, 0, 0, '%'), fill='white', stroke_width=0.265))

    packer = newPacker()
    for r in total_boxes:
      packer.add_rect(*r)


    for b in material_box:
      packer.add_bin(*b)


    packer.pack()


    fitted_box = 0
    for index, abin in enumerate(packer):
      bw, bh  = abin.width, abin.height
      fitted_box = len(abin)
      fig = plt.figure(figsize=(20, 15))
      
      ax = fig.add_subplot(111, aspect='equal')
      
      for rect in abin:
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        
        dwg.add(dwg.rect((x, y), (w, h), stroke=svgwrite.rgb(0, 255, 0, '%'), fill='green', stroke_width=0.265))
        plt.axis([0,bw,0,bh])
        
        ax.add_patch(
            patches.Rectangle(
                (x, y),  # (x,y)
                w,          # width
                h,          # height
                facecolor = "#00ffff",
                edgecolor = "green",
                linewidth = 1
            )
        )
      #fig.savefig("test.png", dpi=144) 
    
    #dwg.save()

    st.write("Total box = " + str(len(total_boxes)) + ", boxes fitted = " + str(fitted_box))
    st.write(fig)
    with open("test.svg", "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/svg;base64,{b64}" download="image.svg">Download SVG file</a>'
        
        st.markdown(href, unsafe_allow_html=True)



 
